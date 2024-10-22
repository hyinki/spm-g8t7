import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import check_password_hash
from Classes.Employees import Employees
from Classes.Login import Login  # Adjust the import based on your actual module structure

@pytest.fixture
def login():
    return Login()

@patch('Classes.Employees.Employees.check_pword')
@patch('werkzeug.security.check_password_hash')
def test_check_user_password_valid(mock_check_password_hash, mock_check_pword, login):
    # Mock the return value of check_pword to be a valid password hash
    mock_check_pword.return_value = 'scrypt:32768:8:1$jTN66XjbtEr5yO1p$1a515bd1b025a48f9fb82e292fe6c52bcd4df7ea366bf272ddab298756b909cc7dcab9fc2589be231c270edbfbacc7f5ace2da9693c95fcbbbef05cad0f8bf77'
    # Mock the return value of check_password_hash to be True
    mock_check_password_hash.return_value = True
    
    # Call the method with a valid user ID and correct password
    result = login.check_user_password(1, 'abcdefg123456')
    
    # Assertions
    assert result is True

@patch('Classes.Employees.Employees.check_pword')
@patch('werkzeug.security.check_password_hash')
def test_check_user_password_invalid_password(mock_check_password_hash, mock_check_pword, login):
    # Mock the return value of check_pword to be a valid password hash
    mock_check_pword.return_value = 'scrypt:32768:8:1$jTN66XjbtEr5yO1p$1a515bd1b025a48f9fb82e292fe6c52bcd4df7ea366bf272ddab298756b909cc7dcab9fc2589be231c270edbfbacc7f5ace2da9693c95fcbbbef05cad0f8bf77'
 
    mock_check_password_hash.return_value = False
    
    # Call the method with a valid user ID and incorrect password
    result = login.check_user_password(1, 'abcdefg123453')
    
    # Assertions
    assert result is False

@patch('Classes.Employees.Employees.check_pword')
def test_check_user_password_invalid_user(mock_check_pword, login):
    # Mock the return value of check_pword to be None (invalid user ID)
    mock_check_pword.return_value = None
    
    # Call the method with an invalid user ID
    result = login.check_user_password(999, 'any_password')
    
    # Assertions
    assert result is False


@patch('Classes.Employees.Employees.check_pword')
@patch('werkzeug.security.check_password_hash')
def test_check_user_password_empty_password(mock_check_password_hash, mock_check_pword, login):
    # Mock the return value of check_pword to be a valid password hash
    mock_check_pword.return_value = 'hashed_password'
    # Mock the return value of check_password_hash to be False
    mock_check_password_hash.return_value = False
    
    # Call the method with a valid user ID and empty password
    result = login.check_user_password(1, '')
    
    # Assertions
    assert result is False