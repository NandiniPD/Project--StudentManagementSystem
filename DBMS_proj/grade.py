from tkinter import *
import time
from tkinter import messagebox
import ttkthemes
import tkinter as tk
from tkinter import ttk
import pymysql
import datetime

# Clock Function to display time and date
def clock():
    global date, currenttime
    date = datetime.date.today()  # Get today's date
    date = date.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD
    currenttime = time.strftime('%H:%M:%S')  # Time format: hour:minute:second
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# Slider function
count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text += s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)
def top_data(title, button_text, command):
    global studentNameEntry, courseNameEntry, gradeEntry, percentageEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    screen.geometry('430x400+15+120')

    # Student Name
    studentNameLabel = Label(screen, text='Student Name:', font=('times new roman', 20, 'bold'))
    studentNameLabel.grid(row=0, column=0, padx=20, sticky=W)
    studentNameEntry = Entry(screen, font=('roman', 15, 'bold'))
    studentNameEntry.grid(row=0, column=1, pady=25, padx=10)

    # Course Name
    courseNameLabel = Label(screen, text='Course Name:', font=('times new roman', 20, 'bold'))
    courseNameLabel.grid(row=1, column=0, padx=20, sticky=W)
    courseNameEntry = Entry(screen, font=('roman', 15, 'bold'))
    courseNameEntry.grid(row=1, column=1, pady=25, padx=10)

    # Grade
    gradeLabel = Label(screen, text='Grade:', font=('times new roman', 20, 'bold'))
    gradeLabel.grid(row=2, column=0, padx=20, sticky=W)
    gradeEntry = Entry(screen, font=('roman', 15, 'bold'))
    gradeEntry.grid(row=2, column=1, pady=25, padx=10)

    # Percentage (input with % sign auto-added)
    percentageLabel = Label(screen, text='Percentage:', font=('times new roman', 20, 'bold'))
    percentageLabel.grid(row=3, column=0, padx=20, sticky=W)
    percentageEntry = Entry(screen, font=('roman', 15, 'bold'))
    percentageEntry.grid(row=3, column=1, pady=25, padx=10)

    # Bind the event to append % when entering percentage
    percentageEntry.bind("<KeyRelease>", append_percentage)

    button = tk.Button(screen, text=button_text, width=10, font=('times new roman', 13, 'bold'),
                    bg='dodger blue', activebackground='green2',
                    command=command if button_text != 'SEARCH' else lambda: [command(), screen.destroy()])
    button.grid(row=4, column=0, columnspan=1, ipady=5, padx=5)
    clear_button = tk.Button(screen, text='Clear', width=10, font=('times new roman', 13, 'bold'),
                            bg='dodger blue', activebackground='green2', command=clear_fields)
    clear_button.grid(row=4, column=1, columnspan=1, ipady=5, padx=5)

def append_percentage(event):
    """Ensure that '%' sign is added automatically."""
    value = percentageEntry.get()
    if value and not value.endswith('%'):
        percentageEntry.delete(0, END)
        percentageEntry.insert(0, value + '%')
        

# Update average and total percentage labels when data changes
def update_avg_total():
    # Calculate the total and average percentage from the grades table
    total_percentage = 0
    count = 0
    gradeTable_data = gradeTable.get_children()
    
    for item in gradeTable_data:
        percentage = gradeTable.item(item)['values'][4].replace('%', '')  # Get percentage value without '%'
        if percentage:
            total_percentage += float(percentage)  # Sum all percentages
            count += 1

    # Calculate average
    avg_percentage = (total_percentage / count) if count > 0 else 0

    # Update the labels with calculated values
    avg_label.config(text=f"Average Percentage: {avg_percentage:.2f}%")
    total_label.config(text=f"Total Percentage: {total_percentage:.2f}%")


def clear_fields():
    studentNameEntry.delete(0, END)
    courseNameEntry.delete(0, END)
    gradeEntry.delete(0, END)
    percentageEntry.delete(0, END)
