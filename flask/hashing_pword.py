from werkzeug.security import generate_password_hash, check_password_hash

# Generate hashed password
password = '123456'
hashed_password = generate_password_hash(password)
print(hashed_password)

unhashed_password=check_password_hash(hashed_password,"123456")
print("Unhashed pword is ",unhashed_password)