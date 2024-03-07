import sqlite3
from tabulate import tabulate

class Database:
    def __init__(self, db_path):
        """
        Initializes a new instance of the Database class, opening a connection to the SQLite database.
        
        :param db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_path)
            # print("= Database connection opened =\n")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def setupdatabase(self):
        # Create table
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Student" (
        "StudentID"	INTEGER,
        "FirstName"	TEXT NOT NULL,
        "LastName"	TEXT NOT NULL,
        "Email"	TEXT NOT NULL UNIQUE,
        "PhoneNumber"	TEXT,
        "DateOfBirth"	TEXT,
        PRIMARY KEY("StudentID" AUTOINCREMENT))''')
        
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Instructor" (
        "InstructorID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "FirstName" TEXT NOT NULL,
        "LastName" TEXT NOT NULL,
        "Email" TEXT NOT NULL UNIQUE,
        "OfficeNumber" TEXT
        )''')
        
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Enrollment" (
        "EnrollmentID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "StudentID" INTEGER NOT NULL,
        "CourseID" INTEGER NOT NULL,
        "EnrollmentDate" TEXT NOT NULL,
        "Grade" TEXT,
        FOREIGN KEY ("StudentID") REFERENCES "Student" ("StudentID"),
        FOREIGN KEY ("CourseID") REFERENCES "Course" ("CourseID")
        )''')
        
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Course" (
        "CourseID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "CourseName" TEXT NOT NULL,
        "CourseDescription" TEXT,
        "CreditHours" INTEGER NOT NULL
        )''')
        
    def execute_query(self, query, params=None):
        """
        Executes a SQL query and returns the results for 'SELECT' or the last row id for 'INSERT'.
        
        :param query: SQL query to be executed
        :param params: Parameters for the query to prevent SQL injection
        :return: Query result set for 'SELECT' queries or last row id for 'INSERT'
        """
        cursor = self.conn.cursor()
        try:
            # Does the query contain parameters?
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # if query starts with 'SELECT' or 'PRAGMA'
            if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('PRAGMA'):
                return cursor.fetchall()
            
            # if query starts with 'INSERT'
            else:
                self.conn.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return None
                
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_column_names(self, table_name):
        """Returns list of column names of table_name."""
        column_info_query = f"PRAGMA table_info({table_name});"
        columns_info = self.execute_query(column_info_query)
        column_names = [info[1] for info in columns_info]  # Column name is in the second position
        return column_names
        
    def list_tables(self):
        """Lists all existing table names in database."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        try:
            tables = self.execute_query(query)
            if tables:
                for table in tables:
                    table_name = table[0]
                    print(table_name)
            else:
                print("No tables found or unable to retrieve tables.")
        except TypeError as e:
            print(f"An error occurred: {e}")
        print()
    
    def print_table(self, table_name):
        """Prints table contents in tabular format."""
        query = f"SELECT * FROM {table_name};"
        try:
            rows = self.execute_query(query)
            if rows:
                column_names = self.get_column_names(table_name)
                print(tabulate(rows, headers=column_names, tablefmt='github'))
            else:
                print("This table does not have any data.")
        except TypeError as e:
            print(f"An error occurred: {e}")
        print()

    def user_query(self, query):
        """Executes a user sql query."""
        result = self.execute_query(query)
        print(f"{query}\n{result}")

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            # print("\n= Database connection closed =")
