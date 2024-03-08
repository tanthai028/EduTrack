import sys, os
from database import Database
from interface import *
from student import student_login
from faculty import faculty_login


def main():
    db = Database('school_database.db')
    db.setupdatabase()  # Call setupdatabase method

    try:
        while True:
            print_menu(main_menu_cfg)
            user_type = input("> ")
            os.system('cls')
            if user_type == '1':
                student_login(db)
            elif user_type == '2':
                faculty_login(db)
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

if __name__ == '__main__':
    main()
    # print_menu(faculty_menu_options)
