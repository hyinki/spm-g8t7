from datetime import datetime, timedelta
import calendar


#trial_total_people = 10
#month = 7
#Trial_dict = [{'request_ID': 1, 'start_date': datetime.date(2024, 7, 24), 'end_date': datetime.date(2024, 7, 29), 'Requester_ID': 150192, 'Requester_Supervisor': 151408, 'Monday': 'AM', 'Tuesday': 'AM', 'Wednesday': 'AM', 'Thursday': 'PM', 'Friday': 'AM', 'Saturday': 'PM', 'Sunday': 'Whole Day', 'Request_Status': 'Pending'}, {'request_ID': 2, 'start_date': datetime.date(2024, 7, 24), 'end_date': datetime.date(2024, 7, 29), 'Requester_ID': 150192, 'Requester_Supervisor': 151408, 'Monday': 'AM', 'Tuesday': 'AM', 'Wednesday': 'AM', 'Thursday': 'PM', 'Friday': 'AM', 'Saturday': 'PM', 'Sunday': 'Whole Day', 'Request_Status': 'Approved'}, {'request_ID': 4, 'start_date': datetime.date(2024, 7, 24), 'end_date': datetime.date(2024, 7, 29), 'Requester_ID': 150192, 'Requester_Supervisor': 151408, 'Monday': 'AM', 'Tuesday': 'AM', 'Wednesday': 'AM', 'Thursday': 'PM', 'Friday': 'AM', 'Saturday': 'PM', 'Sunday': 'Whole Day', 'Request_Status': 'Pending'}]

def calendar_count(request_dict, total_people, month):
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
        #print(start_date, end_date)
        if start_date.month <= int(month) and end_date.month >= int(month):
                while start_date != end_date:
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

def sql_to_indiv_row(request_dictionary):
    returned_array = []
    for requests in request_dictionary:
        start_date = requests['start_date']
        end_date = requests['end_date']
        print("This is the start date and end date", start_date, end_date)
        while start_date != end_date:
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