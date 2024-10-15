drop table wfh_requests;
drop table employee_list;


CREATE DATABASE  if not exists spmtest1 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE spmtest1; 

create table Employee_List(
Staff_ID int not null,
Primary key (Staff_ID),
Staff_FName varchar(50) Not Null,
Staff_LName varchar(50) Not Null,
Dept varchar(50) Not Null,
Position varchar(50) Not Null,
Country varchar(50) not null,
Email varchar(50) not null,
Reporting_Manager int, 
User_Password varchar(1024),
Role int Not Null
);

select * from employee_list;


ALTER TABLE employee_list
    ADD COLUMN Request_Status ENUM('Approved', 'Pending', 'Withdrawn', 'Rejected', 'Cancelled') 
    DEFAULT 'Pending';

ALTER TABLE employee_list
    ADD CONSTRAINT FK_Reporting_Manager
    FOREIGN KEY (Reporting_Manager) 
    REFERENCES employee_list(Staff_ID);




#Create booking table (outdated)
#create table WFH_Requests(
#request_ID int AUTO_INCREMENT Primary key,
#selected_date date not null,
#day_of_week char(50) not null,
#time_block ENUM ("AM", "PM", "Whole Day"),
#Requester_ID int not null,
#Foreign key (Requester_ID) references Employee_list(Staff_ID),
#Requester_Supervisor int not null,
#Foreign key (Requester_Supervisor) references Employee_list(Reporting_Manager),
#Request_Status ENUM('Approved', 'Pending',"Withdrawn","Rejected",'Cancelled') DEFAULT 'Pending'
#);

#Create booking table (new)
create table WFH_Requests(
request_ID int AUTO_INCREMENT Primary key,
start_date date not null,
end_date date not null,
Requester_ID int not null,
Foreign key (Requester_ID) references Employee_list(Staff_ID),
Requester_Supervisor int not null,
Foreign key (Requester_Supervisor) references Employee_list(Reporting_Manager),
Monday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Tuesday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Wednesday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Thursday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Friday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Saturday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Sunday Enum('AM', 'PM', 'Whole Day', 'NULL') DEFAULT 'NULL',
Request_Status ENUM('Approved', 'Pending',"Withdrawn","Rejected",'Cancelled') DEFAULT 'Pending'
cloudinary_link varchar(1028),
repeating Boolean DEFAULT FALSE;
);

# Mock data for testing
insert into wfh_requests values (1, 20240724, 20240729, 150192, 151408, "AM", "AM", "AM", "PM", "AM", "PM", "Whole Day", "Pending");
insert into wfh_requests values (2, 20240724, 20240729, 150192, 151408, "AM", "AM", "AM", "PM", "AM", "PM", "Whole Day", "Approved");
