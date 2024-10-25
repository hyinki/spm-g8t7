import pytest
import calendar
from datetime import datetime, timedelta,date
from unittest.mock import patch
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.Calender_DT_Processing import calendar_count, sql_to_indiv_row, tally_people_in_office,delete_person
import json

def test_calendar_no_wfh_requests():
    request_dict = []
    total_people = 10
    month = 7
    result = calendar_count(request_dict, total_people, month)
    expected = {i: {"AM": 0, "PM": 0, "wholeday": 0} for i in range(1, 32)}
    assert result == expected

def test_calendar_single_wfh_request():
    request_dict = [
        {
            'request_ID': 1,
            'start_date': datetime(2024, 7, 24),
            'end_date': datetime(2024, 7, 24),
            'Requester_ID': 150192,
            'Requester_Supervisor': 151408,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'AM',
            'Thursday': 'NULL',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        }
    ]
    total_people = 10
    month = 7
    result = calendar_count(request_dict, total_people, month)
    expected = {i: {"AM": 0, "PM": 0, "wholeday": 0} for i in range(1, 32)}
    expected[24]["AM"] = 1
    assert result == expected

def test_calendar_multiple_wfh_requests():
    # First scenario: Multiple WFH requests within the same month
    request_dict = [
        {
            'request_ID': 1,
            'start_date': datetime(2024, 7, 24),
            'end_date': datetime(2024, 7, 24),
            'Requester_ID': 150192,
            'Requester_Supervisor': 151408,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'AM',
            'Thursday': 'NULL',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        },
        {
            'request_ID': 2,
            'start_date': datetime(2024, 7, 25),
            'end_date': datetime(2024, 7, 25),
            'Requester_ID': 150193,
            'Requester_Supervisor': 151409,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'NULL',
            'Thursday': 'PM',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        }
    ]
    total_people = 10
    month = 7
    result = calendar_count(request_dict, total_people, month)
    expected = {i: {"AM": 0, "PM": 0, "wholeday": 0} for i in range(1, 32)}
    expected[24]["AM"] = 1
    expected[25]["PM"] = 1
    assert result == expected

    # Second scenario: WFH requests spanning multiple months
    request_dict = [
        {
            'request_ID': 1,
            'start_date': datetime(2024, 6, 30),
            'end_date': datetime(2024, 7, 2),
            'Requester_ID': 150192,
            'Requester_Supervisor': 151408,
            'Monday': 'PM',
            'Tuesday': 'Whole Day',
            'Wednesday': 'NULL',
            'Thursday': 'NULL',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'AM',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        }
    ]
    total_people = 10
    month = 7
    result = calendar_count(request_dict, total_people, month)
    expected = {i: {"AM": 0, "PM": 0, "wholeday": 0} for i in range(1, 32)}
    expected[1]["PM"] = 1
    expected[2]["wholeday"] = 1
    assert result == expected

def test_calendar_overlapping_wfh_requests():
    request_dict = [
        {
            'request_ID': 1,
            'start_date': datetime(2024, 7, 24),
            'end_date': datetime(2024, 7, 24),
            'Requester_ID': 150192,
            'Requester_Supervisor': 151408,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'AM',
            'Thursday': 'NULL',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        },
        {
            'request_ID': 2,
            'start_date': datetime(2024, 7, 24),
            'end_date': datetime(2024, 7, 24),
            'Requester_ID': 150193,
            'Requester_Supervisor': 151409,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'AM',
            'Thursday': 'NULL',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0
        }
    ]
    total_people = 10
    month = 7
    result = calendar_count(request_dict, total_people, month)
    expected = {i: {"AM": 0, "PM": 0, "wholeday": 0} for i in range(1, 32)}
    expected[24]["AM"] = 2
    assert result == expected

