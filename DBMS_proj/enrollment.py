from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
import ttkthemes
import time

# Clock function to display current date and time
def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# Slide function for dynamic text
count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

# Create input form in a new window for Add, Update, or Search Enrollment
def top_data(title, button_text, command):
    global idEntry, studentNameEntry, courseNameEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.geometry('500x300+15+120')
    screen.grab_set()
    screen.resizable(False, False)

    # Enrollment ID
    idLabel = Label(screen, text='Enrollment ID:', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=25, padx=10)

    # Student Name
    studentLabel = Label(screen, text='Student Name:', font=('times new roman', 20, 'bold'))
    studentLabel.grid(row=1, column=0, padx=20, sticky=W)
    studentNameEntry = Entry(screen, font=('roman', 15, 'bold'))
    studentNameEntry.grid(row=1, column=1, pady=25, padx=10)

    # Course Name
    courseLabel = Label(screen, text='Course Name:', font=('times new roman', 20, 'bold'))
    courseLabel.grid(row=2, column=0, padx=20, sticky=W)
    courseNameEntry = Entry(screen, font=('roman', 15, 'bold'))
    courseNameEntry.grid(row=2, column=1, pady=25, padx=10)

    # Submit button
    button = Button(screen, text=button_text, width=10, font=('times new roman', 13, 'bold'), bg='dodger blue', command=command)
    button.grid(row=3, column=0, pady=20)
    clear_button = Button(screen, text='Clear', width=10, font=('times new roman', 13, 'bold'), bg='dodger blue', command=clear_fields)
    clear_button.grid(row=3, column=1, pady=20)
    
    
    if title=='Update Enrollment':
        indexing=enrollmentTable.focus()
        content=enrollmentTable.item(indexing)
        listdata=content['values'] #listdata selects and stores the complete row which u want
        # after selecting a row the information stored in their place..mainly in the update box
        idEntry.insert(0, listdata[0])
        studentNameEntry.insert(0, listdata[1])
        courseNameEntry.insert(0,listdata[2])

def clear_fields():
    idEntry.delete(0, END)
    studentNameEntry.delete(0, END)
    courseNameEntry.delete(0, END)

def connect():
    global mycursor, con
    try:
        con = pymysql.connect(host='localhost', user='root', password='qwerty1234', database='student_db')
        mycursor = con.cursor()
        messagebox.showinfo('Success', 'Database Connection Successful')
        toggle_buttons(NORMAL)
    except Exception as e:
        messagebox.showerror('Error', f'Failed to connect: {e}', parent=root)


def toggle_buttons(state):
    addEnrollmentButton.config(state=state)
    searchEnrollmentButton.config(state=state)
    updateEnrollmentButton.config(state=state)
    showEnrollmentButton.config(state=state)
    deleteEnrollmentButton.config(state=state)
    exitbutton.config(state=state)
    
def add_data():
    if studentNameEntry.get() == '' or courseNameEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            # Check if the enrollment_id already exists in the database
            enrollment_id = idEntry.get()
            mycursor.execute('SELECT enrollment_id FROM enrollment WHERE enrollment_id=%s', (enrollment_id,))
            existing_id = mycursor.fetchone()

            if existing_id:
                messagebox.showerror('Error', 'Enrollment ID already exists', parent=screen)
            else:
                # Get the student_id and course_id based on the names entered
                mycursor.execute('SELECT id FROM student WHERE name=%s', (studentNameEntry.get(),))
                student_id = mycursor.fetchone()

                mycursor.execute('SELECT course_id FROM course WHERE course_name=%s', (courseNameEntry.get(),))
                course_id = mycursor.fetchone()

                # If student_id or course_id is not found, show error
                if not student_id:
                    messagebox.showerror('Error', 'Student Name not found.', parent=screen)
                elif not course_id:
                    messagebox.showerror('Error', 'Course Name not found.', parent=screen)
                else:
                    student_id = student_id[0]  # Extract student_id
                    course_id = course_id[0]    # Extract course_id
                    
                    # Insert into enrollment table using student_id and course_id
                    query = 'INSERT INTO enrollment (enrollment_id, student_id, course_id, enrollment_date) VALUES (%s, %s, %s, CURDATE())'
                    mycursor.execute(query, (enrollment_id, student_id, course_id))
                    con.commit()
                    messagebox.showinfo('Success', 'Enrollment added successfully', parent=screen)
                    screen.destroy()
                    show_enrollments()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add enrollment: {e}', parent=screen)

