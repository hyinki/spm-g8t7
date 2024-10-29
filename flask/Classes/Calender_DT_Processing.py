from datetime import datetime, timedelta, date
import calendar


#trial_total_people = 10
#month = 7
#Trial_dict = [{'request_ID': 28, 'start_date': datetime.date(2024, 10, 29), 'end_date': datetime.date(2024, 10, 31), 'Requester_ID': 140002, 'Requester_Supervisor': 140894, 'Monday': 'NULL', 'Tuesday': 'PM', 'Wednesday': 'AM', 'Thursday': 'AM', 'Friday': 'NULL', 'Saturday': 'NULL', 'Sunday': 'NULL', 'Request_Status': 'Approved', 'cloudinary_link': None, 'repeating': 0}, {'request_ID': 29, 'start_date': datetime.date(2024, 10, 25), 'end_date': datetime.date(2024, 10, 25), 'Requester_ID': 140004, 'Requester_Supervisor': 140894, 'Monday': 'NULL', 'Tuesday': 'NULL', 'Wednesday': 'NULL', 'Thursday': 'NULL', 'Friday': 'PM', 'Saturday': 'NULL', 'Sunday': 'NULL', 'Request_Status': 'Approved', 'cloudinary_link': None, 'repeating': 0}]

def calendar_count(request_dict, total_people, month):
    print(request_dict)
    processed_dict_for_jsonify = {}
    processed_dict_for_jsonify_2 = {}
    #print(total_people)
    #print(month)
    total_days_in_current_month = calendar.monthrange(2024, int(month))[1]
    #print("Month :",month," has ",total_days_in_current_month," days")
    total_days_for_ranging = total_days_in_current_month + 1

    # i in range starts with 0 and ends at the number before the end, so add 1 for the range to get a dict with the days.
    for i in range(total_days_for_ranging):
        if i != 0:
            the_day = datetime(2024, int(month), i)
            processed_dict_for_jsonify[the_day] = total_people
            processed_dict_for_jsonify_2[i] = {"AM":0, "PM":0, "wholeday":0}
    #print(processed_dict_for_jsonify)
    #print(processed_dict_for_jsonify_2)
    for row in request_dict:
        #print(row)
        start_date = row['start_date']
        end_date = row['end_date']
        #Create end_date_plus_one so it takes into account the last day.
        end_date_plus_one = end_date + timedelta(days=1)
        #print(start_date, end_date)
        if start_date.month <= int(month) and end_date.month >= int(month):
                while start_date != end_date_plus_one:
                    #Added this line of code to take into account recurring arrangements over the course of multiple months. Since the page only displays for 1 month
                    #This will push the start_date until it the start of the selected month
                    if start_date.month < int(month):
                        start_date += timedelta(days = 1)
                        continue
                    #In the event the end date is later then end of the month, break the loop after the start date is greater then the month selected.
                    if start_date.month > int(month):
                        break
                    current_day_name = start_date.strftime("%A")
                    current_day_status = row[current_day_name]
                    if current_day_status == "AM" or current_day_status == "PM" or current_day_status == "Whole Day":
                         day = start_date.day
                         if current_day_status == "Whole Day":
                              current_day_status = "wholeday"
                         #print(day, current_day_name)
                         #print(processed_dict_for_jsonify_2[day][current_day_status])
                         processed_dict_for_jsonify_2[day][current_day_status] = processed_dict_for_jsonify_2[day][current_day_status] + 1
                    #print(start_date)
                    start_date += timedelta(days = 1)

    #print(processed_dict_for_jsonify_2)

    #for date in processed_dict_for_jsonify:
        #print(date)
    return processed_dict_for_jsonify_2



#print(calendar_count(Trial_dict, trial_total_people, month))

def sql_to_indiv_row(request_dictionary, month):
    returned_array = []
    for requests in request_dictionary:
        start_date = requests['start_date']
        end_date = requests['end_date']
        end_date_plus_one = end_date + timedelta(days=1)
        print("This is the start date and end date", start_date, end_date)
        while start_date != end_date_plus_one:
            #Added this line of code to take into account recurring arrangements over the course of multiple months. Since the page only displays for 1 month
            #This will push the start_date until it the start of the selected month
            if start_date.month < int(month):
                start_date += timedelta(days = 1)
                continue
            #In the event the end date is later then end of the month, break the loop after the start date is greater then the month selected.
            if start_date.month > int(month):
                break
            appended_dictionary = {}
            current_day_name = start_date.strftime("%A")
            day_status = requests[current_day_name]
            print("Current day :", current_day_name, "Day Status:", day_status)
            staff_name = requests["staff_name"]
            appended_dictionary['Date'] = start_date
            appended_dictionary['Timeblock'] = day_status
            appended_dictionary['staff_name'] = staff_name
            returned_array.append(appended_dictionary)
            start_date += timedelta(days=1)
    return returned_array


