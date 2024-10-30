from flask import Flask, request, jsonify,  session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Classes.Database import db  
from Classes.Employees import Employees
from Classes.Wfh_Request import WFHRequests
from Classes.Login import Login
from werkzeug.security import check_password_hash
from sqlalchemy import text
from Classes.Calender_DT_Processing import calendar_count, sql_to_indiv_row, tally_people_in_office
import mysql.connector
import os
import cloudinary
import cloudinary.uploader
app = Flask(__name__)


app.config.update(
    SESSION_COOKIE_SECURE=True,      # Required for HTTPS
    SESSION_COOKIE_SAMESITE='None',   # Recommended for security
)

cloudinary.config(
    cloud_name='dofj7bkm3',
    api_key='844945974877343',
    api_secret='kxy0mseU1Qsz5G7UX31WElZ1hts'
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://brandyn:root@34.80.185.149/spmtest1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Set a random secret key for security
db.init_app(app)  # Initialize the db with the Flask app
# CORS(app, supports_credentials=True, origins=["https://spm-g8t7-vue.onrender.com"], allow_headers=["Content-Type", "Authorization","X-staff-ID","X-Role","X-Month","X-Dept"],
#     expose_headers=["Content-Range", "X-Content-Range"])
CORS(app, supports_credentials=True, 
     resources={r"/*": {"origins": '*'}}, 
     allow_headers=["Content-Type", "Authorization", "X-userid", "X-Role", "X-Month", "X-Dept"],
     expose_headers=["Content-Range", "X-Content-Range"])

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_route'  # Redirect to login if not authenticated

# Define User class
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    return Employees.query.get(user_id)

# Route for login
@app.route("/login", methods=["POST"])
def login_route():
    user_id = request.json.get('username')  # Get the user ID from the JSON body
    print(user_id)
    input_password = request.json.get('password') 
    print(input_password) # Get the password from the JSON body
    
    print("password is "+ input_password)
    # Create an instance of Login to check user credentials
    login1 = Login()
    if login1.check_user_password(user_id, input_password):


        # Optionally return the user's role or other information
        user =Employees.query.get(user_id)
        userid=session['employee_id']
        user_role = Employees.get_role(user.Role)
        print(user_role)
        
        return jsonify({
            "user_name": session['name'],
            "role": user_role,
            "dept": session['dept'],
            "supervisor": session['supervisor'],
            "email": session['email'],
            "position": session['position'],
            "userid": session['employee_id'],

            "msg": "Login successful."
        }), 200
    else:
        return jsonify({"msg": "Invalid credentials."}), 401  # Return error if login fails






@app.route("/submit_wfh_request", methods=["POST"])

def submit_wfh_request():

    data = request.get_json()

    start_date = data.get('startDate')
    end_date = data.get('endDate')
    requester_id = data.get('userId')
    requester_supervisor = data.get('supervisor')
    request_status = "pending"  # or however you determine the initial status
    cloudinary_link = data.get('cloudinary_link')
    repeating= data.get('repeating')

    # Get selected days and timeslots
    selected_days = data.get('selectedDays', [])
    # print(selected_days)
    days_dict = {day['day']: day['timeslot'] for day in selected_days}


    # Create a new WFH request instance
    new_request = WFHRequests(
        Requester_ID=requester_id,
        Requester_Supervisor=requester_supervisor,
        Request_Status=request_status,
        start_date = start_date,
        end_date = end_date,
        Cloudinary_link=cloudinary_link,
        Repeating=repeating,
        Monday=days_dict.get('Monday', None),
        Tuesday=days_dict.get('Tuesday', None),
        Wednesday=days_dict.get('Wednesday', None),
        Thursday=days_dict.get('Thursday', None),
        Friday=days_dict.get('Friday', None),
        Saturday=days_dict.get('Saturday', None),
        Sunday=days_dict.get('Sunday', None)
        
        )

    try:
        # Add the new request to the session and commit it to the database
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Request submitted successfully'}), 201
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({'message': 'Failed to submit request'}), 500  # Redirect to the failure page






@app.route("/viewownrequests", methods=['GET'])
def viewownrequests():
    # Retrieve employee_id from cookies

    employee_id = request.cookies.get('userid')
    print(employee_id + " is the employee id")
    print()
    print(session.get('test'))
    

    # Check if 'Staff_ID' exists in the cookies
    if not employee_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401
    
    # Fetch the requests from the database
    sql = text("SELECT * FROM wfh_requests WHERE Requester_ID = :requester_id")
    sqldonepog = db.session.execute(sql, {'requester_id': employee_id}).mappings().all()

    # Convert the SQL result to a list of dictionaries
    requests = [dict(row) for row in sqldonepog]

    # Return the data as JSON
    return jsonify(requests), 200


@app.route("/withdrawrequest/<int:request_id>/<int:userid>", methods=['patch'])

def withdraw_request(request_id, userid):
    # Retrieve employee_id from cookies
    print("Received request to withdraw:", request_id, "for user ID:", userid)
    
    # Assume employee_id comes from the URL for this logic
    employee_id = userid

    print("Employee ID from URL:", employee_id)


    if not employee_id:
        print("User ID is not provided.")
        return jsonify({"status": "failure", "message": "User not logged in"}), 401
    
    # Check if the request belongs to the logged-in user
    sql_check = text("SELECT * FROM wfh_requests WHERE Requester_ID = :requester_id AND request_ID = :request_id")
    result = db.session.execute(sql_check, {'requester_id': employee_id, 'request_id': request_id}).fetchone()

    if not result:
        print("Request not found or user does not have permission.")
        return jsonify({"status": "failure", "message": "Request not found or you do not have permission to withdraw this request."}), 404
    
    # Update the request status to 'Withdrawn'
    sql_update = text("UPDATE wfh_requests SET Request_Status = :status WHERE request_ID = :request_id")
    db.session.execute(sql_update, {'status': 'Withdrawn', 'request_id': request_id})
    db.session.commit()  # Commit the update

    return jsonify({"status": "success", "message": "Request status updated to 'Withdrawn' successfully"}), 200


@app.route("/approve_request", methods=['GET'])
def approve_request():
    try:
        cookie_req_id=request.args.get("request")
        print(cookie_req_id)
        sql_string = "UPDATE wfh_requests SET Request_Status = 'Approved' WHERE Request_ID = :request_id"
        sql = text(sql_string)

            # Execute the SQL statement using parameterized query
        sql_processed = db.session.execute(sql, {"request_id": cookie_req_id})

            # Commit the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({"status": "success", "message": "Request approved"}), 200

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        print(f"Error updating request status: {e}")  # Debugging statement
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route("/reject_request", methods=['GET'])
def reject_request():
    try:
        cookie_req_id=request.args.get("request")
        print(cookie_req_id)
        sql_string = "UPDATE wfh_requests SET Request_Status = 'Rejected' WHERE Request_ID = :request_id"
        sql = text(sql_string)

            # Execute the SQL statement using parameterized query
        sql_processed = db.session.execute(sql, {"request_id": cookie_req_id})

            # Commit the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({"status": "success", "message": "Request rejected"}), 200

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        print(f"Error updating request status: {e}")  # Debugging statement
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/manager_to_approve", methods=['GET'])
def retrieve_manager_approve():

    user_id_2_the_electric_boogaloo = request.cookies.get("userid")
    # print(selected_month)

    sql_stringie =  "SELECT w.*, CONCAT(e.Staff_FName, ' ', e.Staff_LName) AS staff_name FROM wfh_requests w LEFT JOIN employee_list e ON w.Requester_ID = e.Staff_ID WHERE w.Requester_Supervisor ="+ str(user_id_2_the_electric_boogaloo)+" AND w.Request_Status = 'Pending'"
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
   
    print(sql_processed_2)

    return jsonify(sql_processed_2)





@app.route("/api/manager_view", methods=['GET'])
def retrieve_manager_view():
  
    # user_id_2_the_electric_boogaloo = request.cookies.get("userid")
    # selected_month = request.args.get('month')
    #localsetstorage
    print('Manager view user id is ' ,request.headers.get('X-userid'))
    selected_month = request.headers.get('X-Month')
    user_id_2_the_electric_boogaloo = request.headers.get('X-userid')
    print(selected_month, user_id_2_the_electric_boogaloo)
    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and w.Requester_Supervisor ="+str(user_id_2_the_electric_boogaloo)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_processed_3 = sql_to_indiv_row(sql_processed_2, selected_month)
    print(sql_processed_2)
    print(sql_processed_3)
    return jsonify(sql_processed_3)

@app.route("/api/manager_view_calendar", methods=['GET'])
def retrieve_manager_calendar_data():
    user_id_2_the_electric_boogaloo = request.cookies.get("userid")
    selected_month = request.args.get('month')
    print(selected_month)

    sql_stringie = "Select * from wfh_requests where Requester_Supervisor = "+str(user_id_2_the_electric_boogaloo)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)+" and Request_Status = 'Approved';"
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    print("This is sql processed 1 ",sql_processed)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    print("this is the sql processed 2 ",sql_processed_2, " ==finished \n\n")
    sql_2 = text("Select Count(Staff_ID) from employee_list where Reporting_Manager =" + str(user_id_2_the_electric_boogaloo))
    result = db.session.execute(sql_2)
    total_managed_people = result.scalar()
    returned_stuff = calendar_count(sql_processed_2, total_managed_people, selected_month)
    # print("this is the return things, ",returned_stuff,"\n\n\n")
    return jsonify(returned_stuff)


