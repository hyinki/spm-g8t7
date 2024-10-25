import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Classes.Wfh_Request import WFHRequests
from Classes.Database import db

import sys
import os

# Add the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='module')
def test_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def wfh_request():
    return WFHRequests(
        request_ID=1,
        start_date=date(2024, 7, 24),
        end_date=date(2024, 7, 29),
        Requester_ID=150192,
        Requester_Supervisor=151408,
        Monday='AM',
        Tuesday='AM',
        Wednesday='AM',
        Thursday='PM',
        Friday='AM',
        Saturday='PM',
        Sunday='Whole Day',
        Request_Status='Pending'
    )

@patch('Classes.Wfh_Request.WFHRequests.query')  # Ensure this matches your import path
def test_get_by_id_existing(mock_query, wfh_request, test_app):
    # Mock the return value of query.get to return the wfh_request instance
    mock_query.get.return_value = wfh_request
    
    # Call the method to get the request by ID
    with test_app.app_context():
        result = WFHRequests.get_by_id(1)
        
    # Assertions
    assert result is not None
    assert result.request_ID == 1
    assert result.Requester_ID == 150192

@patch('Classes.Wfh_Request.WFHRequests.query')  # Ensure this matches your import path
def test_get_by_id_non_existent(mock_query, test_app):
    # Mock the return value of query.get to return None
    mock_query.get.return_value = None
    
    # Call the method to get the request by ID
    with test_app.app_context():
        result = WFHRequests.get_by_id(999)
    
    # Assertions
    assert result is None

@patch('Classes.Wfh_Request.WFHRequests.query')  # Ensure this matches your import path
def test_get_all_empty(mock_query, test_app):
    # Mock the return value of query.all to return an empty list
    mock_query.all.return_value = []
    
    # Call the method to get all requests
    with test_app.app_context():
        result = WFHRequests.get_all()
    
    # Assertions
    assert result == []

@patch('Classes.Wfh_Request.WFHRequests.query')  # Ensure this matches your import path
def test_get_all_multiple(mock_query, test_app):
    # Mock the return value of query.all to return a list of wfh_request instances
    wfh_request1 = WFHRequests(
        request_ID=1,
        start_date=date(2024, 7, 24),
        end_date=date(2024, 7, 29),
        Requester_ID=150192,
        Requester_Supervisor=151408,
        Monday='AM',
        Tuesday='AM',
        Wednesday='AM',
        Thursday='PM',
        Friday='AM',
        Saturday='PM',
        Sunday='Whole Day',
        Request_Status='Pending'
    )
    wfh_request2 = WFHRequests(
        request_ID=2,
        start_date=date(2024, 8, 1),
        end_date=date(2024, 8, 5),
        Requester_ID=150193,
        Requester_Supervisor=151409,
        Monday='PM',
        Tuesday='PM',
        Wednesday='PM',
        Thursday='AM',
        Friday='PM',
        Saturday='AM',
        Sunday='Whole Day',
        Request_Status='Approved'
    )

    mock_query.all.return_value = [wfh_request1,wfh_request2]
    
    # Call the method to get all requests
    with test_app.app_context():
        result = WFHRequests.get_all()
    
    # Assertions
    assert len(result) == 2
    assert result[0].request_ID == 1
    assert result[0].Requester_ID == 150192
    assert result[1].request_ID == 2
    assert result[1].Requester_ID == 150193