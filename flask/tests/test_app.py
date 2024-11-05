import unittest
from app import app
from flask import json

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        cls.client = app.test_client()

    def test_login_route(self):
        # Mock data for the login request
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        
        # Make a POST request to /login with the mock data
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        
        # Check that the status code is 200 (successful login) or 401 (failed login)
        self.assertIn(response.status_code, [200, 401])

        # Check the message in the JSON response
        response_json = response.get_json()
        if response.status_code == 200:
            self.assertIn("msg", response_json)
            self.assertEqual(response_json["msg"], "Login successful.")
        else:
            self.assertEqual(response_json["msg"], "Invalid credentials.")
