from datetime import datetime

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
        if option == 'update':
            # Allow the instructor to select a class to update
            course_id_to_update = input("Enter CourseID of the class to update: ")
            # Check if the instructor manages the selected class
            if any(course_id_to_update == row[0] for row in faculty_classes):
                # Implement logic to update an existing class
                update_class(course_id_to_update, db)
            else:
                print("You don't manage the selected class.")
        elif option == 'remove':
            # Allow the instructor to select a class to remove
            course_id_to_remove = input("Enter CourseID of the class to remove: ")
            # Check if the instructor manages the selected class
            if any(course_id_to_remove == row[0] for row in faculty_classes):
                # Implement logic to remove a class
                remove_class(course_id_to_remove, db)
            else:
                print("You don't manage the selected class.")
        else:
            print("Invalid option.")
    else:
        print("You are not managing any classes.")

def update_class(course_id, db):
    print(f"=== Update Class {course_id} ===")
    # Fetch information of the class to be updated
    query = "SELECT * FROM Course WHERE CourseID = ?;"
    params = (course_id,)
    class_info = db.execute_query(query, params)
    
    if class_info:
        print("Current Class Information:")
        print(f"Course Name: {class_info[0][2]}")
        print(f"Current Course Description: {class_info[0][3]}")
        print(f"Current Credit Hours: {class_info[0][4]}")
        
        # Get updated information from the user
        new_course_name = input("Enter new course name (leave blank to keep current): ")
        new_course_description = input("Enter new course description (leave blank to keep current): ")
        new_credit_hours = input("Enter new credit hours (leave blank to keep current): ")
        
        # Update the class information in the database
        if new_course_name or new_course_description or new_credit_hours:
            query = "UPDATE Course SET CourseName = COALESCE(?, CourseName), CourseDescription = COALESCE(?, CourseDescription), CreditHours = COALESCE(?, CreditHours) WHERE CourseID = ?;"
            params = (new_course_name, new_course_description, new_credit_hours, course_id)
            db.execute_query(query, params)
            print("Class updated successfully.")
        else:
            print("No changes made.")
    else:
        print(f"Class with CourseID: {course_id} not found.")

def remove_class(course_id, db):
    print(f"=== Remove Class {course_id} ===")
    # Confirm with the instructor before removing the class
    confirmation = input(f"Are you sure you want to remove the class with CourseID {course_id}? (yes/no): ")
    if confirmation.lower() == 'yes':
        # Remove the class and associated enrollments from the database
        query_remove_enrollments = "DELETE FROM Enrollment WHERE CourseID = ?;"
        params_remove_enrollments = (course_id,)
        db.execute_query(query_remove_enrollments, params_remove_enrollments)
        
        query_remove_class = "DELETE FROM Course WHERE CourseID = ?;"
        params_remove_class = (course_id,)
        db.execute_query(query_remove_class, params_remove_class)
        
        print("Class removed successfully.")
    else:
        print("Removal canceled.")

        
def register_classes(u_number, db):
    print("=== Register Classes ===")
    # Fetch available classes
    query = "SELECT * FROM Course;"
    available_classes = db.execute_query(query)
    
    if available_classes:
        # Allow the user to select classes to register
        selected_courses = input("Enter CourseIDs separated by commas to register or a single CourseID (e.g., CourseID1, CourseID2): ").split(",")
        
        # Register selected classes
        for course_id in selected_courses:
            # Check if the course exists
            query = "SELECT * FROM Course WHERE CourseID = ?;"
            params = (course_id.strip(),)
            course = db.execute_query(query, params)
            if course:
                # Insert the enrollment into the database
                enrollment_id = f"{u_number}_{course_id.strip()}"
                enrollment_date = datetime.now().strftime("%Y-%m-%d")
                query = "INSERT INTO Enrollment (EnrollmentID, StudentID, CourseID, EnrollmentDate) VALUES (?, ?, ?, ?);"
                params = (enrollment_id, u_number, course_id.strip(), enrollment_date)
                db.execute_query(query, params)
                print(f"Successfully registered for CourseID: {course_id.strip()}")
            else:
                print(f"CourseID: {course_id.strip()} does not exist.")
    else:
        print("No classes available for registration.")
def unregister_a_class(u_number, db):
    print("=== Unregister a Class ===")
    # Fetch classes registered by the student
    query = "SELECT * FROM Enrollment WHERE StudentID = ?;"
    params = (u_number,)
    registered_classes = db.execute_query(query, params)
    
    if registered_classes:
        # Display classes registered by the student
        print("Classes Registered by You:")
        for row in registered_classes:
            course_id = row[2]
            query = "SELECT * FROM Course WHERE CourseID = ?;"
            params = (course_id,)
            course_info = db.execute_query(query, params)
            if course_info:
                print(f"CourseID: {course_info[0][0]}, Course Name: {course_info[0][2]}, Credit Hours: {course_info[0][4]}")
        
        # Allow the user to select a class to unregister
        class_to_unregister = input("Enter CourseID to unregister: ")
        
        # Check if the user is registered for the selected class
        query = "SELECT * FROM Enrollment WHERE StudentID = ? AND CourseID = ?;"
        params = (u_number, class_to_unregister)
        existing_registration = db.execute_query(query, params)
        
        if existing_registration:
            # Unregister the class
            query = "DELETE FROM Enrollment WHERE StudentID = ? AND CourseID = ?;"
            params = (u_number, class_to_unregister)
            db.execute_query(query, params)
            print(f"Successfully unregistered from CourseID: {class_to_unregister}")
        else:
            print("You are not registered for the selected class.")
    else:
        print("You are not registered for any classes.")
