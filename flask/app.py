from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Classes.Database import db  
from Classes.Employees import Employees
from Classes.Wfh_Request import WFHRequests
from Classes.Login import Login
from werkzeug.security import check_password_hash
from sqlalchemy import text
from Classes.Calender_DT_Processing import calendar_count, sql_to_indiv_row
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/spmtest1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Set a random secret key for security
db.init_app(app)  # Initialize the db with the Flask app
CORS(app, supports_credentials=True)

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
    input_password = request.json.get('password')  # Get the password from the JSON body
    print(user_id)
    print("password is "+ input_password)
    # Create an instance of Login to check user credentials
    login1 = Login()
    if login1.check_user_password(user_id, input_password):


        # Optionally return the user's role or other information
        user =Employees.query.get(user_id)
        user_role = Employees.get_role(user.Role)
        user_name =user.Staff_FName
        return jsonify({
            "user_name": user_name,
            "role": user_role,
            "dept": user.Dept,
            "supervisor": user.Reporting_Manager,
            "email": user.Email,
            "position": user.Position,
            "userid": user.Staff_ID,
            "msg": "Login successful."
        }), 200
    else:
        return jsonify({"msg": "Invalid credentials."}), 401  # Return error if login fails

# @app.route("/session", methods=['GET'])
# @login_required
# def get_session():
#     name = session.get('name')  # Get the name from the session
#     return jsonify({"name": name}), 200


# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('login_route'))  # Redirect to login page

@app.route("/homepage")
@login_required
def homepage():
    staff_name=session['employee_id'] 
    session['name']
    session['dept'] 
    session['supervisor']
    session['email']
    return render_template("homepage.html")


# Define a protected route
@app.route("/test_employees")
@login_required 
def retrieve_employees():
    """Retrieve and display all employees."""
    emp_name=session['name']
    #employees_list = Employees.get_all()  # Retrieve all employees from the database
    sql = text("SELECT * FROM employee_list where Reporting_Manager =" + str(session['supervisor']))
    employees_list = db.session.execute(sql)
    return render_template('employees.html', employees=employees_list, emp_name=emp_name)  # Render the employees in the template


@app.route("/wfh_request")
@login_required
def wfh_request():
    emp_name=session['name']
    emp_sup=session['supervisor']
    emp_id=session['employee_id']
    return render_template("wfh_request.html", emp_name=emp_name, emp_sup=emp_sup,emp_id=emp_id)

@app.route("/submit_wfh_request", methods=["POST"])
@login_required
def submit_wfh_request():
    """Submit a new WFH request to the database."""
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    monday = request.form['monday']
    tuesday = request.form['tuesday']
    wednesday = request.form['wednesday']
    thursday = request.form['thursday']
    friday = request.form['friday']
    saturday = request.form['saturday']
    sunday = request.form['sunday']
    requester_id = request.form['requester_id']
    requester_supervisor = request.form['requester_supervisor']
    request_status = request.form['request_status']

    # Create a new WFH request instance
    new_request = WFHRequests(
        Requester_ID=requester_id,
        Requester_Supervisor=requester_supervisor,
        Request_Status=request_status,
        start_date = start_date,
        end_date = end_date,
        Monday = monday,
        Tuesday = tuesday,
        Wednesday = wednesday,
        Thursday = thursday,
        Friday = friday,
        Saturday = saturday,
        Sunday = sunday
    )

    try:
        # Add the new request to the session and commit it to the database
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('success'))  # Redirect to the success page
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return redirect(url_for('failure'))  # Redirect to the failure page

@app.route("/wfh_viewer")
@login_required
def retrieve_wfh():
    """Retrieve and display all wfh."""
    wfh_list = WFHRequests.get_all()  # Retrieve all employees from the database
    return  render_template('WFH.html',wfh_li=wfh_list) # Render the employees in the 


@app.route("/update_wfh_request/<int:request_id>", methods=["GET", "POST"])
@login_required
def update_wfh_request(request_id):
    """Update a WFH request."""
    wfh_request = WFHRequests.get_by_id(request_id)
    if request.method == "POST":
        # Update the WFH request with the form data
        selected_date = request.form['selected_date']
        day_of_week = request.form['day_of_week']
        requester_id = request.form['requester_id']
        requester_supervisor = request.form['requester_supervisor']
        request_status = request.form['request_status']

        success = WFHRequests.update_request(request_id, selected_date, day_of_week, requester_id, requester_supervisor, request_status)
        if success:
            return redirect(url_for('wfh_request'))  # Redirect to the WFH requests page
        else:
            return redirect(url_for('failure'))  # Redirect to the failure page if update fails

    return render_template('update_wfh_request.html', wfh_request=wfh_request)


