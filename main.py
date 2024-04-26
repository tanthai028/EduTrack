from database import Database
from account import login, register
from menu import Menu
from helpers import clear_screen

def main_menu(db):
    options = [
        ("Login", login, (db,)),
        ("Register", register, (db,)),
        ("Exit", None, ())  # None here makes the menu exit
    ]
    title = "=== EduTrack ==="
    menu = Menu(title, options)
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing database...")
        return

if __name__ == "__main__":
    clear_screen()
    db = Database('school_database.db')
    db.setup_database()  # Setup the initial database
    print('* Press Ctrl+C to cancel operation *\n')
    main_menu(db)
    db.close()