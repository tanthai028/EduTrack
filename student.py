from menu import Menu
from classes import *

def get_student_info(db, uid):
    # Adjusted query to join Person and Student tables
    query = """
    SELECT 
        Person.PersonID, Person.FirstName, Person.LastName, Person.Email, Person.PhoneNumber, Person.DateOfBirth, 
        Student.Major, Student.Minor, Student.GraduationYear, Student.TotalCreditHrs
    FROM 
        Person 
    JOIN 
        Student ON Person.PersonID = Student.PersonID
    WHERE 
        Person.PersonID = ? AND Person.Role = 'Student';
    """
    params = (uid,)
    student_info = db.execute_query(query, params)
    if student_info:
        # Updated return dictionary to include new fields
        return {
            'StudentID': student_info[0][0],
            'FirstName': student_info[0][1],
            'LastName': student_info[0][2],
            'Email': student_info[0][3],
            'PhoneNumber': student_info[0][4],
            'DateOfBirth': student_info[0][5],
            'Major': student_info[0][6],
            'Minor': student_info[0][7],
            'GraduationYear': student_info[0][8],
            'TotalCreditHrs': student_info[0][9],
        }
    else:
        return None

def view_details(db, uid):
    student_info = get_student_info(db, uid)

    print("=== Student Information ===")
    details = [
        f"U Number: {student_info.get('StudentID', 'N/A')}",
        f"Name: {student_info.get('FirstName', 'N/A')} {student_info.get('LastName', 'N/A')}",
        f"Email: {student_info.get('Email', 'N/A')}",
        f"Phone Number: {student_info.get('PhoneNumber', 'N/A')}",
        f"Date of Birth: {student_info.get('DateOfBirth', 'N/A')}",
        f"Major: {student_info.get('Major', 'N/A')}",
        f"Minor: {student_info.get('Minor', 'N/A')}",
        f"GraduationYear: {student_info.get('GraduationYear', 'N/A')}",
        f"TotalCreditHrs: {student_info.get('TotalCreditHrs', 'N/A')}",
    ]
    for detail in details:
        if 'None' not in detail:
            print(detail)
    
    print()

def delete_student(db, person_id):
    confirmation = input(f"Are you sure you want to delete the account for Professor with ID {person_id}? (yes/no): ")
    
    # Proceed only if  the user confirms with 'yes'
    if confirmation.lower() == 'yes':
        try:
            db.start_transaction()
            delete_enrollments_query = '''DELETE FROM Enrollment WHERE PersonID = ?;'''
            db.execute_query(delete_enrollments_query, (person_id,))
            
            delete_student_details_query = '''DELETE FROM Student WHERE PersonID = ?;'''
            db.execute_query(delete_student_details_query, (person_id,))

            delete_person_query = '''DELETE FROM Person WHERE PersonID = ?;'''
            db.execute_query(delete_person_query, (person_id,))

            print("Student and all related records have been deleted successfully.")
        except Exception as e:
            # Rollback transaction in case of error
            db.rollback_transaction()
            print(f"An error occurred: {e}")

def student_menu(db, uid):
    options = [
        ("View Student Information", view_details, (db, uid)),
        ("Search Classes", search_classes, (db, )),
        ("Manage Enrollments", manage_enrollments, (db, uid)),
        ("Delete Account", delete_student, (db, uid)),
        ("Back", None, ())  # None here makes the menu exit
    ]
    title = "=== Student Menu ==="
    menu = Menu(title, options)
    menu.uid = uid
    menu.run()