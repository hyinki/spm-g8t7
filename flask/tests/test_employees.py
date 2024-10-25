import pytest
from unittest.mock import patch
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# Add the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.Employees import Employees
from requests import Session

# Create the Flask application and configure it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
app.secret_key = 'test'  # Set a secret key for session management
db = SQLAlchemy()

# Initialize the SQLAlchemy instance with the Flask app
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

@pytest.fixture(scope='module')
def app_context():
    ctx = app.app_context()
    ctx.push()
    yield ctx
    ctx.pop()

@pytest.fixture
def request_context():
    with app.test_request_context():
        yield

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_by_id_success(mock_query):
    # Create a mock employee instance
    mock_employee = Employees(
        Staff_ID=1,
        Staff_FName='John',
        Staff_LName='Doe',
        Dept='HR',
        Position='Manager',
        Country='USA',
        Email='john.doe@example.com',
        User_Password='scrypt:32768:8:1$qxr6mhfSMpC78JYq$94c163a55ce221239e29007ceb096b7a3e461d227a51cfd69d38f1bf1ee1d6a5ffbc1be0d72a2d7602334f67d52a91c75be954c22a58a62ae07c1bd77ee30b64',
        Role=1
    )
    # Mock the return value of the query
    mock_query.get.return_value = mock_employee
    
    # Call the method to get the employee by ID
    employee1 = Employees.get_by_id(1)
    
    # Assertions for employee details
    assert employee1 is not None
    assert employee1.Staff_FName == 'John'
    assert employee1.Staff_LName == 'Doe'

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_by_id_fail(mock_query, app_context):
    # Create a mock employee instance

    # Mock the return value of the query
    mock_query.get.return_value = None
    
    # Call the method to get the employee by ID
    employee1 = Employees.get_by_id(99)
    
    # Assertions for employee details
    assert employee1 is None


@patch('Classes.Employees.Employees.query')
@patch('Classes.Employees.db.session.execute')
def test_check_password_pass(mock_execute, mock_query, app_context, request_context):
    # Create a mock employee instance
    mock_employee = Employees(
        Staff_ID=1,
        Staff_FName='John',
        Staff_LName='Doe',
        Dept='HR',
        Position='Manager',
        Country='USA',
        Email='john.doe@example.com',
        User_Password='scrypt:32768:8:1$qxr6mhfSMpC78JYq$94c163a55ce221239e29007ceb096b7a3e461d227a51cfd69d38f1bf1ee1d6a5ffbc1be0d72a2d7602334f67d52a91c75be954c22a58a62ae07c1bd77ee30b64',
        Role=1
    )
    # Mock the return value of the query
    mock_query.get.return_value = mock_employee
    # Mock the SQL execution result
    mock_execute.return_value.scalar.return_value = 0
    
    # Call the method to check the password
    password = Employees.check_pword(1)
    
    # Assertions for password
    assert password == 'scrypt:32768:8:1$qxr6mhfSMpC78JYq$94c163a55ce221239e29007ceb096b7a3e461d227a51cfd69d38f1bf1ee1d6a5ffbc1be0d72a2d7602334f67d52a91c75be954c22a58a62ae07c1bd77ee30b64'


@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_check_password_fail(mock_query):
    # Mock the return value of the query to be None (employee not found)
    mock_query.get.return_value = None

    password = Employees.check_pword(1)

    assert password == "nope"

def test_check_HR_roles():
    role = 1

    actualRole= Employees.get_role(role)
    
    assert actualRole == "HR"

def test_check_Staff_roles():

    role = 2
    actualRole= Employees.get_role(role)
    
    assert actualRole == "Staff"

def test_check_Manager_roles():

    role = 3
    actualRole= Employees.get_role(role)
    
    assert actualRole == "Manager"

def test_check_invalid_roles():
    role1 = 4
    role2=7
    role3=45
    role4="nope"
    role5=None
    
    actualRole1= Employees.get_role(role1)
    actualRole2= Employees.get_role(role2)
    actualRole3= Employees.get_role(role3)
    actualRole4= Employees.get_role(role4)
    actualRole5=Employees.get_role(role5)

    assert actualRole1== "Invalid"
    assert actualRole2== "Invalid"
    assert actualRole3== "Invalid"
    assert actualRole4== "Invalid"
    assert actualRole5== "Invalid"

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_all_empty(mock_query):
    # Mock the return value of the query to be an empty list
    mock_query.all.return_value = []
    
    # Call the method to get all employees
    employees = Employees.get_all()
    
    # Assertions for an empty list
    assert employees == []

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_all_multiple(mock_query):
    # Create mock employee instances
    mock_employee1 = Employees(
        Staff_ID=1,
        Staff_FName='John',
        Staff_LName='Doe',
        Dept='HR',
        Position='Manager',
        Country='USA',
        Email='john.doe@example.com',
        User_Password='password1',
        Role=1
    )
    mock_employee2 = Employees(
        Staff_ID=2,
        Staff_FName='Jane',
        Staff_LName='Smith',
        Dept='IT',
        Position='Developer',
        Country='USA',
        Email='jane.smith@example.com',
        User_Password='password2',
        Role=2
    )
    # Mock the return value of the query
    mock_query.all.return_value = [mock_employee1, mock_employee2]
    
    # Call the method to get all employees
    employees = Employees.get_all()
    
    # Assertions for multiple employees
    assert len(employees) == 2
    assert employees[0].Staff_FName == 'John'
    assert employees[1].Staff_FName == 'Jane'

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_all_single(mock_query):
    # Create a mock employee instance
    mock_employee = Employees(
        Staff_ID=1,
        Staff_FName='John',
        Staff_LName='Doe',
        Dept='HR',
        Position='Manager',
        Country='SG',
        Email='john.doe@example.com',
        User_Password='password1',
        Role=1
    )
    # Mock the return value of the query
    mock_query.all.return_value = [mock_employee]
    
    # Call the method to get all employees
    employees = Employees.get_all()
    
    # Assertions for a single employee
    assert employees[0].Country == 'SG'
    assert employees[0].Dept == 'HR'

@patch('Classes.Employees.Employees.query')  # Ensure this matches your import path
def test_get_all_order(mock_query):
    # Create mock employee instances
    mock_employee1 = Employees(
        Staff_ID=1,
        Staff_FName='John',
        Staff_LName='Doe',
        Dept='HR',
        Position='Manager',
        Country='USA',
        Email='john.doe@example.com',
        User_Password='password1',
        Role=1
    )
    mock_employee2 = Employees(
        Staff_ID=2,
        Staff_FName='Jane',
        Staff_LName='Smith',
        Dept='IT',
        Position='Developer',
        Country='USA',
        Email='jane.smith@example.com',
        User_Password='password2',
        Role=3
    )
    # Mock the return value of the query
    mock_query.all.return_value = [mock_employee1, mock_employee2]
    
    # Call the method to get all employees
    employees = Employees.get_all()
    
    # Assertions for the order of employees
    assert employees[0].Role == 1
    assert employees[1].Role == 3