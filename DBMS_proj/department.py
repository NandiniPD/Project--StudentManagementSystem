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

# Create input form in a new window for Add, Update, or Search Department
def top_data(title, button_text, command):
    global idEntry, nameEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.geometry('500x300+15+120')
    screen.grab_set()
    screen.resizable(False, False)

    idLabel = Label(screen, text='Department ID:', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=25, padx=10)
    
    # Department Name
    nameLabel = Label(screen, text='Department Name:', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, pady=25, padx=10)
    
    # Submit button
    button = Button(screen, text=button_text, width=10, font=('times new roman', 13, 'bold'), bg='dodger blue', command=command)
    button.grid(row=2, column=0, pady=20)
    clear_button = Button(screen, text='Clear', width=10, font=('times new roman', 13, 'bold'), bg='dodger blue', command=clear_fields)
    clear_button.grid(row=2, column=1, pady=20)
    
    
    if title == 'Update Department':
        indexing = deptTable.focus()
        if not indexing:
            messagebox.showerror('Error', 'No department selected', parent=screen)
            return
        content = deptTable.item(indexing)
        listdata = content['values']
        
        if len(listdata) < 2:
            messagebox.showerror('Error', 'Invalid data selected', parent=screen)
            return
        
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        
def clear_fields():
    nameEntry.delete(0, END)

# Connect to MySQL database
def connect():
    global mycursor, con
    global mycursor, con
    try:
        con = pymysql.connect(host='localhost', user='root', password='qwerty1234', database='student_db')
        mycursor = con.cursor()
        messagebox.showinfo('Success', 'Database Connection Successful')
        toggle_buttons(NORMAL)
    except Exception as e:
        messagebox.showerror('Error', f'Failed to connect: {e}', parent=root)
        
def toggle_buttons(state):
    addDeptButton.config(state=state)
    searchDeptButton.config(state=state)
    updateDeptButton.config(state=state)
    showDeptButton.config(state=state)
    deleteDeptButton.config(state=state)
    exitButton.config(state=state)

# Add Department
def add_data():
    if nameEntry.get() == '':
        messagebox.showerror('Error', 'Department name is required', parent=screen)
    else:
        try:
            dept_id = idEntry.get()
            # Check if the ID already exists
            query = 'SELECT * FROM department WHERE dept_Id=%s'
            mycursor.execute(query, (dept_id,))
            existing_data = mycursor.fetchall()
            if existing_data:
                messagebox.showerror('Error', 'Department ID already exists', parent=screen)
            else:
                # Insert the new department
                query = 'INSERT INTO department (dept_Id, dept_name) VALUES (%s, %s)'
                mycursor.execute(query, (dept_id, nameEntry.get()))
                con.commit()
                messagebox.showinfo('Success', 'Department added successfully', parent=screen)
                clear_fields()
                show_departments()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add department: {e}', parent=screen)

# Search Department
def search_data():
    query = 'SELECT * FROM department WHERE dept_Id=%s  or  dept_name=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get()))
    deptTable.delete(*deptTable.get_children())
    fetched_data = mycursor.fetchall()
    if not fetched_data:  # Check if no data is found
        messagebox.showerror('Error', 'No department found with the given ID or Name', parent=screen)
    else:
        for data in fetched_data:
            deptTable.insert('', END, values=data)
    screen.destroy()
 # Update Department
def update_data():
    dept_id = idEntry.get()
    new_dept_name = nameEntry.get()

    # Check if the department is referenced in other tables
    query_student = 'SELECT * FROM student WHERE dept_id = %s'
    query_course = 'SELECT * FROM course WHERE dept_id = %s'
    mycursor.execute(query_student, (dept_id,))
    referenced_in_student = mycursor.fetchall()
    mycursor.execute(query_course, (dept_id,))
    referenced_in_course = mycursor.fetchall()

    if referenced_in_student or referenced_in_course:
        messagebox.showerror('Error', 'Cannot update department: it is referenced in other tables', parent=screen)
    else:
        # Update department name
        query = 'UPDATE department SET dept_name = %s WHERE dept_Id = %s'
        mycursor.execute(query, (new_dept_name, dept_id))
        con.commit()
        messagebox.showinfo('Success', f'Department {dept_id} updated successfully', parent=screen)
        screen.destroy()
        show_departments()


