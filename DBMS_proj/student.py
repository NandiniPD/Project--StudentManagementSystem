from tkinter import *
import time
from tkinter import messagebox
import ttkthemes
import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import PhotoImage


# Clock Function to display time and date
def clock():
    global date,currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)  # Update every 1 second


#Slide functuion
count = 0 # 1 -> t, 2 -> u
text = ''

def slider():
    global text, count # to change the values
    if count == len(s): # to start again with letter 's' without stopping
        count = 0
        text = ''
    text = text + s[count] # Add the next letter to 'text'
    sliderLabel.config(text=text)
    count += 1 #to change charcter
    sliderLabel.after(300, slider)  # Call the function again after 300 ms
    
    


#the labels and entries are belongs to add,search,update functions ..instead of writing again and again so created function
def top_data(title,button_text,command):
    global idEntry,nameEntry,departmentEntry,emailEntry,phoneEntry,addressEntry,genderEntry,dobEntry,screen
    screen=Toplevel()
    screen.title(title) #title on the box
    screen.grab_set()
    screen.resizable(False,False)
    screen.geometry('480x700+15+120')
    
    
    idLabel=Label(screen,text='Id:',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=20,sticky=W) #padx=space btn id and the id entering box
    idEntry=Entry(screen,font=('roman',15,'bold'))
    idEntry.grid(row=0,column=1,pady=25,padx=10)

    nameLabel=Label(screen,text='Name:',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=20,sticky=W) #space btn id and the id entering box
    nameEntry=Entry(screen,font=('roman',15,'bold'))
    nameEntry.grid(row=1,column=1,pady=25,padx=10)
    
    # Department ID
    deptLabel = Label(screen, text='Department ID:', font=('times new roman', 20, 'bold'))
    deptLabel.grid(row=2, column=0, padx=20, sticky=W)
    departmentEntry = Entry(screen, font=('roman', 15, 'bold'))
    departmentEntry.grid(row=2, column=1, pady=25, padx=10)
    
    phoneLabel=Label(screen,text='Phone:',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=3,column=0,padx=20,sticky=W) #space btn id and the id entering box
    phoneEntry=Entry(screen,font=('roman',15,'bold'))
    phoneEntry.grid(row=3,column=1,pady=25,padx=10)
    
    emailLabel=Label(screen,text='Email-ID:',font=('times new roman',20,'bold'))
    emailLabel.grid(row=4,column=0,padx=20,sticky=W) #space btn id and the id entering box
    emailEntry=Entry(screen,font=('roman',15,'bold'))
    emailEntry.grid(row=4,column=1,pady=25,padx=10)
    
    addressLabel=Label(screen,text='Address:',font=('times new roman',20,'bold'))
    addressLabel.grid(row=5,column=0,padx=20,sticky=W) #space btn id and the id entering box
    addressEntry=Entry(screen,font=('roman',15,'bold'))
    addressEntry.grid(row=5,column=1,pady=25,padx=10)
    
    genderLabel=Label(screen,text='Gender',font=('times new roman',20,'bold'))
    genderLabel.grid(row=6,column=0,padx=20,sticky=W) #space btn id and the id entering box
    
    # Gender Combobox
    genderEntry = ttk.Combobox(screen, font=('times new roman', 14, 'bold'), state='readonly')
    genderEntry['values'] = ['Male', 'Female', 'Other']
    genderEntry.set('Select Gender')  # Placeholder text
    genderEntry.grid(row=6, column=1, pady=25, padx=20)
    # genderEntry=Entry(screen,font=('roman',15,'bold'))
    # genderEntry.grid(row=5,column=1,)
    
    dobLabel=Label(screen,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=7,column=0,padx=20,sticky=W) #space btn id and the id entering box
    dobEntry=Entry(screen,font=('roman',15,'bold'))
    dobEntry.grid(row=7,column=1,pady=25,padx=10)
    
    button=tk.Button(screen,text=button_text,width=10,font=('times new roman',13,'bold'),bg='dodger blue',activebackground='green2',command=command)
    button.grid(row=8,column=0,columnspan=1,ipady=5,padx=5)
    clear_button=tk.Button(screen,text='Clear',width=10,font=('times new roman',13,'bold'),bg='dodger blue',activebackground='green2',command=clear_fields)
    clear_button.grid(row=8,column=1,columnspan=1,ipady=5,padx=5)
    
    
    if title=='Update Student':
        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        listdata=content['values'] 
        if listdata:  # Only proceed if listdata is not empty
            idEntry.insert(0, listdata[0])
            nameEntry.insert(0, listdata[1])
            departmentEntry.insert(0, listdata[2])
            phoneEntry.insert(0, listdata[3])
            emailEntry.insert(0, listdata[4])
            addressEntry.insert(0, listdata[5])
            dobEntry.insert(0, listdata[7])
            genderEntry.set(listdata[6])
        else:
            messagebox.showerror("Error", "No data selected. Please select a valid student.", parent=screen)

    



