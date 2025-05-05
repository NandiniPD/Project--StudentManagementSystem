from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pymysql
import ttkthemes
import time

# Removed the import from grade module
# from grade import delete_data

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



original_course_id = None

# Create input form in a new window for Add, Update, or Search Course
def top_data(title, button_text, command):
    global courseIdEntry, courseNameEntry, durationEntry, creditsEntry, deptIDEntry, screen,original_course_id
    screen = Toplevel()
    screen.title(title)
    screen.geometry('500x500+15+120')  # Increased height
    screen.grab_set()
    screen.resizable(False, False)

    # Course ID
    courseIdLabel = Label(screen, text='Course ID:', font=('times new roman', 20, 'bold'))
    courseIdLabel.grid(row=0, column=0, padx=20, sticky=W)
    courseIdEntry = Entry(screen, font=('roman', 15, 'bold'))
    courseIdEntry.grid(row=0, column=1, pady=25, padx=10)

    # Course Name
    courseNameLabel = Label(screen, text='Course Name:', font=('times new roman', 20, 'bold'))
    courseNameLabel.grid(row=1, column=0, padx=20, sticky=W)
    courseNameEntry = Entry(screen, font=('roman', 15, 'bold'))
    courseNameEntry.grid(row=1, column=1, pady=25, padx=10)

    # Department ID (new field to reference department table)
    deptIDLabel = Label(screen, text='Department ID:', font=('times new roman', 20, 'bold'))
    deptIDLabel.grid(row=2, column=0, padx=20, sticky=W)
    deptIDEntry = Entry(screen, font=('roman', 15, 'bold'))
    deptIDEntry.grid(row=2, column=1, pady=25, padx=10)

    # Duration
    durationLabel = Label(screen, text='Duration:', font=('times new roman', 20, 'bold'))
    durationLabel.grid(row=3, column=0, padx=20, sticky=W)
    durationEntry = Entry(screen, font=('roman', 15, 'bold'))
    durationEntry.grid(row=3, column=1, pady=25, padx=10)

    # Credits
    creditsLabel = Label(screen, text='Credits:', font=('times new roman', 20, 'bold'))
    creditsLabel.grid(row=4, column=0, padx=20, sticky=W)
    creditsEntry = Entry(screen, font=('roman', 15, 'bold'))
    creditsEntry.grid(row=4, column=1, pady=25, padx=10)

    # Submit button
    button = Button(screen, text=button_text, width=10, font=('times new roman', 13, 'bold'), bg='dodger blue',
                    command=command)
    button.grid(row=6, column=0, pady=15, padx=30, sticky=W)

    # Clear button
    clear_button = Button(screen, text='Clear', width=10, font=('times new roman', 13, 'bold'), bg='dodger blue',
                        command=clear_fields)
    clear_button.grid(row=6, column=1, pady=10, padx=30, sticky=E)

    if title == 'Update Course':
        indexing = courseTable.focus()
        content = courseTable.item(indexing)
        listdata = content['values']
        courseIdEntry.insert(0, listdata[0])
        courseNameEntry.insert(0, listdata[1])
        deptIDEntry.insert(0, listdata[2])
        durationEntry.insert(0, listdata[3])
        creditsEntry.insert(0, listdata[4])
        # Store original course_id
        original_course_id = listdata[0]

def clear_fields():
    courseIdEntry.delete(0, END)
    courseNameEntry.delete(0, END)
    deptIDEntry.delete(0, END)
    durationEntry.delete(0, END)
    creditsEntry.delete(0, END)

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
    addCourseButton.config(state=state)
    searchCourseButton.config(state=state)
    updateCourseButton.config(state=state)
    showCourseButton.config(state=state)
    deleteCourseButton.config(state=state)
    exitbutton.config(state=state)

# Functions for adding, updating, searching, showing, and deleting data
def add_course():
    if courseNameEntry.get() == '' or deptIDEntry.get() == '' or durationEntry.get() == '' or creditsEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            # Check if department ID exists in the department table
            dept_id = deptIDEntry.get()
            mycursor.execute('SELECT dept_id FROM department WHERE dept_id = %s', (dept_id,))
            department_exists = mycursor.fetchone()

            if not department_exists:
                messagebox.showerror('Error', 'Invalid Department ID', parent=screen)
            else:
                # Insert into course table if department ID exists
                course_id=courseIdEntry.get()
                course_name = courseNameEntry.get()
                duration = durationEntry.get()
                credits = creditsEntry.get()
                query = 'INSERT INTO course (course_id,course_name, dept_id, duration, credits) VALUES (%s,%s, %s, %s, %s)'
                mycursor.execute(query, (course_id,course_name, dept_id, duration, credits))
                con.commit()
                messagebox.showinfo('Success', 'Course added successfully', parent=screen)
                screen.destroy()
                show_courses()  # Refresh course list
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add course: {e}', parent=screen)
            
            
def update_course():
    global original_course_id
    if courseNameEntry.get() == '' or durationEntry.get() == '' or creditsEntry.get() == '' or courseIdEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        try:
            # Get updated course ID and details
            new_course_id = courseIdEntry.get()
            course_name = courseNameEntry.get()
            dept_id = deptIDEntry.get()
            duration = durationEntry.get()
            credits = creditsEntry.get()

            # Check if new_course_id is taken by another course
            mycursor.execute('SELECT course_id FROM course WHERE course_id=%s AND course_id != %s', 
                             (new_course_id, original_course_id))
            result = mycursor.fetchone()

            if result is None:
                # Proceed with updating the course details
                query = '''
                UPDATE course SET 
                    course_id = %s, 
                    course_name = %s, 
                    dept_id = %s, 
                    duration = %s, 
                    credits = %s 
                WHERE course_id = %s
                '''
                mycursor.execute(query, (new_course_id, course_name, dept_id, duration, credits, original_course_id))
                con.commit()
                
                messagebox.showinfo('Success', 'Course updated successfully!', parent=screen)
                screen.destroy()
                show_courses()  # Refresh course list
            else:
                messagebox.showerror('Error', f'Course ID {new_course_id} already exists. Please choose a different ID.', parent=screen)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to update course: {e}', parent=screen)




