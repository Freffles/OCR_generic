import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError

# Import the modules to test
from oauth_handler import get_credentials_path, get_credentials, AuthError
from oauth_reauth import reauthorize

# Test fixtures
@pytest.fixture
def mock_credentials():
    """Create a mock Credentials object."""
    creds = MagicMock(spec=Credentials)
    creds.valid = True
    creds.expired = False
    creds.token = "mock_token"
    creds.refresh_token = "mock_refresh_token"
    creds.client_id = "mock_client_id"
    creds.client_secret = "mock_client_secret"
    creds.scopes = ["https://www.googleapis.com/auth/gmail.readonly", 
                    "https://www.googleapis.com/auth/spreadsheets"]
    return creds

@pytest.fixture
def mock_token_data():
    """Create mock token data."""
    return {
        "token": "mock_token",
        "refresh_token": "mock_refresh_token",
        "client_id": "mock_client_id",
        "client_secret": "mock_client_secret",
        "scopes": ["https://www.googleapis.com/auth/gmail.readonly", 
                  "https://www.googleapis.com/auth/spreadsheets"]
    }

# Tests for oauth_handler.py
def test_get_credentials_path():
    """Test finding client_secret file."""
    with patch('os.listdir', return_value=['client_secret_123.json', 'other_file.txt']):
        path = get_credentials_path('test_dir')
        expected_path = os.path.join('test_dir', 'client_secret_123.json')
        assert path == expected_path

def test_get_credentials_path_not_found():
    """Test error when client_secret file not found."""
    with patch('os.listdir', return_value=['other_file.txt']):
        with pytest.raises(FileNotFoundError):
            get_credentials_path('test_dir')

def test_get_credentials_existing_valid(mock_credentials, mock_token_data):
    """Test loading existing valid credentials."""
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=json.dumps(mock_token_data))), \
         patch('google.oauth2.credentials.Credentials.from_authorized_user_info', 
               return_value=mock_credentials):
        
        creds = get_credentials('test_dir', 'test_token.json')
        assert creds.valid
        assert creds.token == "mock_token"

def test_get_credentials_refresh(mock_credentials, mock_token_data):
    """Test refreshing expired credentials."""
    mock_credentials.valid = False
    mock_credentials.expired = True
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=json.dumps(mock_token_data))), \
         patch('google.oauth2.credentials.Credentials.from_authorized_user_info', 
               return_value=mock_credentials), \
         patch.object(mock_credentials, 'refresh'), \
         patch('json.dump'):
        
        creds = get_credentials('test_dir', 'test_token.json')
        mock_credentials.refresh.assert_called_once()

def test_get_credentials_new_flow(mock_credentials):
    """Test creating new credentials when none exist."""
    flow_mock = MagicMock()
    flow_mock.run_local_server.return_value = mock_credentials
    
    with patch('os.path.exists', return_value=False), \
         patch('oauth_handler.get_credentials_path', return_value=os.path.join('test_dir', 'client_secret.json')), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', 
               return_value=flow_mock), \
         patch('builtins.open', mock_open()), \
         patch('json.dump'):
        
        creds = get_credentials('test_dir', 'test_token.json')
        flow_mock.run_local_server.assert_called_once_with(port=0)
        assert creds == mock_credentials

def test_get_credentials_refresh_error(mock_credentials, mock_token_data):
    """Test handling refresh error by creating new credentials."""
    mock_credentials.valid = False
    mock_credentials.expired = True
    mock_credentials.refresh.side_effect = RefreshError()
    
    flow_mock = MagicMock()
    flow_mock.run_local_server.return_value = mock_credentials
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=json.dumps(mock_token_data))), \
         patch('google.oauth2.credentials.Credentials.from_authorized_user_info', 
               return_value=mock_credentials), \
         patch('oauth_handler.get_credentials_path', return_value=os.path.join('test_dir', 'client_secret.json')), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', 
               return_value=flow_mock), \
         patch('json.dump'):
        
        creds = get_credentials('test_dir', 'test_token.json')
        mock_credentials.refresh.assert_called_once()
        flow_mock.run_local_server.assert_called_once_with(port=0)

# Tests for oauth_reauth.py
def test_reauthorize_success():
    """Test successful reauthorization."""
    with patch('os.path.exists', return_value=True), \
         patch('os.remove'), \
         patch('oauth_reauth.get_credentials'):
        
        result = reauthorize('test_dir', 'test_token.json')
        assert result is True

def test_reauthorize_remove_error():
    """Test handling error when removing token file."""
    with patch('os.path.exists', return_value=True), \
         patch('os.remove', side_effect=Exception("Test error")), \
         patch('oauth_reauth.get_credentials'):
        
        result = reauthorize('test_dir', 'test_token.json')
        assert result is False

def test_reauthorize_auth_error():
    """Test handling authentication error."""
    with patch('os.path.exists', return_value=True), \
         patch('os.remove'), \
         patch('oauth_reauth.get_credentials', side_effect=AuthError("Test auth error")):
        
        result = reauthorize('test_dir', 'test_token.json')
        assert result is False

def test_reauthorize_unexpected_error():
    """Test handling unexpected error."""
    with patch('os.path.exists', return_value=True), \
         patch('os.remove'), \
         patch('oauth_reauth.get_credentials', side_effect=Exception("Test unexpected error")):
        
        result = reauthorize('test_dir', 'test_token.json')
        assert result is False