def update_data():
    if studentNameEntry.get() == '' or courseNameEntry.get() == '' or idEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            # Get the student_id based on the entered student name
            mycursor.execute('SELECT id FROM student WHERE name=%s', (studentNameEntry.get(),))
            student_id = mycursor.fetchone()

            # Get the course_id based on the entered course name
            mycursor.execute('SELECT course_id FROM course WHERE course_name=%s', (courseNameEntry.get(),))
            course_id = mycursor.fetchone()

            if not student_id:
                messagebox.showerror('Error', 'Student name does not exist!!', parent=screen)
            elif not course_id:
                messagebox.showerror('Error', 'Course name does not exist!!', parent=screen)
            else:
                student_id = student_id[0]
                course_id = course_id[0]

                # Ensure that the enrollment ID is valid and exists
                mycursor.execute('SELECT * FROM enrollment WHERE enrollment_id=%s', (idEntry.get(),))
                existing_enrollment = mycursor.fetchone()
                if not existing_enrollment:
                    messagebox.showerror('Error', f'Enrollment ID {idEntry.get()} does not exist!', parent=screen)
                    return

                # Update the enrollment record in the database
                query = 'UPDATE enrollment SET student_id=%s, course_id=%s WHERE enrollment_id=%s'
                mycursor.execute(query, (student_id, course_id, idEntry.get()))
                con.commit()

                messagebox.showinfo('Success', f'Enrollment {idEntry.get()} updated successfully', parent=screen)
                screen.destroy()
                show_enrollments()  # Refresh the enrollment list after the update
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update enrollment: {e}', parent=screen)



def delete_data():
    indexing = enrollmentTable.focus()
    content = enrollmentTable.item(indexing)
    content_id = content['values'][0]

    # Check for selected row before deletion
    if content_id:
        query = 'DELETE FROM enrollment WHERE enrollment_id=%s'
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Enrollment with ID {content_id} has been deleted.')
        show_enrollments()
    else:
        messagebox.showwarning("No Selection", "Please select an enrollment to delete")


# Search student function
def search_data():
    query = '''SELECT e.enrollment_id, s.name, c.course_name, e.enrollment_date 
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        JOIN course c ON e.course_id = c.course_id
        WHERE e.enrollment_id=%s OR s.name=%s OR c.course_name=%s'''

    mycursor.execute(query, (idEntry.get(),
                            studentNameEntry.get(),
                            courseNameEntry.get()
                            ))
    enrollmentTable.delete(*enrollmentTable.get_children()) # No need for previous data
    fetched_data = mycursor.fetchall()
    # Check if no data was found
    if not fetched_data:
        messagebox.showerror("Error", "No data found for the given search criteria.")
    else:
        for data in fetched_data:
            enrollmentTable.insert('', END, values=data)
    screen.destroy()  # After clicking search, the search student window will close


# Display all enrollments
def show_enrollments():
    try:
        query = 'SELECT e.enrollment_id, s.name, c.course_name, e.enrollment_date ' \
                'FROM enrollment e ' \
                'JOIN student s ON e.student_id = s.id ' \
                'JOIN course c ON e.course_id = c.course_id'

        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        
        # Update the enrollmentTable with all enrollments
        enrollmentTable.delete(*enrollmentTable.get_children())
        for data in fetched_data:
            enrollmentTable.insert('', END, values=data)
    except Exception as e:
        messagebox.showerror('Error', f'Failed to fetch enrollments: {e}', parent=root)


