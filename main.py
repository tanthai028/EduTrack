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
                student_menu(db)
            elif user_type == '2':
                faculty_menu(db)
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

def student_menu(db):
    print("=== Student Menu ===")
    print("1. View Student Information")
    print("2. Search Classes")
    print("3. Register for Classes")
    print("4. Logout")

    student_id = input("Enter your student ID: ")
    student_info = get_student_info(student_id, db)
    if student_info:
        while True:
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                print("=== Student Information ===")
                print(f"Student ID: {student_info['student_id']}")
                print(f"Name: {student_info['fname']} {student_info['lname']}")
                print(f"Degree: {student_info['degree']}")
                print(f"GPA: {student_info['gpa']}")
                print(f"Major: {student_info['major']}")
                print(f"Date of Birth: {student_info['DOB']}")
            elif choice == '2':
                search_classes(db)
            elif choice == '3':
                register_classes(student_id, db)
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

def get_student_info(student_id, db):
    query = "SELECT * FROM Students WHERE student_id = ?;"
    params = (student_id,)
    result = db.execute_query(query, params)
    if result:
        student_info = {
            'student_id': result[0][0],
            'fname': result[0][1],
            'lname': result[0][2],
            'degree': result[0][3],
            'gpa': result[0][4],
            'major': result[0][5],
            'DOB': result[0][6]
        }
        return student_info
    else:
        print("Student not found.")
        return None

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

def register_classes(student_id, db):
    # Implementation of class registration
    pass

def faculty_menu(db):
    print("=== Faculty Menu ===")
    print("1. View Faculty Information")
    print("2. Manage Classes")
    print("3. Logout")

    faculty_id = input("Enter your faculty ID: ")
    faculty_info = get_faculty_info(faculty_id, db)
    if faculty_info:
        while True:
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                print("=== Faculty Information ===")
                print(f"Faculty ID: {faculty_info['faculty_id']}")
                print(f"Name: {faculty_info['fname']} {faculty_info['lname']}")
                # Add more information as needed
            elif choice == '2':
                manage_classes(faculty_id, db)
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")

def get_faculty_info(faculty_id, db):
    # Implementation to retrieve faculty information
    pass

def manage_classes(faculty_id, db):
    # Implementation for faculty to manage classes
    pass

if __name__ == '__main__':
    main()
