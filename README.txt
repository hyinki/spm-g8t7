==================
INSTALLATION GUIDE
==================

(1) set up and run a WAMP or MAMP server

(2) Run the sql script


(3) Open sql workbench. Under schema, select spmtest1, employee_list table, right click and select table data import wizard. Import employeeupdated.csv 

(3) Install the following, do:

	   python -m pip install flask
	   python -m pip install flask_cors
	   python -m pip install Flask-SQLAlchemy
	   python -m pip install mysql-connector-python
	   Python -m pip install flask_login
		

(5) in the 'flask' directory, run "python app.py" in a terminal.

	--> if it fails to run, open app.py in an editor and check that
		the DB connection string is correct (e.g. port 3306 vs. 8889)