def exit():
    r=messagebox.askyesno('Exit','Do You Want To Exit?')
    if r:
        root.destroy()
    else:
        pass


# GUI Initialization
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1530x800+0+0')
root.resizable(0, 0)
root.title('Enrollment Management System')

# Clock and Slider
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=0, y=7)
clock()
s = 'Enrollment Management System.'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=400, y=30)
slider()

# Connect Database Button
connectButton = ttk.Button(root, text='Connect Database', command=connect)
connectButton.place(x=1340, y=34)

# Left Frame for Buttons
leftFrame = Frame(root)
leftFrame.place(x=50, y=100, width=300, height=700)

# Adding a Logo Image (replace with your own file path)
logo_image = PhotoImage(file='students.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0, pady=40)

addEnrollmentButton = ttk.Button(leftFrame, text='Add Enrollment', width=25, state=DISABLED, command=lambda: top_data('Add Enrollment', 'SUBMIT', add_data))
addEnrollmentButton.grid(row=1, column=0, pady=20)
searchEnrollmentButton = ttk.Button(leftFrame, text='Search Enrollment', width=25, state=DISABLED, command=lambda: top_data('Search Enrollment', 'SEARCH', search_data))
searchEnrollmentButton.grid(row=2, column=0, pady=20)
updateEnrollmentButton = ttk.Button(leftFrame, text='Update Enrollment', width=25, state=DISABLED, command=lambda: top_data('Update Enrollment', 'UPDATE', update_data))
updateEnrollmentButton.grid(row=3, column=0, pady=20)
deleteEnrollmentButton = ttk.Button(leftFrame, text='Delete Enrollment', width=25, state=DISABLED, command=delete_data)
deleteEnrollmentButton.grid(row=4, column=0, pady=20)
showEnrollmentButton = ttk.Button(leftFrame, text='Show Enrollments', width=25, state=DISABLED, command=show_enrollments)
showEnrollmentButton.grid(row=5, column=0, pady=20)
exitbutton = ttk.Button(leftFrame, text="Exit", width=25, command=exit)
exitbutton.grid(row=6, column=0, pady=20)

# Right Frame for Enrollment Table
rightFrame = Frame(root)
rightFrame.place(x=400, y=170, width=1000, height=600)

#scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
enrollmentTable = ttk.Treeview(rightFrame, columns=('Enrollment ID', 'Student Name', 'Course Name', 'Enrollment Date'), yscrollcommand=scrollBarY.set)
# scrollBarX.config(command=enrollmentTable.xview)
# scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.config(command=enrollmentTable.yview)

scrollBarY.pack(side=RIGHT, fill=Y)
enrollmentTable.pack(fill=BOTH, expand=1)
enrollmentTable.heading('Enrollment ID', text='Enrollment ID')
enrollmentTable.heading('Student Name', text='Student Name')
enrollmentTable.heading('Course Name', text='Course Name')
enrollmentTable.heading('Enrollment Date', text='Enrollment Date')



#align rows infrom centre with height  & width
enrollmentTable.column('Enrollment ID',width=60,anchor=CENTER)
enrollmentTable.column('Student Name',width=160,anchor=CENTER)
enrollmentTable.column('Course Name',width=160,anchor=CENTER)
enrollmentTable.column('Enrollment Date',width=200,anchor=CENTER)



style=ttk.Style()

#style.configure('Treeview',rowheight=25,font= ('arial',15,'bold'),foreground='red4',background='yellow',fieldbackground='red')
style.configure('Treeview',rowheight=35,font= ('arial',13),bg='white')

#style changing of upper subheads
style.configure('Treeview.Heading',font=('classic',14,'bold'),foreground='red')


enrollmentTable.config(show='headings')

root.mainloop()





