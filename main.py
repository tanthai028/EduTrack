import sys, os
from database import Database
from interface import *
from student import student_login
from faculty import faculty_login


def main():
    db = Database('school_database.db')
    db.setupdatabase()  # Setup the initial database

    try:
        while True:
            print_menu(main_menu_cfg)
            choice = input("> ")
            os.system('cls')
            match choice:
                case '1':
                    student_login(db)
                case '2':
                    faculty_login(db)
                case '3':
                    db.close()
                    print("Exiting...")
                    break
                case _:
                    print_invalid_msg(main_menu_cfg)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing database...")
        db.close()
        sys.exit()

if __name__ == '__main__':
    main()
