import os
from classes import *
from interface import *

def delete_student(db, student_id):
    delete_enrollments_query = '''DELETE FROM Enrollment WHERE StudentID = ?'''
    db.execute_query(delete_enrollments_query, (student_id,))

    delete_student_query = '''DELETE FROM Student WHERE StudentID = ?'''
    db.execute_query(delete_student_query, (student_id,))

def print_student_info(student_info):
    title = "=== Student Information ==="
    details = [
        f"U Number: {student_info.get('StudentID', 'N/A')}",
        f"Name: {student_info.get('FirstName', 'N/A')} {student_info.get('LastName', 'N/A')}",
        f"Email: {student_info.get('Email', 'N/A')}",
        f"Phone Number: {student_info.get('PhoneNumber', 'N/A')}",
        f"Date of Birth: {student_info.get('DateOfBirth', 'N/A')}",
    ]
    
    print(title)
    for detail in details:
        print(detail)
        
def edit_student_info(u_number, db):
    student_info = get_student_info(u_number, db)
    if student_info is None:
        print("Student not found.")
        return

    print("Select information to edit:")
    print("1. First Name")
    print("2. Last Name")
    # Add more fields as necessary

    choice = input("Enter your choice: ")
    new_value = input("Enter the new value: ")

    if choice == '1':
        query = "UPDATE Student SET FirstName = ? WHERE StudentID = ?;"
    elif choice == '2':
        query = "UPDATE Student SET LastName = ? WHERE StudentID = ?;"
    # Add more cases as necessary

    db.execute_query(query, (new_value, u_number))
    print("Information updated successfully.")

def student_menu(db, u_number):
    while True:
        print_menu(student_menu_cfg)
        user_input = input("> ")
        os.system('cls')

        match user_input:
            case '1':
                student_info = get_student_info(u_number, db)
                print_student_info(student_info)
            case '2':
                search_classes(db)
            case '3':
                register_classes(u_number, db)
            case '4':
                unregister_a_class(u_number, db)
            case '5':
                edit_student_info(u_number, db)
            case '6':
                delete_student(db, u_number)
                print(f"Successfully Deleted User: {u_number}")
                return
            case '7':
                print("Logging out...")
                return
            case _:
                print_invalid_msg(student_menu_cfg)

def student_login(db):
    while True:
        print_menu(student_login_menu_cfg)
        user_input = input("> ")
        os.system('cls')

        match user_input:
            case '1': 
                u_number = input("Enter your U number: ")
                password = input("Enter your password: ")
                student_info = validate_student_login(u_number, password, db)
                if student_info:
                    print("Login successful.")
                    student_menu(db, u_number)
                    return
                else:
                    print("Student not found or incorrect password. Please re-enter your U number and password.")
            case '2':
                create_student_account(db)
            case '3':
                return
            case _:
                print_invalid_msg(student_login_menu_cfg)

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
    
def create_student_account(db):
    print("=== Student Registration ===")
    u_number = input("Enter your U number: ")
    password = input("Create a password: ")
    first_name = input("Enter your first name: ").capitalize()
    last_name = input("Enter your last name: ").capitalize()
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
    
def edit_student_info(u_number, db):
    student_info = get_student_info(u_number, db)
    if student_info is None:
        print("Student not found.")
        return

    print("Select information to edit:")
    print("1. First Name")
    print("2. Last Name")
    # Add more fields as necessary

    choice = input("Enter your choice: ")
    new_value = input("Enter the new value: ")

    if choice == '1':
        query = "UPDATE Student SET FirstName = ? WHERE StudentID = ?;"
    elif choice == '2':
        query = "UPDATE Student SET LastName = ? WHERE StudentID = ?;"
    # Add more cases as necessary

    db.execute_query(query, (new_value, u_number))
    print("Information updated successfully.")
