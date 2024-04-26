from menu import Menu
from clases import *
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
    # print(prof_info)

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
    query = '''DELETE FROM Student WHERE PersonID = ?;'''
    db.execute_query(query, (uid,))

    query = '''DELETE FROM Enrollment WHERE PersonID = ?;'''
    db.execute_query(query, (uid,))

    query = '''DELETE FROM Person WHERE PersonID = ?;'''
    db.execute_query(query, (uid,))
    input("Student and all related records have been deleted successfully.")

def professor_menu(db, uid):
    options = [
        ("View Professor Information", view_details, (db,uid)),
        ("Create Class", create_class, (db,uid)),
        ("Manage Classes", manage_classes, (db,uid)),
        ("Delete Account", delete_prof, (db,uid)),
        ("Print Students for a Class", print_students_for_class, (uid,1, None)),
        ("Exit", None)  # None here makes the menu exit
    ]
    title = "=== Professor Menu ==="
    menu = Menu(title, options)
    menu.run()
