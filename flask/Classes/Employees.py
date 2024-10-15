from .Database import db  # Import the shared db instance
from flask import session
from sqlalchemy import text
class Employees(db.Model):
    __tablename__ = 'employee_list'  # Ensure this matches your actual table name

    Staff_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Position = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.Integer,db.ForeignKey('employee_list.Staff_ID'), nullable=True)
    User_Password = db.Column(db.String(1024),nullable=True)
    Role = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return f'<employee_list {self.Staff_FName} {self.Staff_LName}>'
    @property
    def is_authenticated(self):
        return True  # Always return True for this example

    @property
    def is_active(self):
        return True  # Adjust based on your application's logic

    @staticmethod
    def get_by_id(staff_id):
        """Retrieve a specific employee by their Staff_ID."""
        return Employees.query.get(staff_id)

    def get_role(role):
        if(role==1):
            return "HR"
        if (role==2):
            return "Staff"
        if(role==3):
            return "Manager"

    @staticmethod
    def check_pword(staff_id):
        
        user = Employees.query.get(staff_id)
        # print(staff_id)
        # If the user exists, return their password hash
        if user:
            
            session['employee_id'] = user.Staff_ID
            session['name']= user.Staff_FName
            session['role'] = user.Role
            session['dept'] = user.Dept
            session['supervisor']=user.Reporting_Manager
            session['email']=user.Email
            session['position']=user.Position
            #the following is code to check if the user is a manager himself/herself
            sql = text("Select Count(Staff_ID) from employee_list where Reporting_Manager =" + str(session['employee_id']))
            result = db.session.execute(sql)
            session['managecount'] = result.scalar()
            return user.User_Password
        else:
            return "nope"


    @staticmethod
    def get_all():
        """Retrieve all employees from the database."""
        return Employees.query.all()
     