def clear_fields():
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    departmentEntry.delete(0,END)
    phoneEntry.delete(0, END)
    emailEntry.delete(0, END)
    addressEntry.delete(0, END)
    genderEntry.set('Select Gender')  # Resetting the combo box to default
    dobEntry.delete(0, END)

    
#search student function
def search_data():
    
    query='Select * from student where id=%s or name=%s or dept_Id=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s '
    mycursor.execute(query,(idEntry.get(),
                            nameEntry.get(),
                            departmentEntry.get(),
                            emailEntry.get(),
                            phoneEntry.get(),
                            addressEntry.get(),
                            genderEntry.get(),
                            dobEntry.get()))
    studentTable.delete(*studentTable.get_children()) # not need prev data
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END, values=data)
    screen.destroy()# after click search it the search student window will close
        
    
    
#add_student function
# def add_data():
#     if idEntry.get()=='' or nameEntry.get()=='' or departmentEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='' :
#         messagebox.showerror('Error','All Fields Are Required',parent=screen)
#     else:
#         try:
#             query='INSERT INTO student (id,name, dept_Id, mobile, email, address, gender, dob, date, time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)'#id to dob and also date and time
#             mycursor.execute(query,(idEntry.get(),
#                                     nameEntry.get(),
#                                     departmentEntry.get(),
#                                     phoneEntry.get(),
#                                     emailEntry.get(),
#                                     addressEntry.get(),
#                                     genderEntry.get(),
#                                     dobEntry.get(),
#                                     date,
#                                     currenttime
#             ))
#             con.commit()
#             result=messagebox.askyesno('Confirm','Data Added Successfully. Do u want to clean the form?',parent=screen)
#             if result:
#                 clear_fields()
#                 # idEntry.delete(0,END)
#                 # nameEntry.delete(0,END)
#                 # departmentEntry.delete(0,END)
#                 # phoneEntry.delete(0,END)
#                 # emailEntry.delete(0,END)
#                 # addressEntry.delete(0,END)
#                 # genderEntry.delete(0,END)
#                 # dobEntry.delete(0,END)
            
#             else:
#                 pass
#         except Exception as e:
#                 messagebox.showerror('Error', f'An error occurred: {e}', parent=screen)
#                 return

#         # except:
#         #     messagebox.showerror('Error', 'Id Cannot be Repeated',parent=screen)
#         #     return
#         screen.destroy()
#         query='select * from student'
#         mycursor.execute(query)
#         fetched_data=mycursor.fetchall()
#         studentTable.delete(*studentTable.get_children())  # to delete previous values after added
        
#         for data in fetched_data: #it convert tuple to list
#             #datalist=list(data)
#             studentTable.insert(' ',END,values=data)
            

