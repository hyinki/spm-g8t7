from werkzeug.security import check_password_hash
from .Employees import Employees  # Import the Employees model

class Login:
    def check_user_password(self, user_id, input_password):
        # Get the password hash for the user by their ID
        pword = Employees.check_pword(user_id)
        
        if pword:  # Ensure the password exists for the user
            # Check if the input password matches the stored hash
            return check_password_hash(pword, input_password)
        else:
            return False