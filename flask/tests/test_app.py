import unittest
from unittest.mock import patch
from app import app, db
from flask import json, session

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client
        app.config['TESTING'] = True
        cls.client = app.test_client()

    # Test for unsuccessful login
    def test_unsuccessful_login(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        with patch('app.Login.check_user_password', return_value=False):
            response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 401)
            self.assertIn("msg", response.get_json())
            self.assertEqual(response.get_json()["msg"], "Invalid credentials.")

    # Test for submitting WFH request
    def test_submit_wfh_request(self):
        data = {
            "startDate": "2024-07-24",
            "endDate": "2024-07-25",
            "userId": "testuser",
            "supervisor": "testsup",
            "cloudinary_link": "http://example.com/image.png",
            "repeating": 0,
            "selectedDays": [
                {"day": "Monday", "timeslot": "AM"},
                {"day": "Tuesday", "timeslot": "PM"}
            ]
        }
        with patch('app.db.session.add'), patch('app.db.session.commit'):
            response = self.client.post('/submit_wfh_request', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Request submitted successfully")

    # Test for viewing own requests
    def test_view_own_requests(self):
        with patch('app.db.session.execute') as mock_execute:
            mock_execute.return_value.mappings.return_value.all.return_value = [
                {"request_ID": 1, "Requester_ID": "testuser", "Request_Status": "Approved"}
            ]
            response = self.client.get('/viewownrequests', headers={"X-userid": "testuser"})
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), list)
            self.assertEqual(response.get_json()[0]["Requester_ID"], "testuser")

    # Test for invalid endpoint
    def test_invalid_endpoint(self):
        response = self.client.get('/invalid_endpoint')
        self.assertEqual(response.status_code, 404)

    # Test for missing fields in login request
    def test_missing_fields_login(self):
        data = {
            "username": "testuser"
        }
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # Test for WFH request approval
    def test_approve_wfh_request(self):
        with patch('app.db.session.execute'), patch('app.db.session.commit'):
            response = self.client.get('/approve_request?request=1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Request approved")

    # Test for WFH request rejection
    def test_reject_wfh_request(self):
        with patch('app.db.session.execute'), patch('app.db.session.commit'):
            response = self.client.get('/reject_request?request=1')
            self.assertEqual(response.status_code, 200)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Request rejected")

    # Test for basic hello world route
    def test_hello_world(self):
        response = self.client.get('/basic_api/hello_world')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"Hello": "World"})
  
    # Test for missing user ID in the URL path
    def test_withdraw_wfh_request_missing_user_id(self):
        response = self.client.patch('/withdrawrequest/1/')
        self.assertEqual(response.status_code, 404)
   
    # Test for viewing own team in-office list
    def test_view_own_team_in_office_list(self):
        with patch('app.db.session.execute') as mock_execute:
            mock_execute.return_value.mappings.return_value.all.return_value = [
                {"Date": "2024-07-24", "AM": ["Employee1", "Employee2"], "PM": ["Employee1"]}
            ]
            response = self.client.get('/view_own_team_in_office_list', headers={"X-supervisor": "testmanager", "X-month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIn("2024-07-24", response.get_json())
            self.assertIn("AM", response.get_json()["2024-07-24"])

# Test for successful retrieval of manager view
    def test_manager_view_success(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[{"request_ID": 1, "Requester_ID": "employee1", "Request_Status": "Approved", "staff_name": "John Doe"}]):
            
            mock_execute.return_value.keys.return_value = ["request_ID", "Requester_ID", "Request_Status", "staff_name"]
            mock_execute.return_value.__iter__.return_value = [
                {"request_ID": 1, "Requester_ID": "employee1", "Request_Status": "Approved", "staff_name": "John Doe"}
            ]
            
            response = self.client.get('/api/manager_view', headers={"X-userid": "manager1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), list)
            self.assertEqual(response.get_json()[0]["Requester_ID"], "employee1")
            self.assertEqual(response.get_json()[0]["staff_name"], "John Doe")

    # Test for empty result in manager view
    def test_manager_view_empty_result(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[]):
            
            mock_execute.return_value.__iter__.return_value = []
            response = self.client.get('/api/manager_view', headers={"X-userid": "manager1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [])

   
    # Test for successful retrieval of manager view calendar
    def test_manager_view_calendar_success(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.calendar_count', return_value={"total": 5, "details": []}):
            
            mock_execute.return_value.keys.return_value = ["request_ID", "Requester_ID", "Request_Status", "staff_name"]
            mock_execute.return_value.__iter__.return_value = [
                {"request_ID": 1, "Requester_ID": "employee1", "Request_Status": "Approved", "staff_name": "John Doe"}
            ]
            
            response = self.client.get('/manager_view_calendar', headers={"X-userid": "manager1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("total", response.get_json())
            self.assertEqual(response.get_json()["total"], 5)

    # Test for empty result in manager view calendar
    def test_manager_view_calendar_empty_result(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.calendar_count', return_value={"total": 0, "details": []}):
            
            mock_execute.return_value.__iter__.return_value = []
            response = self.client.get('/manager_view_calendar', headers={"X-userid": "manager1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["total"], 0)
            self.assertEqual(response.get_json()["details"], [])

# Test for retrieving individual view with a sample response


    # Test for retrieving individual view with empty results
    def test_individual_view_empty(self):
        with patch('app.db.session.execute') as mock_execute:
            # Mocking an empty response from the database
            mock_execute.return_value.__iter__.return_value = []
            response = self.client.get('/api/individual_view', headers={"X-userid": "testuser"})
            self.assertEqual(response.status_code, 200)
            # Check if the response is an empty list
            self.assertEqual(response.get_json(), [])

    # Test for retrieving list in office with sample response
   
    # Test for list in office with no staff in office
    def test_list_in_office_empty(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.tally_people_in_office', return_value={"total": 0, "details": []}):
            # Mocking an empty main query response
            mock_execute.return_value.__iter__.return_value = []
            response = self.client.get('/manager_list_in_office', headers={"X-userid": "manager1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            # Check if the tally response indicates no staff
            self.assertEqual(response.get_json()["total"], 0)
            self.assertEqual(response.get_json()["details"], [])

 # Test for retrieving own team schedule with sample response
    def test_view_own_team_schedule_success(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[{"staff_name": "John Doe", "Request_Status": "Approved"}]):
            # Mocking database response for the main query
            mock_execute.return_value.keys.return_value = ["request_ID", "Requester_ID", "Request_Status", "staff_name"]
            mock_execute.return_value.__iter__.return_value = [
                {"request_ID": 1, "Requester_ID": "team_member", "Request_Status": "Approved", "staff_name": "John Doe"}
            ]

            # Making GET request to the endpoint
            response = self.client.get('/api/view_own_team_schedule', headers={"X-supervisor": "supervisor1", "X-month": "7"})
            self.assertEqual(response.status_code, 200)
            # Check if response structure matches expected format
            self.assertIsInstance(response.get_json(), list)
            self.assertEqual(response.get_json()[0]["staff_name"], "John Doe")
            self.assertEqual(response.get_json()[0]["Request_Status"], "Approved")

    # Test for view own team schedule with no results
    def test_view_own_team_schedule_empty(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[]):
            # Mocking empty database response
            mock_execute.return_value.__iter__.return_value = []

            response = self.client.get('/api/view_own_team_schedule', headers={"X-supervisor": "supervisor1", "X-month": "7"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [])


    # Test for staff team calendar with no team members
    def test_staff_team_view_calendar_empty(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.calendar_count', return_value={"total": 0, "details": []}):
            # Mocking empty main query response
            mock_execute.return_value.__iter__.return_value = []

            response = self.client.get('/staff_team_view_calendar', headers={"X-supervisor": "supervisor1", "X-Month": "7"})
            self.assertEqual(response.status_code, 200)
            # Check that the result shows zero team members
            self.assertEqual(response.get_json()["total"], 0)
            self.assertEqual(response.get_json()["details"], [])



    # Test for view all team in office list with no data in the department
    def test_view_all_team_in_office_list_empty(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.tally_people_in_office', return_value={"total": 0, "details": []}):
            # Mocking empty main query response
            mock_execute.return_value.__iter__.return_value = []

            response = self.client.get('/api/view_all_team_in_office_list', query_string={"dept": "Finance", "month": "7"})
            self.assertEqual(response.status_code, 200)
            # Check that the result shows zero members in office
            self.assertEqual(response.get_json()["total"], 0)
            self.assertEqual(response.get_json()["details"], [])

    # Test for HR view with a populated dataset
    def test_hr_view_success(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[{"staff_name": "John Doe", "Request_Status": "Approved"}]):
            # Mock the main SQL query response
            mock_execute.return_value.keys.return_value = ["request_ID", "Requester_ID", "Request_Status", "staff_name"]
            mock_execute.return_value.__iter__.return_value = [
                {"request_ID": 1, "Requester_ID": "emp123", "Request_Status": "Approved", "staff_name": "John Doe"}
            ]

            response = self.client.get('/api/hr_view', query_string={"dept": "HR", "month": "7"})
            self.assertEqual(response.status_code, 200)
            # Verify the structure of the response JSON
            self.assertIsInstance(response.get_json(), list)
            self.assertEqual(response.get_json()[0]["staff_name"], "John Doe")
            self.assertEqual(response.get_json()[0]["Request_Status"], "Approved")

    # Test for HR view with no records
    def test_hr_view_empty(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.sql_to_indiv_row', return_value=[]):
            # Mock an empty database response
            mock_execute.return_value.__iter__.return_value = []

            response = self.client.get('/api/hr_view', query_string={"dept": "Legal", "month": "7"})
            self.assertEqual(response.status_code, 200)
            # Confirm that the response is an empty list
            self.assertEqual(response.get_json(), [])



    # Test for HR calendar view when no WFH requests are found
    def test_hr_view_calendar_no_requests(self):
        with patch('app.db.session.execute') as mock_execute, \
             patch('app.calendar_count', return_value={"month": "7", "details": []}):
            # Mocking empty main query response
            mock_execute.return_value.__iter__.return_value = []

            response = self.client.get('/api/hr_view_calendar', query_string={"dept": "Marketing", "month": "7"})
            self.assertEqual(response.status_code, 200)
            # Check that the result has an empty details list
            self.assertEqual(response.get_json()["details"], [])




    # Test for withdrawal when user is not provided
    def test_withdraw_request_no_user(self):
        response = self.client.patch('/withdrawrequest/1/')
        self.assertEqual(response.status_code, 404)  # Expecting 404 due to incorrect route structure

    # Test for unauthorized access when request doesn't belong to the user
    def test_withdraw_request_unauthorized(self):
        with patch('app.db.session.execute') as mock_execute:
            # Mock the SELECT query to simulate no matching request for the user
            mock_execute.return_value.fetchone.return_value = None

            response = self.client.patch('/withdrawrequest/1/999')
            self.assertEqual(response.status_code, 404)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Request not found or you do not have permission to withdraw this request.")

    # Test for withdrawal when request does not exist
    def test_withdraw_request_nonexistent(self):
        with patch('app.db.session.execute') as mock_execute:
            # Mock the SELECT query to return None, simulating a non-existent request
            mock_execute.return_value.fetchone.return_value = None

            response = self.client.patch('/withdrawrequest/999/123')
            self.assertEqual(response.status_code, 404)
            self.assertIn("message", response.get_json())
            self.assertEqual(response.get_json()["message"], "Request not found or you do not have permission to withdraw this request.")


if __name__ == '__main__':
    unittest.main()