# Add student function with dept_id validation and error handling
def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or departmentEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required', parent=screen)
    else:
        try:
            # Check if the student ID already exists
            student_id = idEntry.get()
            query = 'SELECT id FROM student WHERE id = %s'
            mycursor.execute(query, (student_id,))
            result = mycursor.fetchone()

            if result:
                messagebox.showerror('Error', f'Duplicate entry: Student ID {student_id} already exists.', parent=screen)
                return

            # Check if dept_id exists in the department table
            dept_id = departmentEntry.get()
            query = 'SELECT dept_Id FROM department WHERE dept_Id = %s'
            mycursor.execute(query, (dept_id,))
            result = mycursor.fetchone()

            if result is None:
                messagebox.showerror('Error', 'Department ID does not exist', parent=screen)
                return

            # Add student to the student table
            query = '''INSERT INTO student (id, name, dept_Id, mobile, email, address, gender, dob, date, time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), dept_id, phoneEntry.get(), emailEntry.get(),
                                    addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            messagebox.showinfo('Success', 'Student added successfully', parent=screen)
            clear_fields()
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}', parent=screen)
            return

def update_data():
    try:
        new_id = idEntry.get()  # Get the new ID from the entry
        current_id = studentTable.item(studentTable.focus())['values'][0]  # Get the current ID of the selected student
        
        print(f"Current ID: {current_id}, New ID: {new_id}")  # Debugging print

        # If the ID has not changed, just proceed with updating other details
        if new_id == current_id:
            # Ensure all fields are filled before executing the query
            if not all([nameEntry.get(), departmentEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()]):
                messagebox.showerror('Error', 'All fields must be filled.', parent=screen)
                return
            
            # Update only name, department, etc.
            query = '''UPDATE student 
                    SET name = %s, dept_Id = %s, mobile = %s, email = %s, address = %s, gender = %s, dob = %s 
                    WHERE id = %s'''
            mycursor.execute(query, (nameEntry.get(), departmentEntry.get(), phoneEntry.get(),
                                    emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), current_id))
            con.commit()
            messagebox.showinfo('Success', 'Student updated successfully', parent=screen)
        
        else:
            # If the ID is changing, check if the new ID already exists in the database
            query = 'SELECT id FROM student WHERE id = %s'
            mycursor.execute(query, (new_id,))
            result = mycursor.fetchone()

            if result:
                messagebox.showerror('Error', f'Student ID {new_id} already exists. Choose a different ID.', parent=screen)
                return

            # Proceed to update the ID along with other details
            query = '''UPDATE student 
                    SET id = %s, name = %s, dept_Id = %s, mobile = %s, email = %s, address = %s, gender = %s, dob = %s 
                    WHERE id = %s'''
            mycursor.execute(query, (new_id, nameEntry.get(), departmentEntry.get(), phoneEntry.get(),
                                     emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), current_id))
            con.commit()
            messagebox.showinfo('Success', 'Student updated successfully', parent=screen)
        
        clear_fields()  # Clear the input fields after update
        screen.destroy()  # Close the update window
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}', parent=screen)
        print(f"Error: {e}")  # Print the error for debugging purposes
        return



# Delete student function with foreign key constraint handling
def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content['values'][0]

    try:
        query = 'DELETE FROM student WHERE id = %s'
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'The Row with ID {content_id} is deleted Successfully.')
        

    except pymysql.MySQLError as e:
        if e.args[0] == 1451:  # Foreign key constraint violation error code
            messagebox.showerror('Error', 'Cannot delete student due to existing foreign key constraints.', parent=root)
        else:
            messagebox.showerror('Error', f'An unexpected SQL error occurred: {e}', parent=root)

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}', parent=root)

    # Refresh the student data after deletion
    query = 'SELECT * FROM student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)
    

#Update function
# def update_data():
    
#     query='update student set name=%s,Dept_Id=%s,mobile=%s,email=%s,address=%s,address=%s,dob=%s,date=%s,time=%s where id=%s' # here we won't set id coz it is unique(it cann't be change)
#     mycursor.execute(query,(nameEntry.get(),departmentEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
#     con.commit()
#     messagebox.showinfo('Success',f'ID {idEntry.get()} is updated successfully',parent=screen)
#     screen.destroy()
#     show_student()


#showing all studnt data
def show_student():
    
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)
        
def exit():
    r = messagebox.askyesno('Exit', 'Do You Want To Exit?')
    if r:
        root.destroy()


#connect_database function
def connect():
    global mycursor, con
    try:
        con = pymysql.connect(host='localhost', user='root', password='qwerty1234')
        mycursor = con.cursor()
        mycursor.execute('CREATE DATABASE IF NOT EXISTS student_db')
        mycursor.execute('USE student_db')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to connect: {e}', parent=root)

    try:
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS student(
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
                time VARCHAR(50))
''')
        messagebox.showinfo('Success', 'Database Connection Successful')
        toggle_buttons(NORMAL)
    except:
        toggle_buttons(DISABLED)

