import os
import json
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from pm_convert import convert_to_aedt  # Ensure this import is available in your context

# Configure logging to minimize verbosity
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Define OAuth scopes centrally
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/youtube.readonly'
]

def get_paths(user_folder):
    """Construct paths to the client secret and token files based on user folder."""
    client_secret_file = None
    token_file = f'{user_folder}/token.json'

    # Locate the client_secret file within the user's folder
    for file_name in os.listdir(user_folder):
        if file_name.startswith('client_secret_') and file_name.endswith('.json'):
            client_secret_file = os.path.join(user_folder, file_name)
            break

    if client_secret_file is None:
        raise FileNotFoundError(f"No client_secret file found in {user_folder}")

    return client_secret_file, token_file

def load_credentials(user_folder):
    """Load and refresh OAuth 2.0 credentials."""
    client_secret_file, token_file = get_paths(user_folder)
    creds = None

    # If the token file exists, load existing credentials
    if os.path.exists(token_file):
        with open(token_file, 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token))

    # If there are no credentials or if they are not valid, refresh or reauthorize
    if not creds or not creds.valid:
        creds = refresh_or_reauthorize_credentials(creds, client_secret_file, token_file)

    return creds

def refresh_or_reauthorize_credentials(creds, client_secret_file, token_file):
    """Refresh or reauthorize credentials."""
    try:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
            # Create a dictionary with credential information
            token_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                # Safely handle potential None for scopes
                'scopes': list(creds.scopes) if creds.scopes is not None else []
            }
            
            # Safely write token data
            with open(token_file, 'w') as f:
                json.dump(token_data, f)
        else:
            raise RefreshError
    except RefreshError:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Create a dictionary with new credential information
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            # Safely handle potential None for scopes
            'scopes': list(creds.scopes) if creds.scopes is not None else []
        }
        
        # Safely write token data
        with open(token_file, 'w') as f:
            json.dump(token_data, f)
    
    return creds
