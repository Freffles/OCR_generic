import os
import json
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define OAuth scopes for both Gmail and Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'  # Added Drive scope for accessing spreadsheets
]

# Default paths for token and client secret files
DEFAULT_TOKEN_FILE = 'token.json'
DEFAULT_CREDENTIALS_DIR = '.'

def get_credentials_path(credentials_dir=DEFAULT_CREDENTIALS_DIR):
    """Find the client_secret file in the credentials directory."""
    for file_name in os.listdir(credentials_dir):
        if file_name.startswith('client_secret_') and file_name.endswith('.json'):
            return os.path.join(credentials_dir, file_name)
    
    raise FileNotFoundError(f"No client_secret file found in {credentials_dir}")

def get_credentials(credentials_dir=DEFAULT_CREDENTIALS_DIR, token_file=DEFAULT_TOKEN_FILE):
    """
    Get OAuth credentials for Google APIs.
    
    This function handles the OAuth flow for a single user, requesting access to both
    Gmail and Google Sheets APIs in a single authorization flow.
    
    Args:
        credentials_dir: Directory containing the client_secret file
        token_file: Path to the token file (relative to credentials_dir)
    
    Returns:
        Google OAuth credentials object
    
    Raises:
        FileNotFoundError: If client_secret file is not found
        AuthError: If authentication fails
    """
    token_path = os.path.join(credentials_dir, token_file)
    creds = None
    
    # Load existing credentials if available
    if os.path.exists(token_path):
        try:
            with open(token_path, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
            logger.info("Loaded existing credentials")
        except Exception as e:
            logger.warning(f"Error loading credentials: {e}")
    
    # If credentials don't exist or are invalid, refresh or get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Refreshing expired credentials")
                creds.refresh(Request())
            except RefreshError as e:
                logger.warning(f"Failed to refresh token: {e}")
                creds = None
        
        # If refresh failed or no credentials exist, run the OAuth flow
        if not creds:
            try:
                client_secret_path = get_credentials_path(credentials_dir)
                logger.info(f"Starting OAuth flow with client secret: {client_secret_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info("Successfully obtained new credentials")
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                raise AuthError(f"Failed to authenticate: {e}")
        
        # Save the credentials for future use
        try:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            logger.info(f"Saved credentials to {token_path}")
        except Exception as e:
            logger.warning(f"Failed to save credentials: {e}")
    
    return creds

class AuthError(Exception):
    """Exception raised for authentication errors."""
    pass