def test_sql_to_indiv_row():
    request_dict = [
        {
            'request_ID': 30,
            'start_date': date(2024, 10, 25),
            'end_date': date(2024, 10, 25),
            'Requester_ID': 140894,
            'Requester_Supervisor': 140001,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'NULL',
            'Thursday': 'NULL',
            'Friday': 'AM',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0,
            'staff_name': 'Rahim Khalid'
        },
        {
            'request_ID': 31,
            'start_date': date(2024, 10, 31),
            'end_date': date(2024, 10, 31),
            'Requester_ID': 140894,
            'Requester_Supervisor': 140001,
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'NULL',
            'Thursday': 'PM',
            'Friday': 'NULL',
            'Saturday': 'NULL',
            'Sunday': 'NULL',
            'Request_Status': 'Approved',
            'cloudinary_link': None,
            'repeating': 0,
            'staff_name': 'Rahim Khalid'
        }
    ]
    selected_month = 10  # October

    result = sql_to_indiv_row(request_dict, selected_month)
    
    expected = [
        {'Date': date(2024, 10, 25), 'Timeblock': 'AM', 'staff_name': 'Rahim Khalid'},
        {'Date': date(2024, 10, 31), 'Timeblock': 'PM', 'staff_name': 'Rahim Khalid'}
    ]
    
    assert result == expected

def test_sql_to_indiv_row_empty():
    request_dict = []
    selected_month = 10  # October

    result = sql_to_indiv_row(request_dict, selected_month)
    
    expected = []
    
    assert result == expected


def test_tally_no_wfh_requests():
    staff_fullname_dict = [
        {'staff_name': 'Susan Goh'},{'staff_name': 'Janice Chan'},{'staff_name': 'Mary Teo'}]
    approved_wfh_requests = []
    month = 10  # October

    result = tally_people_in_office(staff_fullname_dict, approved_wfh_requests, month)
    
    total_days_in_month = calendar.monthrange(2024, month)[1]
    expected = {
        date(2024, month, day).isoformat(): {
            "AM": ['Susan Goh','Janice Chan','Mary Teo'],
            "PM": ['Susan Goh','Janice Chan','Mary Teo'],
            "Whole Day": ['Susan Goh','Janice Chan','Mary Teo']
        } for day in range(1, total_days_in_month + 1)
    }
    print("ze output is : ", json.dumps(expected, indent=4))
    print("ze result is : ", json.dumps(result, indent=4), " finished xd")
    assert json.dumps(result, indent=4) == json.dumps(expected, indent=4)

def test_tally_multiple_wfh_request():
    staff_fullname_dict = [
        {'staff_name': 'Susan Goh'}, {'staff_name': 'Janice Chan'}
    ]
    approved_wfh_requests = [
        {
            'start_date': date(2024, 10, 25),
            'end_date': date(2024, 10, 25),
            'staff_name': 'Susan Goh',
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'NULL',
            'Thursday': 'NULL',
            'Friday': 'AM',
            'Saturday': 'NULL',
            'Sunday': 'NULL'
        },
                {
            'start_date': date(2024, 10, 25),
            'end_date': date(2024, 10, 25),
            'staff_name': 'Janice Chan',
            'Monday': 'NULL',
            'Tuesday': 'NULL',
            'Wednesday': 'NULL',
            'Thursday': 'NULL',
            'Friday': 'PM',
            'Saturday': 'NULL',
            'Sunday': 'NULL'
        }
    ]
    month = 10  # October

    result = tally_people_in_office(staff_fullname_dict, approved_wfh_requests, month)
    
    total_days_in_month = calendar.monthrange(2024, month)[1]
    expected = {
        date(2024, month, day).isoformat(): {
            "AM": ['Janice Chan'] if day == 25 else ['Susan Goh', 'Janice Chan'],
            "PM": ['Susan Goh']if day == 25 else ['Susan Goh', 'Janice Chan'],
            "Whole Day": [] if day == 25 else ['Susan Goh', 'Janice Chan']
        } for day in range(1, total_days_in_month + 1)
    }
    print("ze output is : ", json.dumps(expected, indent=4))
    print("ze result is : ", json.dumps(result, indent=4), " finished xd")
    assert json.dumps(result, indent=4) == json.dumps(expected, indent=4)

