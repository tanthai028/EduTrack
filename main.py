import sys
from database import Database

def main():
    db = Database('school_database.db')
    db.setupdatabase()  # Call setupdatabase method

    print("=== School Class Registration System ===")
    print("Login:")
    print("1. Student")
    print("2. Faculty")
    print("3. Exit")

    try:
        while True:
            user_type = input("Enter your role (1 for Student, 2 for Faculty, 3 to Exit): ")

            if user_type == '1':
                student_login(db)
            elif user_type == '2':
                faculty_login(db)
            elif user_type == '3':
                db.close()
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing database...")
        db.close()
        sys.exit()

def student_login(db):
    print("=== Student Login ===")
    while True:
        login_or_register = input("Do you want to (1) login or (2) register? Enter 1 or 2: ")

        if login_or_register == '1':
            u_number = input("Enter your U number: ")
            password = input("Enter your password: ")
            student_info = validate_student_login(u_number, password, db)
            if student_info:
                print("Login successful.")
                student_menu(db, u_number)
                break
            else:
                print("Student not found or incorrect password. Please re-enter your U number and password.")
        elif login_or_register == '2':
            create_student_account(db)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def validate_student_login(u_number, password, db):
    # Check if the user exists in the database and the provided credentials are correct
    query = "SELECT * FROM Student WHERE StudentID = ? AND Password = ?;"
    params = (u_number, password)
    student_info = db.execute_query(query, params)
    if student_info and len(student_info) > 0:
        return {
            'StudentID': student_info[0][0],
            'FirstName': student_info[0][1],
            'LastName': student_info[0][2],
            'Email': student_info[0][3],
            'PhoneNumber': student_info[0][4],
            'DateOfBirth': student_info[0][5]
        }
    else:
        return False

def student_menu(db, u_number):
    student_info = get_student_info(u_number, db)
    if student_info:
        while True:
            print("=== Student Menu ===")
            print("1. View Student Information")
            print("2. Search Classes")
            print("3. Register for Classes")
            print("4. Logout")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                print("=== Student Information ===")
                print(f"U Number: {student_info['StudentID']}")
                print(f"Name: {student_info['FirstName']} {student_info['LastName']}")
                print(f"Email: {student_info['Email']}")
                print(f"Phone Number: {student_info['PhoneNumber']}")
                print(f"Date of Birth: {student_info['DateOfBirth']}")
            elif choice == '2':
                search_classes(db)
            elif choice == '3':
                register_classes(u_number, db)
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

def get_student_info(u_number, db):
    query = "SELECT * FROM Student WHERE StudentID = ?;"
    params = (u_number,)
    student_info = db.execute_query(query, params)
    if student_info:
        return {
            'StudentID': student_info[0][0],
            'FirstName': student_info[0][1],
            'LastName': student_info[0][2],
            'Email': student_info[0][3],
            'PhoneNumber': student_info[0][4],
            'DateOfBirth': student_info[0][5]
        }
    else:
        return None

def search_classes(db):
    print("=== Search Classes ===")
    keyword = input("Enter keyword to search for classes: ")
    query = "SELECT * FROM Course WHERE CourseName LIKE ?;"
    params = (f'%{keyword}%',)
    result = db.execute_query(query, params)
    if result:
        print("Search Results:")
        for row in result:
            print(f"CourseID: {row[0]}, Course Name: {row[1]}, Course Description: {row[2]}, Credit Hours: {row[3]}")
            # You can print more information as needed
    else:
        print("No classes found matching the keyword.")

def register_classes(u_number, db):
    # Implementation of class registration
    pass

def create_student_account(db):
    print("=== Student Registration ===")
    u_number = input("Enter your U number: ")
    password = input("Create a password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    phone_number = input("Enter your phone number: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")

    # Check if the user already exists
    existing_user = db.execute_query("SELECT * FROM Student WHERE StudentID = ?;", (u_number,))
    if existing_user:
        print("User already exists. Please log in.")
    else:
        db.execute_query("INSERT INTO Student (StudentID, Password, FirstName, LastName, Email, PhoneNumber, DateOfBirth) VALUES (?, ?, ?, ?, ?, ?, ?);", (u_number, password, first_name, last_name, email, phone_number, dob))
        print("Account created successfully. You can now log in.")

def faculty_login(db):
    print("=== Faculty Login ===")
    while True:
        login_or_register = input("Do you want to (1) login or (2) register? Enter 1 or 2: ")

        if login_or_register == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if validate_faculty_login(email, password, db):
                print("Login successful.")
                faculty_menu(db, email)
                break
            else:
                print("Invalid credentials. Please try again.")
        elif login_or_register == '2':
            create_faculty_account(db)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def validate_faculty_login(email, password, db):
    # Check if the user exists in the database and the provided credentials are correct
    query = "SELECT * FROM Instructor WHERE Email = ? AND Password = ?;"
    params = (email, password)
    return db.execute_query(query, params)

def faculty_menu(db, email):
    print("=== Faculty Menu ===")
    print("1. View Faculty Information")
    print("2. Manage Classes")
    print("3. Logout")

    faculty_info = get_faculty_info(email, db)
    if faculty_info:
        while True:
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                print("=== Faculty Information ===")
                print(f"Email: {faculty_info['Email']}")
                print(f"Name: {faculty_info['FirstName']} {faculty_info['LastName']}")
                # Add more information as needed
            elif choice == '2':
                manage_classes(email, db)
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")

def get_faculty_info(email, db):
    query = "SELECT * FROM Instructor WHERE Email = ?;"
    params = (email,)
    faculty_info = db.execute_query(query, params)
    if faculty_info:
        return {
            'Email': faculty_info[0][3],
            'FirstName': faculty_info[0][1],
            'LastName': faculty_info[0][2]
            # Add more fields as needed
        }
    else:
        return None

def create_faculty_account(db):
    print("=== Faculty Registration ===")
    email = input("Enter your email: ")
    password = input("Create a password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    office_number = input("Enter your office number: ")

    # Check if the user already exists
    existing_user = db.execute_query("SELECT * FROM Instructor WHERE Email = ?;", (email,))
    if existing_user:
        print("User already exists. Please log in.")
    else:
        db.execute_query("INSERT INTO Instructor (FirstName, LastName, Email, Password, OfficeNumber) VALUES (?, ?, ?, ?, ?);", (first_name, last_name, email, password, office_number))
        print("Account created successfully. You can now log in.")

def manage_classes(email, db):
    # Implementation for faculty to manage classes
    pass

if __name__ == '__main__':
    main()
