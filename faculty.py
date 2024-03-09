from classes import *
import os
from interface import *

def faculty_menu(db, email):
    while True:
        print_menu(faculty_menu_cfg)
        choice = input("> ")
        os.system('cls')

        match choice:
            case '1':
                faculty_info = get_faculty_info(email, db)
                print("=== Faculty Information ===")
                print(f"Email: {faculty_info['Email']}")
                print(f"Name: {faculty_info['FirstName']} {faculty_info['LastName']}")
            case '2':
                create_class(email, db)
            case '3':
                manage_classes(email, db)
            case '4':
                print("Logging out...")
                return
            case _:
                print_invalid_msg(faculty_menu_cfg)


def faculty_login(db):
    while True:
        print_menu(faculty_login_menu_cfg)
        choice = input("> ")
        os.system('cls')

        match choice:
            case '1':
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                if validate_faculty_login(email, password, db):
                    print("Login successful.")
                    faculty_menu(db, email)
                    return
                else:
                    print("Invalid credentials. Please try again.")
            case '2':
                create_faculty_account(db)
            case '3':
                return
            case _:
                print_invalid_msg(faculty_login_menu_cfg)

def validate_faculty_login(email, password, db):
    # Check if the user exists in the database and the provided credentials are correct
    query = "SELECT * FROM Instructor WHERE Email = ? AND Password = ?;"
    params = (email, password)
    return db.execute_query(query, params)

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