@app.route("/api/individual_view", methods=['GET'])
def retrieve_individual_view():
    user_id = request.cookies.get("userid")
    sql_stringie = "Select * from wfh_requests where Requester_ID = "+str(user_id)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
   
    return jsonify(sql_processed_2)


@app.route("/api/manager_list_in_office", methods=['GET'])
def retrieve_list_in_office():
    user_id = request.cookies.get("userid")
    selected_month = request.args.get('month')

    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and w.Requester_Supervisor ="+str(user_id)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_stringie_2 = "select concat(Staff_Fname, ' ', Staff_LName) as staff_name from employee_list where Reporting_Manager = "+str(user_id)
    sql_2 = text(sql_stringie_2)
    sql_processed_bravo = db.session.execute(sql_2)
    column_names_2 = sql_processed_bravo.keys()
    sql_processed_3 = [dict(zip(column_names_2, row)) for row in sql_processed_bravo]
    print("this is sql 3 for tally ",sql_processed_3 ,"\n\n\n")
    print("this is sql 2 for tally ",sql_processed_2 ,"")
    returned_json = tally_people_in_office(sql_processed_3, sql_processed_2, selected_month)
    print("this is the returned json ",returned_json)
    return jsonify(returned_json)
    

@app.route("/api/view_own_team_schedule", methods=['GET'])
def retrieve_own_team_view():
    response.set_cookie('userRole', 'admin', samesite='None', secure=True)
    response.set_cookie('username', 'example_user', samesite='None', secure=True)
    user_supervisor = request.cookies.get("supervisor")
    print("The user's supervisor is: ",user_supervisor)
    selected_month = request.args.get('month')

    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and (w.Requester_Supervisor ="+str(user_supervisor)+" or w.Requester_ID ="+str(user_supervisor)+") and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_processed_3 = sql_to_indiv_row(sql_processed_2, selected_month)

    return jsonify(sql_processed_3)

