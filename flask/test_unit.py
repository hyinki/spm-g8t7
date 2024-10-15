import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from Classes.Employees import Employees
from requests import Session
# Create the Flask application and configure it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
app.secret_key = 'test'  # Set a secret key for session management
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

class TestEmployeesModel(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
    def test_get_by_id(self, mock_query):
        # Create a mock employee instance
        mock_employee = Employees(
            Staff_ID=1,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='HR',
            Position='Manager',
            Country='USA',
            Email='john.doe@example.com',
            User_Password='scrypt:32768:8:1$C3zz5u4j9M0US6Ym$568405523df99fc649921272794f9782c8928d466960ea0a7440e8c788d2e032a6ec6074b8c22b4f2ef359ea32a3f2f7fbf435d8454766f84464bd91d3aa35be',
            Role=1
        )
        # Mock the return value of the query
        mock_query.get.return_value = mock_employee
        
        # Call the method
        employee = Employees.get_by_id(1)
        
        # Assertions
        self.assertIsNotNone(employee)
        self.assertEqual(employee.Staff_FName, 'John')
        self.assertEqual(employee.Staff_LName, 'Doe')



if __name__ == '__main__':
    unittest.main()