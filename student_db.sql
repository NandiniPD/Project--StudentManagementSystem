CREATE DATABASE student_db;
USE student_db;

CREATE TABLE student(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30),
    dept_Id INT,
    FOREIGN KEY (dept_Id) REFERENCES department(dept_Id),
	mobile VARCHAR(10),
    email VARCHAR(30) ,
    address VARCHAR(100),
    gender VARCHAR(30),
    dob VARCHAR(50),
    date VARCHAR(50),
    time VARCHAR(50) 
);

CREATE TABLE department (
    dept_Id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

desc Student;
/*show all data ----------*/
select * from student;
select * from department;
/* Search-------------------*/
Select * from student where id=1;
Select * from student where name='XYZ';
Select * from student where id=1 or name='XYZ';
/*update data------------*/

update student set name='harini' where id=4;

/* Delete-------------*/
delete from student where id=3;




CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    dept_id INT,
    duration VARCHAR(50),
    credits INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
    );


drop table course;
drop table enrollment;
select * from course;




CREATE TABLE enrollment (
            enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT,
            course_id INT,
            enrollment_date DATE,
            FOREIGN KEY (student_id) REFERENCES student(id),
            FOREIGN KEY (course_id) REFERENCES course(course_id)
);
select * from enrollment;
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INt,
    grade CHAR(2),
    semester INT,
    year YEAR,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

select * from grades;
drop table grades;
select * from student;

show tables;