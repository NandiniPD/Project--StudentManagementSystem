# Student Management System

A comprehensive student management system built with Python and MySQL database.

## Project Overview

This Student Management System provides a user-friendly interface for managing student records, courses, departments, and grades. The system includes features for student enrollment, course management, grade tracking, and department administration.

## Features

- **User Authentication**
  - Secure login system
  - Role-based access control

- **Student Management**
  - Add, edit, and view student records
  - Track student information and academic progress

- **Course Management**
  - Create and manage courses
  - Assign courses to departments
  - Track course enrollment

- **Department Management**
  - Add and manage departments
  - Associate courses with departments

- **Grade Management**
  - Record and track student grades
  - Generate grade reports

- **Enrollment System**
  - Manage student course enrollment
  - Track enrollment status

## Project Structure

- `login.py` - User authentication and login system
- `dashboard.py` - Main application dashboard(Main file to run)
- `student.py` - Student management module
- `course.py` - Course management module
- `department.py` - Department management module
- `grade.py` - Grade management module
- `enrollment.py` - Enrollment management module

## Requirements

- Python 3.x
- MySQL Server
- Required Python packages:
  - tkinter
  - PIL (Python Imaging Library)
  - mysql-connector-python

## Installation

1. Clone the repository
2. Ensure Python 3.x is installed on your system
3. Install required packages:
   ```bash
   pip install pillow mysql-connector-python
   ```
4. Set up your MySQL database and update the connection details in the code
5. Run the application:
   ```bash
   python login.py
   ```

## Usage

1. Launch the application using `login.py`
2. Log in with your credentials
3. Navigate through the dashboard to access different features
4. Use the respective modules to manage students, courses, departments, and grades

## Database

The system uses MySQL as its database management system. The database stores all the application data including:
- User information
- Student records
- Course details
- Department information
- Grade records
- Enrollment data

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## License

This project is open-source and available under the MIT License. 