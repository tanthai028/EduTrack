from database import Database

def main():
    db = Database('example.db')

    db.list_tables()
    db.print_table('Student')
    db.user_query('SELECT * FROM Student;')

    db.close()

if __name__ == '__main__':
    main()
