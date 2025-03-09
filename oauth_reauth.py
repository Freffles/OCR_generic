import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from oauth_handler import get_paths  # Import get_paths from oauth_handler


# Define OAuth scopes centrally
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/youtube.readonly'
]

def load_credentials(user_folder):
    """Load OAuth 2.0 credentials from the specified user folder."""
    client_secret_file, token_file = get_paths(user_folder)
    creds = None

    if os.path.exists(token_file):
        with open(token_file, 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    return creds

def refresh_or_reauthorize_credentials(creds, client_secret_file, token_file):
    """Refresh or reauthorize credentials."""
    try:
        creds.refresh(Request())
        with open(token_file, 'w') as token_file:
            token_file.write(creds.to_json())
            print("Token refreshed successfully.")
    except RefreshError:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token_file:
            token_file.write(creds.to_json())
            print("There was a refresh error but token now refreshed successfully.")
    return creds

def main():
    users = ['rayluckins', 'wozard']
    
    for user in users:
        try:
            client_secret_file, token_file = get_paths(user)
            creds = load_credentials(user)
            
            if not creds or not creds.valid:
                creds = refresh_or_reauthorize_credentials(creds, client_secret_file, token_file)
            else:
                print(f"Token for {user} is still valid, no action required.")
        except Exception as e:
            print(f"Error processing {user}: {e}")

if __name__ == '__main__':
    main()
