import sqlite3
import os
from tabulate import tabulate

class Database:
    def __init__(self, db_filename='school_database.db'):
        """
        Initializes a new instance of the Database class, opening a connection to the SQLite database.
        
        :param db_filename: Filename of the SQLite database file (default: 'school_database.db')
        """
        self.db_path = os.path.join(os.getcwd(), db_filename)
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"= Database connection opened at {self.db_path} =\n")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def setupdatabase(self):
        # Create database file if it doesn't exist
        try:
            open(self.db_path, 'r').close()  # Check if file exists
            print(f"Database file '{self.db_path}' already exists.")
        except FileNotFoundError:
            open(self.db_path, 'w').close()  # Create file if it doesn't exist
            print(f"Database file '{self.db_path}' created.")

        # Create tables
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Student" (
        "StudentID" TEXT PRIMARY KEY CHECK(length("StudentID") = 9),
        "FirstName" TEXT NOT NULL,
        "LastName" TEXT NOT NULL,
        "Email" TEXT NOT NULL UNIQUE,
        "PhoneNumber" TEXT,
        "DateOfBirth" TEXT,
        "Password" TEXT NOT NULL
        )''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Instructor" (
        "InstructorID" TEXT PRIMARY KEY,
        "FirstName" TEXT NOT NULL,
        "LastName" TEXT NOT NULL,
        "Email" TEXT NOT NULL UNIQUE,
        "OfficeNumber" TEXT,
        "Password" TEXT NOT NULL
        )''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Enrollment" (
        "EnrollmentID" TEXT PRIMARY KEY,
        "StudentID" TEXT NOT NULL,
        "CourseID" TEXT NOT NULL,
        "EnrollmentDate" TEXT NOT NULL,
        "Grade" TEXT,
        FOREIGN KEY ("StudentID") REFERENCES "Student" ("StudentID"),
        FOREIGN KEY ("CourseID") REFERENCES "Course" ("CourseID")
        )''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Course" (
        "CourseID" TEXT PRIMARY KEY,
        "CourseName" TEXT NOT NULL,
        "CourseDescription" TEXT,
        "CreditHours" TEXT NOT NULL
        )''')

    # Remaining methods remain unchanged...

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
    
    # Remaining methods remain unchanged...

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            # print("\n= Database connection closed =")