def add_data():
    if studentNameEntry.get() == '' or courseNameEntry.get() == '' or gradeEntry.get() == '' or percentageEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required', parent=screen)
    else:
        try:
            # Retrieve student_id based on student name
            mycursor.execute('SELECT id FROM student WHERE name = %s', (studentNameEntry.get(),))
            student_id = mycursor.fetchone()  # Should return (id,) or None if not found
            
            # Retrieve course_id based on course name
            mycursor.execute('SELECT course_id FROM course WHERE course_name = %s', (courseNameEntry.get(),))
            course_id = mycursor.fetchone()  # Should return (course_id,) or None if not found
            
            # Check if both student_id and course_id are found
            if student_id is None or course_id is None:
                messagebox.showerror('Error', 'Invalid Student or Course Name', parent=screen)
                return  # Exit the function if no valid IDs are found
            
            # Remove the '%' before saving to the database
            percentage = percentageEntry.get().replace('%', '')  
            
            # Insert the grade data into the 'grades' table
            query = 'INSERT INTO grades (student_id, course_id, grade, percentage, date) VALUES (%s, %s, %s, %s, %s)'
            mycursor.execute(query, (student_id[0], course_id[0], gradeEntry.get(), percentage, date))
            con.commit()  # Commit the changes to the database
            
            messagebox.showinfo('Success', 'Grade Added Successfully', parent=screen)
            clear_fields()  # Clear the input fields
            show_grades()  # Update the grade table view and total/average labels
            
        except Exception as e:
            # Log the specific exception to the console for debugging purposes
            print(f"Error: {e}")
            messagebox.showerror('Error', f'An error occurred: {e}', parent=screen)
        
        # Close the screen after operation (could be moved outside try-except if necessary)
        screen.destroy()

        
def delete_data():
    selected_item = gradeTable.selection()
    if selected_item:
        item_id = gradeTable.item(selected_item)['values'][0]  # Fetching the 'grade_id' column value
        query = 'DELETE FROM grades WHERE grade_id=%s'
        mycursor.execute(query, (item_id,))
        con.commit()
        messagebox.showinfo('Success', 'Grade Deleted Successfully')
        show_grades()
        update_avg_total()  # Update avg and total
    else:
        messagebox.showerror('Error', 'Please select a record to delete')

def search_data():
    student_name = studentNameEntry.get()
    if student_name:
        query = '''
            SELECT g.grade_id, s.name AS student_name, c.course_name, g.grade, g.percentage, g.date
            FROM grades g
            JOIN student s ON g.student_id = s.id
            JOIN course c ON g.course_id = c.course_id
            WHERE s.name = %s
        '''
        mycursor.execute(query, (student_name,))
        result = mycursor.fetchall()

        gradeTable.delete(*gradeTable.get_children())
        for data in result:
            data = list(data)  # Convert tuple to list to modify it
            # Format percentage with '%'
            if isinstance(data[4], (int, float)):
                data[4] = f"{data[4]}%"
            # Format date if it is a datetime.date object
            if isinstance(data[5], datetime.date):
                data[5] = data[5].strftime('%Y-%m-%d')
            gradeTable.insert('', END, values=data)
    else:
        messagebox.showerror('Error', 'Please enter a Student Name to search')


def update_data():
    selected_item = gradeTable.selection()
    if selected_item:
        item_id = gradeTable.item(selected_item)['values'][0]
        student_name = gradeTable.item(selected_item)['values'][1]
        course_name = gradeTable.item(selected_item)['values'][2]
        grade = gradeTable.item(selected_item)['values'][3]
        percentage = gradeTable.item(selected_item)['values'][4]  # Percentage field

        top_data("Update Grade", "Update", lambda: update_entry(item_id))
        
        studentNameEntry.insert(0, student_name)
        courseNameEntry.insert(0, course_name)
        gradeEntry.insert(0, grade)
        percentageEntry.insert(0, f"{percentage}%")  # Display percentage with '%'
    else:
        messagebox.showerror('Error', 'Please select a record to update')

def update_entry(item_id):
    if studentNameEntry.get() == '' or courseNameEntry.get() == '' or gradeEntry.get() == '' or percentageEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required', parent=screen)
    else:
        percentage = percentageEntry.get().replace('%', '')  # Remove '%' before saving to DB
        
        # Fetch student_id and course_id for the update
        mycursor.execute('SELECT id FROM student WHERE name = %s', (studentNameEntry.get(),))
        student_id = mycursor.fetchone()
        
        mycursor.execute('SELECT course_id FROM course WHERE course_name = %s', (courseNameEntry.get(),))
        course_id = mycursor.fetchone()
        
        if student_id and course_id:
            query = 'UPDATE grades SET student_id=%s, course_id=%s, grade=%s, percentage=%s WHERE grade_id=%s'
            mycursor.execute(query, (student_id[0], course_id[0], gradeEntry.get(), percentage, item_id))
            con.commit()
            messagebox.showinfo('Success', 'Grade Updated Successfully')
            screen.destroy()
            show_grades()
            update_avg_total()  # Update avg and total
        else:
            messagebox.showerror('Error', 'Invalid Student or Course Name', parent=screen)