def toggle_buttons(state):
    addstudentButton.config(state=state)
    searchstudentButton.config(state=state)
    updatestudentButton.config(state=state)
    showstudentButton.config(state=state)
    exitstudentButton.config(state=state)
    deletestudentButton.config(state=state)
    

#GUI part
root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

# Window settings
root.geometry('1530x800+0+0')
root.resizable(0, 0)
root.title('Student Management System')

#Left Frame for Buttons
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)


#Display Date and time
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=0, y=7)
clock()

# Slider for "Student Management System" Text
s = 'Student Management System.'
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=400, y=30)
slider()

# Creation of Connect Database Button
connectButton = ttk.Button(root, text='Connect database',command=connect)  # ttk adds theme
connectButton.place(x=1340, y=34)

#Left Frame for Buttons
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=700)

# Adding a Logo Image (replace with your own file path)
logo_image = PhotoImage(file='students.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0,pady=40)

# Adding Buttons for Student Management Actions
addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,command=lambda:top_data('Add Student','SUBMIT',add_data))
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,command=lambda:top_data('Search Student','SEARCH',search_data))
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,command=lambda:top_data('Update Student',' UPDATE',update_data))
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED,command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exitstudentButton = ttk.Button(leftFrame, text='Exit Student', width=25,command=exit)
exitstudentButton.grid(row=6, column=0, pady=20)



# Right Frame for Displaying the Student Table
rightFrame = Frame(root)
rightFrame.place(x=350, y=170, width=1170, height=610)

# Scrollbars for the Table
scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

# Student Table
studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name','Dept_Id', 'Mobile No', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)


scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)  # Fill the space and make the table expandable


# Table Headings
studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Dept_Id',text='Dept_Id')
studentTable.heading('Mobile No', text='Mobile No')
studentTable.heading('Email', text='Email')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')


#align rows infrom centre with height  & width
studentTable.column('Id',width=60,anchor=CENTER)
studentTable.column('Name',width=160,anchor=CENTER)
studentTable.column('Dept_Id',width=160,anchor=CENTER)
studentTable.column('Mobile No',width=200,anchor=CENTER)
studentTable.column('Email',width=220,anchor=CENTER)
studentTable.column('Address',width=190,anchor=CENTER)
studentTable.column('Gender',width=180,anchor=CENTER)
studentTable.column('D.O.B',width=180,anchor=CENTER)
studentTable.column('Added Date',width=180,anchor=CENTER)
studentTable.column('Added Time',width=180,anchor=CENTER)




style=ttk.Style()

#style.configure('Treeview',rowheight=25,font= ('arial',15,'bold'),foreground='red4',background='yellow',fieldbackground='red')
style.configure('Treeview',rowheight=35,font= ('arial',13),bg='white')

#style changing of upper subheads
style.configure('Treeview.Heading',font=('classic',14,'bold'),foreground='red')


studentTable.config(show='headings')

root.mainloop()















