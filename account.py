import uuid
from helpers import clear_screen
from student import student_menu
from professor import professor_menu

def generate_unique_id():
    """Generate a UUID and extract the first 8 digits from it."""
    uuid_str = str(uuid.uuid4())  # Generate a UUID and convert to string
    digits = ''.join([char for char in uuid_str if char.isdigit()])  # Extract digits
    return digits[:8]  # Return the first 8 digits

def valid_uid(uid):
    if 'U' in uid:
        return len(uid[1:])
    else: 
        return len(uid) == 8 == 8
    
def reformat_uid(uid):
    if 'U' in uid:
        return uid
    else:
        return 'U' + uid

def ask_role():
    role = None
    while role not in ['1','2']:
        print('Are you a student or professor?')
        print('1. Student')
        print('2. Professor')
        role = input('> ')

        if role not in ['1','2']:
            clear_screen()
            print('Invalid option, please try again.')

    role = 'Student' if role == '1' else 'Professor'
    return role

def id_exists(db, table, id_column, id_value):
    query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {id_column} = ? LIMIT 1)"
    return db.execute_query(query, (id_value,))[0] == 1

def create_account(db, role, fname, lname, email, password):
    # Check if the email already exists in the Person table
    existing_user = db.execute_query("SELECT * FROM Person WHERE Email = ?;", (email,))
    try:
        if existing_user:
            input(f"{role} already exists. Please log in.")
        else:
            # Generate a unique Person ID
            uid = 'U' + generate_unique_id()
            while id_exists(db, 'Person', 'PersonID', uid):
                uid = 'U' + generate_unique_id()

            # Insert the new user into the Person table
            db.execute_query('''INSERT INTO Person (PersonID, FirstName, LastName, Email, Password, Role) 
                                VALUES (?, ?, ?, ?, ?, ?);''', (uid, fname, lname, email, password, role))

            # Insert into role-specific tables if necessary
            if role == 'Student':
                # Assuming additional student details are required at signup, modify as necessary
                db.execute_query('''INSERT INTO Student (PersonID, Major, Minor)
                                    VALUES (?, ?, ?);''', (uid, 'Undeclared', None))
            elif role == 'Professor':
                # Assuming default values for Professor, modify as necessary
                db.execute_query('''INSERT INTO Professor (PersonID, OfficeNumber)
                                    VALUES (?, ?);''', (uid, 'TBD'))
            
            clear_screen()
            print(f"{role} account created successfully.")
            print(f"Your UID is {uid}")
            return uid
    except Exception as e:
        input(f"An error occurred while creating the account: {str(e)}")

def login(db):
    uid = ''
    while True:
        uid = input("Enter your UID: ")
        if not valid_uid(uid):
            clear_screen()
            print('Invalid UID.')
            continue

        break

    reformat_uid(uid)
    password = input("Enter your password: ")

    try:
        result = db.execute_query("SELECT Role FROM Person WHERE PersonID = ? AND Password = ?;", (uid, password))
        if result:
            input("Login successful!")
            clear_screen()
            role = result[0][0]  # Assuming the role is the first column in the result set

            if role == 'Student':
                student_menu(db, uid)
            elif role == 'Professor':
                professor_menu(db, uid)
            
            return True
        else:
            input("Invalid uid or password.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def register(db):
    role = ask_role()
    clear_screen()
    
    print(f"=== {role} Registration ===")
    fname = input('First Name: ').capitalize()
    lname = input('Last Name: ').capitalize()
    email = fname.lower() + lname.lower() + '@usf.edu'
    print(f'Your email is: {email}')

    password, conf_password = None, None
    while True:
        password = input('Password: ')
        conf_password = input('Confirm Password: ')

        if password != conf_password:
            clear_screen()
            print('Password does not match')
            continue
            
        break

    uid = create_account(db, role, fname, lname, email, password)
    clear_screen()
    if uid:
        print('Logged in!')
        if role == 'Student':
            student_menu(db, uid)
        elif role == 'Professor':
            professor_menu(db, uid)
    else:
        return