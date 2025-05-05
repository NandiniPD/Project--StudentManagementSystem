from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

# Function to crop the center circle from the image and save it as 'logo.png'
def create_circular_logo(input_path, output_path):
    image = Image.open(input_path)
    
    # Get dimensions
    width, height = image.size
    center_x, center_y = width // 2, height // 2
    radius = min(center_x, center_y)
    
    # Create a mask for circular cropping
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    
    # Apply the circular mask to the image
    circle_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    circle_image.paste(image, (0, 0), mask=mask)
    
    # Crop to the circular area
    circle_image = circle_image.crop((center_x - radius, center_y - radius, center_x + radius, center_y + radius))
    
    # Save the circular cropped image
    circle_image.save(output_path)

# Crop the center circle from 'image.png' and save it as 'logo.png'
input_image_path = 'logo.png'  # Path to the uploaded image
output_logo_path = 'logo.png'
create_circular_logo(input_image_path, output_logo_path)

# Function for login button
def login():
    if usernameEntry.get() == '' or PwdEntry.get() == '':
        messagebox.showerror('Error', 'Fields Cannot be Empty')
    elif usernameEntry.get() == 'Admin@gmail.com' and PwdEntry.get() == '12345':
        messagebox.showinfo('Success', 'You Successfully Logged in..')
        window.destroy()
        import dashboard  # Assuming dashboard is another script in your project
    else:
        messagebox.showerror('Error', 'Please Enter Correct Credentials')


# Create the tkinter window
window = Tk()
window.geometry('1530x900+0+0')
window.title("Login System Of Student Management")
window.resizable(False, False)

# Load the background image
background_image = Image.open('bg.jpg')
resized_image = background_image.resize((1680, 900), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(resized_image)
bg_label = Label(window, image=bg_image)
bg_label.place(x=(1380 - 1680) // 2, y=(900 - 900) // 2)

# Login frame
loginFrame = Frame(window, bg='#313139', padx=30, pady=30)
loginFrame.place(x=500, y=150)

# Load and display the circular logo
logoImage = ImageTk.PhotoImage(file=output_logo_path)
logoLabel = Label(loginFrame, image=logoImage, bg='#313139')
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

# Username field
usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT, font=('times new roman', 20, 'bold'), fg='white', bg='#313139')
usernameLabel.grid(row=1, column=0, pady=10)

usernameEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, relief='solid', highlightthickness=1, highlightcolor='cornflowerblue', justify='center')
usernameEntry.grid(row=1, column=1, padx=10, pady=10)

# Password field
PwdImage = PhotoImage(file='pwd.png')
PwdLabel = Label(loginFrame, image=PwdImage, text='Password', compound=LEFT, font=('times new roman', 20, 'bold'), fg='white', bg='#313139')
PwdLabel.grid(row=2, column=0, pady=10)

PwdEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, relief='solid', highlightthickness=1, highlightcolor='cornflowerblue', show="*")
PwdEntry.grid(row=2, column=1, padx=10, pady=10)

# Login button with hover effect
def on_enter(event):
    loginButton['background'] = 'dodgerblue'

def on_leave(event):
    loginButton['background'] = 'cornflowerblue'

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15, fg='white', bg='cornflowerblue', activebackground='red', cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)
loginButton.bind("<Enter>", on_enter)
loginButton.bind("<Leave>", on_leave)

# Start the tkinter main loop
window.mainloop()
