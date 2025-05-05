from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector
import time

# Establish connection to the database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",       # Replace with your MySQL username
        password="qwerty1234",    # Replace with your MySQL password
        database="student_db"     # Replace with your database name
    )
    mycursor = db.cursor()
except mysql.connector.Error as e:
    messagebox.showerror("Database Connection Error", f"An error occurred: {e}")

def student_form():
    subprocess.Popen(['python', 'student.py'])
    #window.after(100, update_counts)
    
def course_form():
    subprocess.Popen(['python', 'course.py'])
    window.after(500, update_counts)

def department_form():
    subprocess.Popen(['python', 'department.py'])
    window.after(100, update_counts)
    
def enrollment_form():
    subprocess.Popen(['python', 'enrollment.py'])
    window.after(100, update_counts)
    
def grade_form():
    subprocess.Popen(['python', 'grade.py'])
    window.after(100, update_counts)


# Logout function
def logout():
    window.destroy()  # Close the dashboard window
    subprocess.Popen(['python', 'login.py'])


# Exit function
def exit_app():
    window.destroy()
    
    
# Functions to get counts for dashboard statistics
def get_student_count():
    try:
        query = "SELECT COUNT(*) FROM student"
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return 0
    
def get_course_count():
    try:
        query = "SELECT COUNT(*) FROM course"
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return 0


# Function to get department count
def get_department_count():
    try:
        query = "SELECT COUNT(*) FROM department"
        mycursor.execute(query)
        count = mycursor.fetchone()[0]
        return count
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return 0
    
def get_enrollment_count():
    try:
        query = "SELECT COUNT(*) FROM enrollment"
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return 0

# Function to update counts onac the dashboard
def update_counts():
        tot_stud_cou_label.config(text=str(get_student_count()))
        cou_count_label.config(text=str(get_course_count()))
        dept_cou_label.config(text=str(get_department_count()))
        enroll_cou_label.config(text=str(get_enrollment_count()))
        window.after(1000, update_counts)
        

# Function to update the current date and time in the subtitle label
def update_datetime():
    current_time = time.strftime("%I:%M:%S %p")  # Current time in 12-hour format with AM/PM
    current_date = time.strftime("%d-%m-%Y")  # Current date in dd-mm-yyyy format
    subtitleLabel.config(text=f"Welcome Admin\t\t\t\t\t Date:{current_date}\t\t\t Time:{current_time}")
    window.after(1000, update_datetime)  # Update the time every 1000ms (1 second)



# dashboard window
window = Tk()
window.title('Dashboard')
window.geometry('1530x900+0+0')
window.resizable(0, 0)
window.config(bg='white')

bg_image = PhotoImage(file='dash1.png')

titleLabel = Label(window, image=bg_image, compound=LEFT, text='      Student Management System',
                font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=30)
titleLabel.place(x=0, y=0, relwidth=1)

logooutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48',command=logout)
logooutButton.place(x=1370, y=10)

subtitleLabel = Label(window, text="Welcome Admin\t\t\t\t\t Date:26-10-2024\t\t\t Time:12:14 am",
                    font=('times new roman', 16), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)
update_datetime()

leftFrame = Frame(window)
leftFrame.place(x=0, y=102, width=300, height=800)

logoimage = PhotoImage(file='d2.png')
ImageLabel = Label(leftFrame, image=logoimage)
ImageLabel.pack()

menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 29), bg='#009688')
menuLabel.pack(fill=X)

stud_icon = PhotoImage(file='stud2.png')
student_button = Button(leftFrame, text=' Students', image=stud_icon, compound=LEFT,
                        font=('times new roman', 26, 'bold'), anchor='w', padx=10, command=student_form)
student_button.pack(fill=X)

course_icon = PhotoImage(file='course.png')
course_button = Button(leftFrame, text=' Course', image=course_icon, compound=LEFT,
                    font=('times new roman', 26, 'bold'), anchor='w', padx=10,command=course_form)
