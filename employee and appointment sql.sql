
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

Alter table Employee_List
Add constraint FK_Reporting_Manager
Foreign key (Reporting_Manager) references Employee_List(Staff_ID);
Request_Status ENUM('Approved', 'Pending',"Withdrawn","Rejected",'Cancelled') DEFAULT 'Pending'
);


#Create booking table
create table WFH_Requests(
request_ID int AUTO_INCREMENT Primary key,
selected_date date not null,
day_of_week char(50) not null,
time_block ENUM ("AM", "PM", "Whole Day"),
Requester_ID int not null,
Foreign key (Requester_ID) references Employee_list(Staff_ID),
Requester_Supervisor int not null,
Foreign key (Requester_Supervisor) references Employee_list(Reporting_Manager),
Request_Status ENUM('Approved', 'Pending',"Withdrawn","Rejected",'Cancelled') DEFAULT 'Pending'
);