@app.route("/api/staff_team_view_calendar", methods=['GET'])
def retrieve_staff_team_calendar_data():
    user_supervisor = request.cookies.get("supervisor")
    selected_month = request.args.get('month')
    print(selected_month)
    #print(user_id_2_the_electric_boogaloo)
    sql_stringie = "Select * from wfh_requests where (Requester_Supervisor = "+str(user_supervisor)+" or Requester_ID = "+str(user_supervisor)+") and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)+" and Request_Status = 'Approved';"
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    #print(sql_processed_2)
    sql_2 = text("Select Count(Staff_ID) from employee_list where (Reporting_Manager =" + str(user_supervisor)+" or Staff_ID = " + str(user_supervisor)+")")
    result = db.session.execute(sql_2)
    total_managed_people = result.scalar()
    returned_stuff = calendar_count(sql_processed_2, total_managed_people, selected_month)
    # print(type(returned_stuff))
    return jsonify(returned_stuff)

@app.route("/api/view_own_team_in_office_list", methods=['GET'])
def retrieve_own_team_in_office_list():
    user_supervisor = request.cookies.get("supervisor")
    selected_month = request.args.get('month')

    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and (w.Requester_Supervisor ="+str(user_supervisor)+" or w.Requester_ID ="+str(user_supervisor)+") and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_stringie_2 = "select concat(Staff_Fname, ' ', Staff_LName) as staff_name from employee_list where (Reporting_Manager = "+str(user_supervisor)+ " or Staff_ID = "+str(user_supervisor)+")"
    sql_2 = text(sql_stringie_2)
    sql_processed_bravo = db.session.execute(sql_2)
    column_names_2 = sql_processed_bravo.keys()
    sql_processed_3 = [dict(zip(column_names_2, row)) for row in sql_processed_bravo]
    returned_json = tally_people_in_office(sql_processed_3, sql_processed_2, selected_month)
    #Comment the following to check the function
    #returned_json = {}
    return jsonify(returned_json)