# def test_tally_multiple_wfh_requests():
#     staff_fullname_dict = [
#         {'staff_name': 'Susan Goh'}, {'staff_name': 'Janice Chan'}, {'staff_name': 'Mary Teo'},
#         {'staff_name': 'Oliva Lim'}, {'staff_name': 'Emma Heng'}, {'staff_name': 'Charlotte Wong'},
#         {'staff_name': 'Amelia Ong'}, {'staff_name': 'Eva Yong'}, {'staff_name': 'Liam The'},
#         {'staff_name': 'Noah Ng'}, {'staff_name': 'Oliver Tan'}, {'staff_name': 'William Fu'},
#         {'staff_name': 'James Tong'}
#     ]
#     approved_wfh_requests = [
#         {
#             'start_date': date(2024, 10, 25),
#             'end_date': date(2024, 10, 25),
#             'staff_name': 'Susan Goh',
#             'Monday': 'NULL',
#             'Tuesday': 'NULL',
#             'Wednesday': 'NULL',
#             'Thursday': 'NULL',
#             'Friday': 'AM',
#             'Saturday': 'NULL',
#             'Sunday': 'NULL'
#         },
#         {
#             'start_date': date(2024, 10, 31),
#             'end_date': date(2024, 10, 31),
#             'staff_name': 'Mary Teo',
#             'Monday': 'NULL',
#             'Tuesday': 'NULL',
#             'Wednesday': 'NULL',
#             'Thursday': 'PM',
#             'Friday': 'NULL',
#             'Saturday': 'NULL',
#             'Sunday': 'NULL'
#         }
#     ]
#     month = 10  # October

#     result =tally_people_in_office(staff_fullname_dict, approved_wfh_requests, month)
    
#     total_days_in_month = calendar.monthrange(2024, month)[1]
#     expected = {
#         date(2024, month, day).isoformat(): {
#             "AM": ['Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'] if day == 25 else ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'],
#             "PM": ['Susan Goh', 'Janice Chan', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'] if day == 31 else ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'],
#             "Whole Day": ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong']
#         } for day in range(1, total_days_in_month + 1)
#     }
    
#     assert result == expected

# def test_tally_wfh_requests_spanning_multiple_days():
#     staff_fullname_dict = [
#         {'staff_name': 'Susan Goh'}, {'staff_name': 'Janice Chan'}, {'staff_name': 'Mary Teo'},
#         {'staff_name': 'Oliva Lim'}, {'staff_name': 'Emma Heng'}, {'staff_name': 'Charlotte Wong'},
#         {'staff_name': 'Amelia Ong'}, {'staff_name': 'Eva Yong'}, {'staff_name': 'Liam The'},
#         {'staff_name': 'Noah Ng'}, {'staff_name': 'Oliver Tan'}, {'staff_name': 'William Fu'},
#         {'staff_name': 'James Tong'}
#     ]
#     approved_wfh_requests = [
#         {
#             'start_date': date(2024, 10, 29),
#             'end_date': date(2024, 10, 31),
#             'staff_name': 'Susan Goh',
#             'Monday': 'NULL',
#             'Tuesday': 'PM',
#             'Wednesday': 'AM',
#             'Thursday': 'AM',
#             'Friday': 'NULL',
#             'Saturday': 'NULL',
#             'Sunday': 'NULL'
#         }
#     ]
#     month = 10  # October

#     result = CalendarProcessor.tally_people_in_office(staff_fullname_dict, approved_wfh_requests, month)
    
#     total_days_in_month = calendar.monthrange(2024, month)[1]
#     expected = {
#         date(2024, month, day).isoformat(): {
#             "AM": ['Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'] if day in [29, 30, 31] else ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'],
#             "PM": ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'] if day in [29, 30] else ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong'],
#             "Whole Day": ['Susan Goh', 'Janice Chan', 'Mary Teo', 'Oliva Lim', 'Emma Heng', 'Charlotte Wong', 'Amelia Ong', 'Eva Yong', 'Liam The', 'Noah Ng', 'Oliver Tan', 'William Fu', 'James Tong']
#         } for day in range(1, total_days_in_month + 1)
#     }
    
#     assert result == expected

