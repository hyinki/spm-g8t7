from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from Classes.Database import db  
from Classes.Employees import Employees
from Classes.Wfh_Request import WFHRequests
from Classes.Login import Login
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/spmtest1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the db with the Flask app
CORS(app)



# Route for login
@app.route('/login')
def login_route():
    return render_template("Login.html")  # Call the login function from Auth.py


@app.route("/check_pword",methods=['POST'])
def check_pword():
    login1= Login()
    # Get the form data
    user_id = request.form.get('user_ID')
    input_password = request.form.get('password')
    
    # Convert the password to a string (optional)
    input_password = str(input_password)

    # Use the AuthService to check the password
    if login1.check_user_password(user_id, input_password):
        return render_template("employees.html")
    else:
        return render_template("success.html")
    


# Define your routes here
@app.route("/test_employees")
def retrieve_employees():
    """Retrieve and display all employees."""
    employees_list = Employees.get_all()  # Retrieve all employees from the database
    return render_template('employees.html', employees=employees_list)  # Render the employees in the template




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)