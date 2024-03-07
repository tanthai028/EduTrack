import sys
from database import Database

def main():
    db = Database('example.db')

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
    u_number = input("Enter your U number: ")
    password = input("Enter your password: ")

    # Validate student login credentials
    if validate_student_login(u_number, password, db):
        print("Login successful.")
        student_menu(db, u_number)
    else:
        print("Invalid credentials. Please try again.")

def validate_student_login(u_number, password, db):
    # Implement validation of student login credentials
    # This could involve querying the database to check if the credentials are correct
    # For simplicity, let's assume all logins are successful
    return True

def student_menu(db, u_number):
    print("=== Student Menu ===")
    print("1. View Student Information")
    print("2. Search Classes")
    print("3. Register for Classes")
    print("4. Logout")

    student_info = get_student_info(u_number, db)
    if student_info:
        while True:
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                print("=== Student Information ===")
                print(f"U Number: {student_info['u_number']}")
                print(f"Name: {student_info['fname']} {student_info['lname']}")
                print(f"Degree: {student_info['degree']}")
                print(f"GPA: {student_info['gpa']}")
                print(f"Major: {student_info['major']}")
                print(f"Date of Birth: {student_info['DOB']}")
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
    # Implement function to retrieve student information from the database
    # Stub for now, return example student data
    student_info = {
        'u_number': u_number,
        'fname': 'John',
        'lname': 'Doe',
        'degree': 'Computer Science',
        'gpa': '3.5',
        'major': 'Computer Science',
        'DOB': '1990-01-01'
    }
    return student_info

def search_classes(db):
    print("=== Search Classes ===")
    keyword = input("Enter keyword to search for classes: ")
    query = f"SELECT * FROM Classes WHERE title LIKE ? OR depcode LIKE ? OR course_name LIKE ?;"
    params = (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
    result = db.execute_query(query, params)
    if result:
        print("Search Results:")
        for row in result:
            print(f"CRN: {row[0]}, Title: {row[1]}, Department Code: {row[2]}, Course Name: {row[3]}")
            # You can print more information as needed
    else:
        print("No classes found matching the keyword.")

def register_classes(u_number, db):
    # Implementation of class registration
    pass

def faculty_login(db):
    print("=== Faculty Login ===")
    email = input("Enter your professional email: ")
    password = input("Enter your password: ")

    # Validate faculty login credentials
    if validate_faculty_login(email, password, db):
        print("Login successful.")
        faculty_menu(db, email)
    else:
        print("Invalid credentials. Please try again.")

def validate_faculty_login(email, password, db):
    # Implement validation of faculty login credentials
    # This could involve querying the database to check if the credentials are correct
    # For simplicity, let's assume all logins are successful
    return True

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
                print(f"Email: {faculty_info['email']}")
                print(f"Name: {faculty_info['fname']} {faculty_info['lname']}")
                # Add more information as needed
            elif choice == '2':
                manage_classes(email, db)
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")

def get_faculty_info(email, db):
    # Implement function to retrieve faculty information from the database
    # Stub for now, return example faculty data
    faculty_info = {
        'email': email,
        'fname': 'Jane',
        'lname': 'Smith'
        # Add more fields as needed
    }
    return faculty_info

def manage_classes(email, db):
    # Implementation for faculty to manage classes
    pass

def create_student_account(db):
    print("=== Create Student Account ===")
    u_number = input("Enter U number: ")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    degree = input("Enter degree: ")
    gpa = input("Enter GPA: ")
    major = input("Enter major: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")

    # Insert student information into the database
    query = "INSERT INTO Students (u_number, fname, lname, degree, gpa, major, DOB) VALUES (?, ?, ?, ?, ?, ?, ?);"
    params = (u_number, fname, lname, degree, gpa, major, dob)
    db.execute_query(query, params)
    print("Student account created successfully.")

if __name__ == '__main__':
    main()
