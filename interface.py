
def print_menu(menu):
    title = menu['title']
    options = menu['options']
    print(title)
    for i, option in enumerate(options, 1):
        print(f'{i}. {option}')

def print_student_info(student_info):
    print("=== Student Information ===")
    print(f"U Number: {student_info['StudentID']}")
    print(f"Name: {student_info['FirstName']} {student_info['LastName']}")
    print(f"Email: {student_info['Email']}")
    print(f"Phone Number: {student_info['PhoneNumber']}")
    print(f"Date of Birth: {student_info['DateOfBirth']}")

def print_invalid_choice(menu):
    options = [i for i, ctx in enumerate(menu['options'], 1)]
    print(f"Invalid choice. Please enter a number in {options}")

main_menu_cfg = {
    'title': '=== School Class Registration System ===',
    'options': [
        'Student',
        'Faculty',
        'Exit'
    ]
}

student_login_menu_cfg = {
    'title': '=== Student Login ===',
    'options': [
        'Login',
        'Register',
        'Exit'
    ]
}



student_menu_cfg = {
    'title': '=== Student Menu ===',
    'options': [
        'View Student Information',
        'Search Classes',
        'Register for Classes',
        'Logout',
    ]
}

faculty_login_menu_cfg = {
    'title': '=== Faculty Login ===',
    'options': [
        'Login',
        'Register',
        'Exit'
    ]
}

faculty_menu_cfg = {
    'title': '=== Faculty Menu ===',
    'options': [
        'View Faculty Information',
        'Manage Classes'
    ]
}