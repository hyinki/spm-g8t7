from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Classes.Database import db  
from Classes.Employees import Employees
from Classes.Wfh_Request import WFHRequests
from Classes.Login import Login
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/spmtest1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Set a random secret key for security
db.init_app(app)  # Initialize the db with the Flask app
CORS(app)

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
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        user_id = request.form.get('user_ID')
        input_password = request.form.get('password')

        # Create an instance of Login to check user credentials
        login1 = Login()
        if login1.check_user_password(user_id, input_password):
            user = User()
            user.id = user_id  # or get the user ID from the Employees model if necessary
            login_user(user)  # Log in the user
            return redirect(url_for('homepage'))  # Redirect to the employees page
        else:
            return render_template("Login.html", error="Invalid credentials")  # Show an error if login fails
    return render_template("Login.html")  # Display the login form

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('login_route'))  # Redirect to login page

@app.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html")


# Define a protected route
@app.route("/test_employees")
@login_required  # Protect this route
def retrieve_employees():
    """Retrieve and display all employees."""
    emp_name=session['name']
    employees_list = Employees.get_all()  # Retrieve all employees from the database
    return render_template('employees.html', employees=employees_list, emp_name=emp_name)  # Render the employees in the template


@app.route("/wfh_request")
def wfh_request():
    emp_name=session['name']
    emp_sup=session['supervisor']
    emp_id=session['employee_id']
    return render_template("wfh_request.html", emp_name=emp_name, emp_sup=emp_sup,emp_id=emp_id)

@app.route("/submit_wfh_request", methods=["POST"])
def submit_wfh_request():
    """Submit a new WFH request to the database."""
    selected_date = request.form['selected_date']
    day_of_week = request.form['day_of_week']
    requester_id = request.form['requester_id']
    requester_supervisor = request.form['requester_supervisor']
    request_status = request.form['request_status']

    # Create a new WFH request instance
    new_request = WFHRequests(
        selected_date=selected_date,
        day_of_week=day_of_week,
        Requester_ID=requester_id,
        Requester_Supervisor=requester_supervisor,
        Request_Status=request_status
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
def retrieve_wfh():
    """Retrieve and display all wfh."""
    wfh_list = WFHRequests.get_all()  # Retrieve all employees from the database
    return  render_template('WFH.html',wfh_li=wfh_list) # Render the employees in the 


@app.route("/update_wfh_request/<int:request_id>", methods=["GET", "POST"])
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




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)