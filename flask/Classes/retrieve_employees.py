from flask import render_template


def retrieve_employees(Employees):
    """Retrieve and display all employees."""
    employees_list = Employees.get_all()  # Retrieve all employees from the database
    return render_template('employees.html', employees=employees_list)  # Render the employees in the template