#Note, this function most likely can delete, with the homepage button reroute to manager view, was trialling some session based logic for handling data.
#Might try to integrate a function where if session["managecount"] == 0 redirect back to homepage since no need to approve anything.
@app.route("/manager_view_processing")
def retrieve_staff_wfh_for_manager():
    #sql = text("Select * from WFH_requests where Requester_Supervisor = " + str(session['employee_id']) + " AND Request_Status = 'Pending'")
    #processed = db.session.execute(sql)
    #turn the object into a list
    #pending_list = processed.fetchall()
    #session["manager_pending_list"] = pending_list
    return redirect(url_for('managerview'))

@app.route("/managerview")
def managerview():
    sql = text("Select * from WFH_requests where Requester_Supervisor = " + str(session['employee_id']) + " AND Request_Status = 'Pending'")
    processing = db.session.execute(sql) 
    #list_of_pending_requests = session.get('manager_pending_list', [])   
    return render_template('managerview.html', requests=processing)


@app.route("/viewownrequests")
@login_required
def viewownrequests():
    sql = text("Select * from WFH_requests where Requester_ID = " + str(session['employee_id']))
    sqldonepog = db.session.execute(sql)
    return render_template('viewownrequests.html', ownreq = sqldonepog)

@app.route("/managerview_active")
@login_required
def managerview_active():
    sql = text("Select * from WFH_requests where Requester_Supervisor = " + str(session['employee_id']) + " AND Request_Status = 'Approved'")
    sql_processed = db.session.execute(sql)  
    return render_template('managerview_active.html', active=sql_processed)

@app.route("/org_view")
@login_required
def org_view():
    sql = text("Select * from WFH_requests where Request_Status = 'Approved'")
    sql_processed = db.session.execute(sql)  
    return render_template('org_view.html', org = sql_processed)

@app.route("/api/manager_view", methods=['GET'])
def retrieve_manager_view():
    #user_role = request.cookies.get("userRole")
    #print(user_role)
    #user_id = request.cookies.get("username")
    #print(user_id)
    user_id_2_the_electric_boogaloo = request.cookies.get("userid")
    #print(user_id_2_the_electric_boogaloo)
    #sql_stringie = "Select * from WFH_requests where Requester_Supervisor = "+str(user_id_2_the_electric_boogaloo)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql_stringie = "select w.*, concat(e.Staff_FName, ' ', e.Staff_LName) as staff_name from wfh_requests w left join employee_list e on w.Requester_ID = e.Staff_ID where w.Request_Status = 'Approved' and w.Requester_Supervisor ="+str(user_id_2_the_electric_boogaloo)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    sql_processed_3 = sql_to_indiv_row(sql_processed_2)
    print(sql_processed_2)
    print(sql_processed_3)
    return jsonify(sql_processed_3)

@app.route("/api/manager_view_calendar", methods=['GET'])
def retrieve_manager_calendar_data():
    user_id_2_the_electric_boogaloo = request.cookies.get("userid")
    selected_month = request.args.get('month')
    print(selected_month)
    #print(user_id_2_the_electric_boogaloo)
    sql_stringie = "Select * from WFH_requests where Requester_Supervisor = "+str(user_id_2_the_electric_boogaloo)+" and month(start_date) <="+str(selected_month)+" and month(end_date) >= "+str(selected_month)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)  
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    #print(sql_processed_2)
    sql_2 = text("Select Count(Staff_ID) from employee_list where Reporting_Manager =" + str(user_id_2_the_electric_boogaloo))
    result = db.session.execute(sql_2)
    total_managed_people = result.scalar()
    returned_stuff = calendar_count(sql_processed_2, total_managed_people, selected_month)
    print(type(returned_stuff))
    return jsonify(returned_stuff)


@app.route("/api/individual_view", methods=['GET'])
def retrieve_individual_view():
    user_id = request.cookies.get("userid")
    sql_stringie = "Select * from WFH_requests where Requester_ID = "+str(user_id)
    sql = text(sql_stringie)
    sql_processed = db.session.execute(sql)
    column_names = sql_processed.keys()
    sql_processed_2 = [dict(zip(column_names, row)) for row in sql_processed]
    print(sql_processed_2)
    return jsonify(sql_processed_2)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)