#hr view
@app.route("/api/view_all_team_in_office_list", methods=['GET'])
def retrieve_all_team_in_office_list():
    selected_dept = request.args.get("dept")
    selected_month = request.args.get('month')
    print("the dept is ",selected_dept)
    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)+" and e.Dept = '"+str(selected_dept)+"'"

    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    print("sql is ", sql_processed_2)
    sql_stringie_2 = "select concat(Staff_Fname, ' ', Staff_LName) as staff_name from employee_list where Dept = '"+str(selected_dept)+"'"
    sql_2 = text(sql_stringie_2)
    print(sql_stringie_2)
    sql_processed_bravo = db.session.execute(sql_2)
    column_names_2 = sql_processed_bravo.keys()
    sql_processed_3 = [dict(zip(column_names_2, row)) for row in sql_processed_bravo]
    returned_json = tally_people_in_office(sql_processed_3, sql_processed_2, selected_month)

    print("it works")
   
    return jsonify(returned_json)


@app.route("/api/hr_view", methods=['GET'])
def retrieve_hr_view():
    selected_dept=request.args.get('dept')
    selected_month = request.args.get('month')
    
    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month) +" and e.Dept = '"+str(selected_dept)+"'"
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_processed_3 = sql_to_indiv_row(sql_processed_2, selected_month)

    return jsonify(sql_processed_3)





#hr calendar
@app.route("/api/hr_view_calendar", methods=['GET'])
def retrieve_dept_calendar_data():
    selected_dept=request.args.get('dept')
    selected_month = request.args.get('month')

    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)+" and e.Dept = '"+str(selected_dept)+"'"
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    #print(sql_processed_2)
    sql_stringie_2 = "select concat(Staff_Fname, ' ', Staff_LName) as staff_name from employee_list where Dept = '"+str(selected_dept)+"'"
    sql_2 = text(sql_stringie_2)
    result = db.session.execute(sql_2)
    total_managed_people = result.scalar()
    returned_stuff = calendar_count(sql_processed_2, total_managed_people, selected_month)

    print(type(returned_stuff))
    return jsonify(returned_stuff)

#cloud testing
@app.route('/basic_api/hello_world', methods=["GET"])
def hello_world():
    return jsonify({"Hello":"World"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)