# Delete Department
def delete_data():
    indexing = deptTable.focus()
    content = deptTable.item(indexing)
    dept_id = content['values'][0]

    # Check if the department is referenced in the student or course tables
    query_student = 'SELECT * FROM student WHERE dept_id = %s'
    query_course = 'SELECT * FROM course WHERE dept_id = %s'
    mycursor.execute(query_student, (dept_id,))
    referenced_in_student = mycursor.fetchall()
    mycursor.execute(query_course, (dept_id,))
    referenced_in_course = mycursor.fetchall()

    if referenced_in_student or referenced_in_course:
        messagebox.showerror('Error', 'Cannot delete department: it is referenced by students or courses', parent=root)
    else:
        # Proceed with deletion
        query = 'DELETE FROM department WHERE dept_id = %s'
        mycursor.execute(query, (dept_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Department with ID {dept_id} was deleted successfully.', parent=root)
        screen.destroy()
        show_departments()

        

# Display all departments
def show_departments():
    query = 'SELECT dept_Id, dept_name FROM department'  # Only select ID and Name
    mycursor.execute(query)
    deptTable.delete(*deptTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        deptTable.insert('', END, values=data)
        

def exit():
    r = messagebox.askyesno('Exit', 'Do You Want To Exit?')
    if r:
        root.destroy()

# GUI Initialization
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1530x800+0+0')
root.resizable(0, 0)
root.title('Department Management System')

# Clock and Slider
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=0, y=7)
clock()
s = 'Department Management System.'
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


addDeptButton = ttk.Button(leftFrame, text='Add Department', width=25, state=DISABLED, command=lambda: top_data('Add Department', 'SUBMIT', add_data))
addDeptButton.grid(row=1, column=0, pady=20)
searchDeptButton = ttk.Button(leftFrame, text='Search Department', width=25, state=DISABLED, command=lambda: top_data('Search Department', 'SEARCH', search_data))
searchDeptButton.grid(row=2, column=0, pady=20)
updateDeptButton = ttk.Button(leftFrame, text='Update Department', width=25, state=DISABLED, command=lambda: top_data('Update Department', 'UPDATE', update_data))
updateDeptButton.grid(row=3, column=0, pady=20)
deleteDeptButton = ttk.Button(leftFrame, text='Delete Department', width=25, state=DISABLED, command=delete_data)
deleteDeptButton.grid(row=4, column=0, pady=20)
showDeptButton = ttk.Button(leftFrame, text='Show Departments', width=25, state=DISABLED, command=show_departments)
showDeptButton.grid(row=5, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Exit Student', width=25,command=exit)
exitButton.grid(row=6, column=0, pady=20)

# Right Frame for Department Table
rightFrame = Frame(root)
rightFrame.place(x=400, y=170, width=1000, height=600)
scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
deptTable = ttk.Treeview(rightFrame, columns=('ID', 'Name'),
                        xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
scrollBarX.config(command=deptTable.xview)
scrollBarY.config(command=deptTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
deptTable.pack(fill=BOTH, expand=1)

deptTable.heading('ID', text='ID')
deptTable.heading('Name', text='Name')

deptTable.column('ID', width=100,anchor=CENTER)
deptTable.column('Name', width=200,anchor=CENTER)


style=ttk.Style()

#style.configure('Treeview',rowheight=25,font= ('arial',15,'bold'),foreground='red4',background='yellow',fieldbackground='red')
style.configure('Treeview',rowheight=35,font= ('arial',13),bg='white')

#style changing of upper subheads
style.configure('Treeview.Heading',font=('classic',14,'bold'),foreground='red')


deptTable.config(show='headings')

root.mainloop()