def tally_people_in_office(staff_fullname_dict, approved_wfh_requests, month):
    array_of_staff_name = []
    current_time = datetime.now()
    current_year = current_time.year
    dict_of_dicts = {}
    date_checking = []

    total_days_in_current_month = calendar.monthrange(2024, int(month))[1]
    #print("This print statement is to check that the function is receiving the appropriate dictionaries",staff_fullname_dict, approved_wfh_requests, month)

    #convert the array of dicts into a an array of staff names reporting to a certain manager
    for staff in staff_fullname_dict:
        array_of_staff_name.append(staff['staff_name'])

    #print("Checking if the dictionary is returned to an array for assignment :", array_of_staff_name)

    #print("There are :", total_days_in_current_month, "days in :", month, "month")

    for i in range(total_days_in_current_month+1):
        if i == 0:
            pass
        else:
            thedate = date(current_year, int(month), i)
            date_checking.append(thedate)
            inside_date_dict = {}
            inside_date_dict["AM"] = array_of_staff_name
            inside_date_dict["PM"] = array_of_staff_name
            inside_date_dict["Whole Day"] = array_of_staff_name
            #print("Check the inside_date_dict dictionary: ", inside_date_dict)
            #print("the keys to the dict", inside_date_dict.keys())
            dict_of_dicts[thedate] = inside_date_dict

    # Iterate through the WFH requests and pull out the name in the specific timeslot
    #print("This is the list of approved wfh_requests: ",approved_wfh_requests)
    for indiv_request in approved_wfh_requests:
        start_date = indiv_request["start_date"]
        end_date = indiv_request["end_date"]
        end_date_plus_one = end_date + timedelta(days=1)
        staff_name = indiv_request["staff_name"]
        while start_date !=  end_date_plus_one:
            if start_date.month < int(month):
                start_date += timedelta(days = 1)
                continue
            #In the event the end date is later then end of the month, break the loop after the start date is greater then the month selected.
            if start_date.month > int(month):
                break
            current_day_name = start_date.strftime("%A")
            day_status = indiv_request[current_day_name]
            #print("WFH Occurence of the day itself: ",current_day_name, day_status, "This is staff name: ", staff_name, "This is date: ", start_date)
            delete_person(dict_of_dicts, start_date, day_status, staff_name)
            start_date += timedelta(days=1)

    # print("This is the dictionary after delete: ", dict_of_dicts)
    #Convert back the date keys to strings with isoformat() for jsonify to work.
    returned_dict = {}
    for key in dict_of_dicts:
        new_key = key.isoformat()
        returned_dict[new_key] = dict_of_dicts[key]


    #print("This is the returned dict: ",returned_dict)
    #print("Check if the dict_of_dicts contains the date as a key linked to a timeblock with staff name :", dict_of_dicts)
    #print("Check the WFH requests: ", approved_wfh_requests)
    #print("This is to check if all dates have been properly created by python: ", date_checking)

    return returned_dict





#Trial people delete
#data = {
#    "11/04/24": {"AM": ["Michael", "Charles"], "PM": ["John", "Mark", "Michael"], "Whole Day": ["John", "Mark", "Michael"]},
#    "12/04/24": {"AM": ["Michael", "Alice"], "PM": ["Mark", "Michael"], "Whole Day": ["John", "Mark", "Michael"]}
#}

def delete_person(default_dictionary, date, timeblock, name_to_delete):
    if date in default_dictionary:
        if timeblock == "Whole Day":
            for tb in ["AM", "PM"]:
                if tb in default_dictionary[date]:
                    default_dictionary[date][tb] = [name for name in default_dictionary[date][tb] if name != name_to_delete]
        if timeblock in default_dictionary[date]:
            # Remove name from the specified time block
            default_dictionary[date][timeblock] = [name for name in default_dictionary[date][timeblock] if name != name_to_delete]
            # Always remove from "Whole Day"
            default_dictionary[date]["Whole Day"] = [name for name in default_dictionary[date]["Whole Day"] if name != name_to_delete]

# Usage
#delete_person(data, "11/04/24", "PM", "Michael")
#delete_person(data, "12/04/24", "AM", "Michael")

#print("Delete person test:", data)
