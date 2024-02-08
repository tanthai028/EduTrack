-- Use the .sql extension when saving this script.
-- Begin transaction to execute all or nothing.
BEGIN TRANSACTION;

-- Create 'Course' table
CREATE TABLE IF NOT EXISTS "Course" (
  "CourseID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "CourseName" TEXT NOT NULL,
  "CourseDescription" TEXT,
  "CreditHours" INTEGER NOT NULL
);

-- Create 'Instructor' table
CREATE TABLE IF NOT EXISTS "Instructor" (
  "InstructorID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "FirstName" TEXT NOT NULL,
  "LastName" TEXT NOT NULL,
  "Email" TEXT NOT NULL UNIQUE,
  "OfficeNumber" TEXT
);

-- Create 'Assignment' table
CREATE TABLE IF NOT EXISTS "Assignment" (
  "AssignmentID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "CourseID" INTEGER NOT NULL,
  "AssignmentName" TEXT NOT NULL,
  "Description" TEXT,
  "DueDate" TEXT NOT NULL,
  FOREIGN KEY ("CourseID") REFERENCES "Course" ("CourseID")
);

-- Assuming a 'Student' table exists with the following structure:
-- If it does not exist, this needs to be created as well.
CREATE TABLE IF NOT EXISTS "Student" (
  "StudentID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "FirstName" TEXT NOT NULL,
  "LastName" TEXT NOT NULL,
  "Email" TEXT NOT NULL UNIQUE,
  "PhoneNumber" TEXT,
  "DateOfBirth" TEXT
);

-- Create 'Enrollment' table
CREATE TABLE IF NOT EXISTS "Enrollment" (
  "EnrollmentID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "StudentID" INTEGER NOT NULL,
  "CourseID" INTEGER NOT NULL,
  "EnrollmentDate" TEXT NOT NULL,
  "Grade" TEXT,
  FOREIGN KEY ("StudentID") REFERENCES "Student" ("StudentID"),
  FOREIGN KEY ("CourseID") REFERENCES "Course" ("CourseID")
);

-- Create 'Submission' table
CREATE TABLE IF NOT EXISTS "Submission" (
  "SubmissionID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "AssignmentID" INTEGER NOT NULL,
  "StudentID" INTEGER NOT NULL,
  "SubmissionDate" TEXT NOT NULL,
  "Grade" TEXT,
  "Feedback" TEXT,
  FOREIGN KEY ("AssignmentID") REFERENCES "Assignment" ("AssignmentID"),
  FOREIGN KEY ("StudentID") REFERENCES "Student" ("StudentID")
);

-- Commit the transaction to finalize the changes.
COMMIT;