def show_grades():
    gradeTable.delete(*gradeTable.get_children())  # Clear existing data

    # Fetch all data from the grades table and join with student and course to get names
    query = '''
        SELECT g.grade_id, s.name AS student_name, c.course_name, g.grade, g.percentage, g.date 
        FROM grades g
        JOIN student s ON g.student_id = s.id
        JOIN course c ON g.course_id = c.course_id
    '''
    mycursor.execute(query)
    rows = mycursor.fetchall()

    total_percentage = 0  # To store the total percentage
    count = 0  # To count the number of rows for average calculation

    for row in rows:
        row = list(row)  # Convert tuple to list to modify values
        percentage = str(row[4])  # Get percentage value as string
        date = row[5]  # Get the date value

        # Add '%' if not present in percentage
        if percentage and not percentage.endswith('%'):
            row[4] = f"{percentage}%"
        
        # Format the date as a string if it is a datetime.date object
        if isinstance(date, datetime.date):
            row[5] = date.strftime('%Y-%m-%d')

        # Insert the formatted row into the table
        gradeTable.insert('', END, values=row)

        # Calculate totals for average calculation
        total_percentage += float(percentage.replace('%', ''))
        count += 1

    # Calculate and display average and total percentage
    avg_percentage = (total_percentage / count) if count > 0 else 0
    avg_label.config(text=f"Average Percentage: {avg_percentage:.2f}%")
    total_label.config(text=f"Total Percentage: {total_percentage:.2f}%")

# Exit Application
def exit_app():
    r = messagebox.askyesno('Exit', 'Do You Want To Exit?')
    if r:
        root.destroy()

# Connect to Database
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
    for button in buttons:
        button.config(state=state)


# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1530x800+0+0')
root.resizable(0, 0)
root.title('Grade Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=0, y=7)
clock()

s = 'Grade Management System.'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=400, y=30)
slider()

connectButton = ttk.Button(root, text='Connect Database', command=connect)
connectButton.place(x=1340, y=34)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=700)

logo_image = PhotoImage(file='students.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0, pady=40)

avg_label = Label(leftFrame, text="Average Percentage: 0.00%", font=('times new roman', 14, 'bold'), fg="blue")
avg_label.grid(row=8, column=0, pady=1)

total_label = Label(leftFrame, text="Total Percentage: 0.00%", font=('times new roman', 14, 'bold'), fg="blue")
total_label.grid(row=7, column=0, pady=1)

buttons = [
    ttk.Button(leftFrame, text='Add Grade', width=25, state=DISABLED, command=lambda: top_data('Add Grade', 'SUBMIT', add_data)),
    ttk.Button(leftFrame, text='Delete Grade', width=25, state=DISABLED, command=delete_data),
    ttk.Button(leftFrame, text='Search Grade', width=25, state=DISABLED, command=lambda: top_data('Search Grade', 'SEARCH', search_data)),
    ttk.Button(leftFrame, text='Update Grade', width=25, state=DISABLED, command=update_data),
    ttk.Button(leftFrame, text='Show Grades', width=25, state=DISABLED, command=show_grades),
    ttk.Button(leftFrame, text='Exit', width=25, command=exit_app)
]

for i, button in enumerate(buttons):
    button.grid(row=i+1, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=400, y=170, width=1050, height=600)



# Grade Table
scrollbar_x = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollbar_y = Scrollbar(rightFrame, orient=VERTICAL)


gradeTable = ttk.Treeview(rightFrame, columns=("ID", "Student Name", "Course", "Grade", "Percentage", "Date"), 
                        xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

scrollbar_x.pack(side=BOTTOM, fill=X)
scrollbar_y.pack(side=RIGHT, fill=Y)

scrollbar_x.config(command=gradeTable.xview)
scrollbar_y.config(command=gradeTable.yview)

gradeTable.heading("ID", text="ID")
gradeTable.heading("Student Name", text="Student Name")
gradeTable.heading("Course", text="Course")
gradeTable.heading("Grade", text="Grade")
gradeTable.heading("Percentage", text="Percentage")
gradeTable.heading("Date", text="Date")
gradeTable['show'] = 'headings'
gradeTable.pack(fill=BOTH, expand=True)

gradeTable.column('ID', width=90, anchor=CENTER)
gradeTable.column('Student Name', width=200, anchor=CENTER)
gradeTable.column('Course', width=200, anchor=CENTER)
gradeTable.column('Grade', width=200, anchor=CENTER)
gradeTable.column('Percentage', width=200, anchor=CENTER)
gradeTable.column('Date', width=200, anchor=CENTER)


style = ttk.Style()
style.configure('Treeview', rowheight=35, font=('arial', 13), bg='white')
style.configure('Treeview.Heading', font=('classic', 14, 'bold'), foreground='red')

gradeTable.config(show='headings')

root.mainloop()