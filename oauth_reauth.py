import os
import logging
from oauth_handler import get_credentials, get_credentials_path, AuthError, DEFAULT_CREDENTIALS_DIR, DEFAULT_TOKEN_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reauthorize(credentials_dir=DEFAULT_CREDENTIALS_DIR, token_file=DEFAULT_TOKEN_FILE):
    """
    Force reauthorization of OAuth credentials.
    
    This utility function is used to manually trigger the OAuth flow when needed,
    such as when scopes have changed or when the token is corrupted.
    
    Args:
        credentials_dir: Directory containing the client_secret file
        token_file: Path to the token file (relative to credentials_dir)
    
    Returns:
        True if reauthorization was successful, False otherwise
    """
    token_path = os.path.join(credentials_dir, token_file)
    
    # Remove existing token file if it exists
    if os.path.exists(token_path):
        try:
            os.remove(token_path)
            logger.info(f"Removed existing token file: {token_path}")
        except Exception as e:
            logger.error(f"Failed to remove token file: {e}")
            return False
    
    # Trigger new OAuth flow
    try:
        get_credentials(credentials_dir, token_file)
        logger.info("Successfully reauthorized and saved new credentials")
        return True
    except AuthError as e:
        logger.error(f"Reauthorization failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during reauthorization: {e}")
        return False

def main():
    """
    Command-line entry point for reauthorization.
    
    This function is called when the script is run directly.
    It attempts to reauthorize the OAuth credentials and prints the result.
    """
    try:
        success = reauthorize()
        if success:
            print("Reauthorization completed successfully.")
        else:
            print("Reauthorization failed. Check the logs for details.")
    except Exception as e:
        print(f"Error during reauthorization: {e}")

if __name__ == '__main__':
    main()
