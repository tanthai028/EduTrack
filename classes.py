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
def create_class(email,db):
    print("=== Create Class ===")
    course_id = input("Enter course ID: ")
    course_name = input("Enter course name: ")
    course_description = input("Enter course description: ")
    credit_hours = int(input("Enter credit hours: "))

    
    # Insert the new class into the database
    query = "INSERT INTO Course (CourseID, CourseName, CourseDescription, CreditHours, FacultyEmail) VALUES (?, ?, ?, ?, ?);"
    params = (course_id,course_name, course_description, credit_hours, email)
    db.execute_query(query, params)
    print("Class created successfully.")


def manage_classes(email, db):
    print("=== Manage Classes ===")
    # Fetch classes managed by the faculty member
    query = "SELECT * FROM Course WHERE FacultyEmail = ?;"
    params = (email,)
    faculty_classes = db.execute_query(query, params)
    
    if faculty_classes:
        # Display classes managed by the faculty member
        print("Classes Managed by You:")
        for row in faculty_classes:
            print(f"CourseID: {row[0]}, Course Name: {row[2]}, Course Description: {row[3]}, Credit Hours: {row[4]}")
        
        # Offer options for managing classes (e.g., add, update, remove)
        option = input("Enter 'add', 'update', or 'remove' to manage classes: ")
        if option == 'add':
            # Implement logic to add a new class
            pass
        elif option == 'update':
            # Implement logic to update an existing class
            pass
        elif option == 'remove':
            # Implement logic to remove a class
            pass
        else:
            print("Invalid option.")
    else:
        print("You are not managing any classes.")
        
def register_classes(u_number, db):
    # Implementation of class registration
    return
