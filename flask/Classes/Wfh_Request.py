from .Database import db  # Import the shared db instance

class WFHRequests(db.Model):
    __tablename__ = 'WFH_Requests'

    #request_ID = db.Column(db.Integer, primary_key=True)
    #selected_date = db.Column(db.Date, nullable=False)
    #day_of_week = db.Column(db.String(50), nullable=False)
    #Requester_ID = db.Column(db.Integer, nullable=False)
    #Requester_Supervisor = db.Column(db.Integer, nullable=False)
    #Request_Status = db.Column(db.Enum('Approved', 'Pending', 'Withdrawn', 'Rejected'), default='Pending')

    request_ID = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    Requester_ID = db.Column(db.Integer, nullable=False)
    Requester_Supervisor = db.Column(db.Integer, nullable=False)
    Monday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Tuesday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Wednesday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Thursday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Friday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Saturday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Sunday = db.Column(db.Enum('AM', 'PM', 'Whole Day', 'NULL'), nullable=True, default='NULL')
    Request_Status = db.Column(db.Enum('Approved', 'Pending', 'Withdrawn', 'Rejected'), default='Pending')


    @staticmethod
    def get_by_id(request_id):
        """Retrieve a WFH request by its ID."""
        return WFHRequests.query.get(request_id)

    @staticmethod
    def get_all():
        """Retrieve all WFH requests from the database."""
        return WFHRequests.query.all()


    #not in use yet
    @staticmethod
    def update_request(request_id, selected_date, day_of_week, requester_id, requester_supervisor, request_status):
        """Update a WFH request."""
        wfh_request = WFHRequests.query.get(request_id)
        if wfh_request:
            wfh_request.selected_date = selected_date
            wfh_request.day_of_week = day_of_week
            wfh_request.Requester_ID = requester_id
            wfh_request.Requester_Supervisor = requester_supervisor
            wfh_request.Request_Status = request_status
            db.session.commit()  # Commit the changes to the database
            return True
        return False