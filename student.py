from menu import Menu
from classes import *

def get_student_info(db, uid):
    query = "SELECT * FROM Person WHERE PersonID = ? AND Role = 'Student';"
    params = (uid,)
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

def view_details(db, uid):
    student_info = get_student_info(db, uid)

    print("=== Student Information ===")
    details = [
        f"U Number: {student_info.get('StudentID', 'N/A')}",
        f"Name: {student_info.get('FirstName', 'N/A')} {student_info.get('LastName', 'N/A')}",
        f"Email: {student_info.get('Email', 'N/A')}",
        f"Phone Number: {student_info.get('PhoneNumber', 'N/A')}",
        f"Date of Birth: {student_info.get('DateOfBirth', 'N/A')}",
    ]
    for detail in details:
        print(detail)
    
    print()

def delete_student(db, person_id):
    delete_student_details_query = '''DELETE FROM Student WHERE PersonID = ?;'''
    db.execute_query(delete_student_details_query, (person_id,))

    delete_enrollments_query = '''DELETE FROM Enrollment WHERE PersonID = ?;'''
    db.execute_query(delete_enrollments_query, (person_id,))

    delete_person_query = '''DELETE FROM Person WHERE PersonID = ?;'''
    db.execute_query(delete_person_query, (person_id,))
    input("Student and all related records have been deleted successfully.")

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