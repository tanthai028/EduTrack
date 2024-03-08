
def print_menu(menu):
    title = menu['title']
    options = menu['links']
    print(title)
    for i, option in enumerate(options, 1):
        print(f'{i}. {option}')



def print_invalid_msg(menu):
    links = [i for i, _ in enumerate(menu['links'], 1)]
    print(f"Invalid choice. Please enter a number in {links}")

main_menu_cfg = {
    'title': '=== School Class Registration System ===',
    'links': [
        'Student',
        'Faculty',
        'Exit'
    ]
}

student_login_menu_cfg = {
    'title': '=== Student Login ===',
    'links': [
        'Login',
        'Register',
        'Exit'
    ]
}

student_menu_cfg = {
    'title': '=== Student Menu ===',
    'links': [
        'View Student Information',
        'Search Classes',
        'Register for Classes',
        'Delete Account',
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