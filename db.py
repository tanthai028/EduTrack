import sqlite3
import os

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
            "CourseID" TEXT PRIMARY KEY,
            "CourseName" TEXT NOT NULL,
            "CourseDescription" TEXT,
            "CreditHours" TEXT NOT NULL,
            "ProfessorID" TEXT,
            FOREIGN KEY ("ProfessorID") REFERENCES "Person" ("PersonID")
        );''')

        self.execute_query('''CREATE TABLE IF NOT EXISTS "Role" (
            "RoleID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "RoleName" TEXT NOT NULL UNIQUE
        );''')

        # Future implementation if we want multiple roles like teacher assistants who are students
        self.execute_query('''CREATE TABLE IF NOT EXISTS "PersonRoles" (
            "PersonID" TEXT NOT NULL,
            "RoleID" INTEGER NOT NULL,
            FOREIGN KEY ("PersonID") REFERENCES "Person" ("PersonID"),
            FOREIGN KEY ("RoleID") REFERENCES "Role" ("RoleID"),
            PRIMARY KEY ("PersonID", "RoleID")
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

    def role_exists_for_person(self, person_id, role):
        """ Check if the specified role exists for the given person """
        results = self.execute_query("SELECT 1 FROM Person WHERE PersonID = ? AND Role = ?;", (person_id, role))
        return len(results) > 0

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
            
            # if query starts with 'SELECT'
            if query.strip().upper().startswith('SELECT'):
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
        
    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            print("\n= Database connection closed =")