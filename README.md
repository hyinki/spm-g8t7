
# Project Setup Guide 

## Installation Steps 

1. **Unzip Project Files**  
   - Open and extract the `SPM-G8T7-main.zip` file.

2. **Set Up Server**  
   - Set up and run a WAMP or MAMP server.

3. **Database Setup**  
   - Run the SQL script provided in the project folder to set up the database.
   - Open SQL Workbench, and under the schema, select `spmtest1`. Find the `employee_list` table, right-click on it, and choose **Table Data Import Wizard** to import `employeeupdated.csv`.

4. **Install Python Dependencies**  
   - In the terminal, navigate to the project directory and install the required Python libraries from `requirements.txt` with:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Flask Application**  
   - In the `flask` directory, run the application with:
     ```bash
     python app.py
     ```
   - If it fails to run, open `app.py` in an editor and verify that the database connection string (e.g., port settings like `3306` vs. `8889`) is correct.

6. **Frontend Setup**  
   - Navigate to the `frontend` folder.
   - Run the following commands to install dependencies and start the development server:
     ```bash
     npm install
     npm run dev
     ```

7. **Access the Application**  
   - Open [http://localhost:5173/](http://localhost:5173/) in your browser to view the application.


## Login Instructions

Once the application is running, you can log in using the following details:

- **Use any `STAFF_ID` from the `employee.csv` file**.
- **Password**: `123456`

### Example Logins:
- **Staff**  
  - Username: `140003`  
  - Password: `123456`

- **Manager**  
  - Username: `140894`  
  - Password: `123456`

- **HR**  
  - Username: `130002`  
  - Password: `123456`

