from menu import Menu
from classes import *

def get_prof_info(db, uid):
    query = "SELECT * FROM Person WHERE PersonID = ? AND Role = 'Professor';"
    params = (uid,)
    prof_info = db.execute_query(query, params)
    if prof_info:
        return {
            'ProfessorID': prof_info[0][0],
            'FirstName': prof_info[0][1],
            'LastName': prof_info[0][2],
            'Email': prof_info[0][3],
            'PhoneNumber': prof_info[0][4],
            'DateOfBirth': prof_info[0][5]
        }
    else:
        return None

def view_details(db, uid):
    prof_info = get_prof_info(db, uid)

    print("=== Professor Information ===")
    details = [
        f"U Number: {prof_info.get('ProfessorID', 'N/A')}",
        f"Name: {prof_info.get('FirstName', 'N/A')} {prof_info.get('LastName', 'N/A')}",
        f"Email: {prof_info.get('Email', 'N/A')}",
        f"Phone Number: {prof_info.get('PhoneNumber', 'N/A')}",
        f"Date of Birth: {prof_info.get('DateOfBirth', 'N/A')}",
    ]
    for detail in details:
        print(detail)
    
    print()

def delete_prof(db, uid):
    # Start transaction
    db.start_transaction()
    
    try:
        # Remove enrollments for courses the professor was teaching
        query_enrollments = '''DELETE FROM Enrollment WHERE CourseID IN (SELECT CourseID FROM Course WHERE ProfessorID = ?);'''
        db.execute_query(query_enrollments, (uid,))

        # Remove the professor from courses they are teaching
        query_courses = '''DELETE FROM Course WHERE ProfessorID = ?;'''
        db.execute_query(query_courses, (uid,))

        # Finally, delete the professor from the Person table
        query_person = '''DELETE FROM Person WHERE PersonID = ?;'''
        db.execute_query(query_person, (uid,))
        
        # Commit transaction if all operations were successful
        db.commit_transaction()
        print(f'Deleted Professor {uid} and all associated records.')
    except Exception as e:
        # Rollback transaction in case of error
        db.rollback_transaction()
        print(f"An error occurred: {e}")

def professor_menu(db, uid):
    options = [
        ("View Professor Information", view_details, (db,uid)),
        ("Create Class", create_class, (db,uid)),
        ("Manage Classes", manage_classes, (db,uid)),
        ("Delete Account", delete_prof, (db,uid)),
        ("Print Students for a Class", print_students_for_class, (uid, db)),
        ("Exit", None, ())  # None here makes the menu exit
    ]
    title = "=== Professor Menu ==="
    menu = Menu(title, options)
    menu.run()
