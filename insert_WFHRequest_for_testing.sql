insert into wfh_requests values (1, 20240724, "Monday", "AM", 150192, 151408, "Pending");
insert into wfh_requests values (2, 20240725, "Tuesday", "PM", 150192, 151408, "Pending");
insert into wfh_requests values (3, 20240726, "Wednesday", "AM", 150192, 151408, "Pending");
insert into wfh_requests values (4, 20240728, "Wednesday", "AM", 140001, 130002, "Pending");
insert into wfh_requests values (5, 20240729, "Thursday", "AM", 150192, 151408, "Approved");

update wfh_requests 
set Request_Status = "Approved"
where request_ID = 2;

delete from WFH_requests where request_id = 1;
delete from WFH_requests where request_id = 3;
delete from WFH_requests where request_id = 5;