def delete_data():
    selected_item = courseTable.focus()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a course to delete")
        return

    content = courseTable.item(selected_item)
    content_id = content['values'][0]

    if content_id:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Course ID {content_id}?")
        if confirm:
            try:
                query = 'DELETE FROM course WHERE course_id=%s'
                mycursor.execute(query, (content_id,))
                con.commit()
                messagebox.showinfo('Deleted', f'Course with ID {content_id} has been deleted.')
                show_courses()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to delete course: {e}', parent=root)
    else:
        messagebox.showwarning("No Selection", "Please select a course to delete")
        
        
def search_course():
    search_id = courseIdEntry.get().strip()
    search_name = courseNameEntry.get().strip()

    if not search_id and not search_name:
        messagebox.showwarning("Input Error", "Please enter Course ID or Course Name to search.")
        return

    if search_id and not search_name:
        query = 'SELECT course_id, course_name, dept_id, duration, credits FROM course WHERE course_id=%s'
        mycursor.execute(query, (search_id,))
    elif not search_id and search_name:
        query = 'SELECT course_id, course_name, dept_id, duration, credits FROM course WHERE course_name LIKE %s'
        mycursor.execute(query, (f"%{search_name}%",))
    else:
        query = '''SELECT course_id, course_name, dept_id, duration, credits FROM course WHERE course_id=%s AND course_name LIKE %s'''
        mycursor.execute(query, (search_id, f"%{search_name}%"))

    courseTable.delete(*courseTable.get_children())
    fetched_data = mycursor.fetchall()

    if not fetched_data:
        messagebox.showerror("Error", "No data found for the given search criteria.")
    else:
        for data in fetched_data:
            courseTable.insert('', END, values=data)
    screen.destroy()


def show_courses():
    try:
        query = 'SELECT course_id, course_name, dept_id, duration, credits FROM course'
        mycursor.execute(query)
        courseTable.delete(*courseTable.get_children())
        fetched_data = mycursor.fetchall()

        if not fetched_data:
            messagebox.showerror('Error', 'No courses found', parent=root)

        for data in fetched_data:
            courseTable.insert('', END, values=data)
    except Exception as e:
        messagebox.showerror('Error', f'Failed to load courses: {e}', parent=root)

def exit_app():
    r = messagebox.askyesno('Exit', 'Do You Want To Exit?')
    if r:
        root.destroy()

# GUI Initialization
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1530x800+0+0')
root.resizable(0, 0)
root.title('Course Management System')

# Clock and Slider
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=0, y=7)
clock()
s = 'Course Management System.'
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
logo_Label.grid(row=0, column=0,pady=40)

addCourseButton = ttk.Button(leftFrame, text='Add Course', width=25, state=DISABLED,
                            command=lambda: top_data('Add Course', 'SUBMIT', add_course))
addCourseButton.grid(row=1, column=0, pady=20)
searchCourseButton = ttk.Button(leftFrame, text='Search Course', width=25, state=DISABLED,
                                command=lambda: top_data('Search Course', 'SEARCH', search_course))
searchCourseButton.grid(row=2, column=0, pady=20)
updateCourseButton = ttk.Button(leftFrame, text='Update Course', width=25, state=DISABLED,
                                command=lambda: top_data('Update Course', 'UPDATE', update_course))
updateCourseButton.grid(row=3, column=0, pady=20)
deleteCourseButton = ttk.Button(leftFrame, text='Delete Course', width=25, state=DISABLED, command=delete_data)
deleteCourseButton.grid(row=4, column=0, pady=20)
showCourseButton = ttk.Button(leftFrame, text='Show Courses', width=25, state=DISABLED,
                            command=show_courses)
showCourseButton.grid(row=5, column=0, pady=20)
exitbutton = ttk.Button(leftFrame, text="Exit", width=25, command=exit_app)
exitbutton.grid(row=6, column=0, pady=20)

# Right Frame for Course Table
rightFrame = Frame(root)
rightFrame.place(x=400, y=170, width=1000, height=600)

scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
courseTable = ttk.Treeview(rightFrame, columns=('Course ID', 'Course Name', 'Dept ID', 'Duration', 'Credits'),
                        yscrollcommand=scrollBarY.set)
scrollBarY.config(command=courseTable.yview)

scrollBarY.pack(side=RIGHT, fill=Y)
courseTable.pack(fill=BOTH, expand=1)
courseTable.heading('Course ID', text='Course ID')
courseTable.heading('Course Name', text='Course Name')
courseTable.heading('Dept ID', text='Department ID')  # Added Dept ID
courseTable.heading('Duration', text='Duration')
courseTable.heading('Credits', text='Credits')

courseTable.column('Course ID', width=60, anchor=CENTER)
courseTable.column('Course Name', width=160, anchor=CENTER)
courseTable.column('Dept ID', width=100, anchor=CENTER)  # Set appropriate width
courseTable.column('Duration', width=100, anchor=CENTER)
courseTable.column('Credits', width=80, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=35, font=('arial', 13), bg='white')
style.configure('Treeview.Heading', font=('classic', 14, 'bold'), foreground='red')

courseTable.config(show='headings')

root.mainloop()
