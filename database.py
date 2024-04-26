import sqlite3
import os
import csv

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

    def setup_database(self):
        self.execute_query('''CREATE TABLE IF NOT EXISTS "Person" (
            "PersonID" TEXT PRIMARY KEY,
            "FirstName" TEXT NOT NULL,
            "LastName" TEXT NOT NULL,
            "Email" TEXT NOT NULL UNIQUE,
            "PhoneNumber" TEXT,
            "DateOfBirth" TEXT,
            "Password" TEXT NOT NULL,
            "Role" TEXT NOT NULL CHECK (Role IN ('Student', 'Professor'))
        );''')  


        self.execute_query('''CREATE TABLE IF NOT EXISTS "Enrollment" (
            "EnrollmentID" TEXT PRIMARY KEY,
            "PersonID" TEXT NOT NULL,
            "CourseID" TEXT NOT NULL,
            "EnrollmentDate" TEXT NOT NULL,
            FOREIGN KEY ("PersonID") REFERENCES "Person" ("PersonID"),
            FOREIGN KEY ("CourseID") REFERENCES "Course" ("CourseID")
        );''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Course" (
            "CourseID" INTEGER PRIMARY KEY,
            "CourseName" TEXT NOT NULL,
            "CourseDescription" TEXT,
            "CreditHours" TEXT NOT NULL,
            "ProfessorID" TEXT,
            FOREIGN KEY ("ProfessorID") REFERENCES "Person" ("PersonID")
        );''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Student" (
            "PersonID" TEXT PRIMARY KEY,
            "Major" TEXT,
            "Minor" TEXT,
            "GraduationYear" INTEGER,
            FOREIGN KEY ("PersonID") REFERENCES "Person" ("PersonID")
        );''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Professor" (
            "PersonID" TEXT PRIMARY KEY,
            "OfficeNumber" TEXT,
            FOREIGN KEY ("PersonID") REFERENCES "Person" ("PersonID")
        );''')
        
        if not self.column_exists('Student', 'TotalCreditHrs'):
            self.execute_query('''ALTER TABLE Student ADD COLUMN TotalCreditHrs INTEGER DEFAULT 0;''')

        self.import_data('courses.csv', 'Course', ['CourseID', 'CourseName', 'CourseDescription', 'CreditHours', 'ProfessorID'])
        self.import_data('professors.csv', 'Person', ['PersonID', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'DateOfBirth', 'Password', 'Role'])
        self.import_data('professors.csv', 'Professor', ['PersonID', 'OfficeNumber'])

    def column_exists(self, table_name, column_name):
        """ Check if a specific column exists in a given table """
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in cursor.fetchall()]
        return column_name in columns

    def role_exists_for_person(self, person_id, role):
        """ Check if the specified role exists for the given person """
        results = self.execute_query("SELECT 1 FROM Person WHERE PersonID = ? AND Role = ?;", (person_id, role))
        return len(results) > 0
    
    def import_data(self, csv_path, table, columns):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_tuple = tuple(row[col] if col in row else None for col in columns)
                placeholders = ', '.join(['?'] * len(columns))
                sql = f'INSERT OR IGNORE INTO {table} ({", ".join(columns)}) VALUES ({placeholders});'
                self.execute_query(sql, data_tuple)

    def execute_query(self, query, params=None):
        """
        Executes a SQL query and returns the results for 'SELECT' or the last row id for 'INSERT'.
        
        :param query: SQL query to be executed
        :param params: Parameters for the query to prevent SQL injection
        :return: Query result set for 'SELECT' queries or last row id for 'INSERT'
        """
        cursor = self.conn.cursor()
        try:
            if params: 
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.conn.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return None
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        
    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            print("\n= Database connection closed =")