course_button.pack(fill=X)


depart_icon = PhotoImage(file='fac.png')
depart_button = Button(leftFrame, text=' Department', image=depart_icon, compound=LEFT,
                        font=('times new roman', 26, 'bold'), anchor='w', padx=10, command=department_form)
depart_button.pack(fill=X)

enrol_icon = PhotoImage(file='enrol.png')
enrol_button = Button(leftFrame, text=' Enrollment', image=enrol_icon, compound=LEFT,
                    font=('times new roman', 26, 'bold'), anchor='w', padx=10,command=enrollment_form)
enrol_button.pack(fill=X)

grade_icon = PhotoImage(file='grade.png')
grade_button = Button(leftFrame, text=' Grade', image=grade_icon, compound=LEFT,
                    font=('times new roman', 26, 'bold'), anchor='w', padx=10,command=grade_form)
grade_button.pack(fill=X)

exit_icon = PhotoImage(file='exit.png')
exit_button = Button(leftFrame, text=' Exit', image=exit_icon, compound=LEFT,
                    font=('times new roman', 26, 'bold'), anchor='w', padx=10,command=exit_app)
exit_button.pack(fill=X)

# Creating cards for statistics
stud_frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
stud_frame.place(x=580, y=150, height=240, width=290)

tot_stud_icon = PhotoImage(file='tot.png')
tot_stud_icon_label = Label(stud_frame, image=tot_stud_icon, bg='#2C3E50')
tot_stud_icon_label.pack(pady=10)

tot_stud_label = Label(stud_frame, text='Total Students', font=('times new roman', 18, 'bold'), bg='#2C3E50', fg='white')
tot_stud_label.pack()

tot_stud_cou_label = Label(stud_frame, text='0', font=('times new roman', 31, 'bold'), bg='#2C3E50', fg='white')
tot_stud_cou_label.pack()

# Total course frame
cou_frame = Frame(window, bg='#27AE77', bd=3, relief=RIDGE)
cou_frame.place(x=950, y=150, height=240, width=290)
cou_icon = PhotoImage(file='cou.png')
cou_icon_label = Label(cou_frame, image=cou_icon, bg='#27AE77')
cou_icon_label.pack(pady=10)

cou_label = Label(cou_frame, text='Total Course', font=('times new roman', 18, 'bold'), bg='#27AE77', fg='white')
cou_label.pack()

cou_count_label = Label(cou_frame, text='0', font=('times new roman', 31, 'bold'), bg='#27AE77', fg='white')
cou_count_label.pack()

# Total department frame
dept_frame = Frame(window, bg='#E74366', bd=3, relief=RIDGE)
dept_frame.place(x=580, y=450, height=240, width=290)
dept_icon = PhotoImage(file='dept.png')
dept_icon_label = Label(dept_frame, image=dept_icon, bg='#E74366')
dept_icon_label.pack(pady=10)

dept_label = Label(dept_frame, text='Total Departments', font=('times new roman', 18, 'bold'), bg='#E74366', fg='white')
dept_label.pack()

dept_cou_label = Label(dept_frame, text='0', font=('times new roman', 31, 'bold'), bg='#E74366', fg='white')
dept_cou_label.pack()

# Total enrollments frame
enroll_frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
enroll_frame.place(x=950, y=450, height=240, width=290)
enroll_icon = PhotoImage(file='enroll.png')
enroll_icon_label = Label(enroll_frame, image=enroll_icon, bg='#2C3E50')
enroll_icon_label.pack(pady=10)

enroll_label = Label(enroll_frame, text='Total Enrollments', font=('times new roman', 18, 'bold'), bg='#2C3E50', fg='white')
enroll_label.pack()

enroll_cou_label = Label(enroll_frame, text='0', font=('times new roman', 31, 'bold'), bg='#2C3E50', fg='white')
enroll_cou_label.pack()

# Call update_counts to refresh data
update_counts()

window.mainloop()
