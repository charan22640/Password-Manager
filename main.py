from tkinter import *
import random
import pyperclip
import json
import os
from tkinter import messagebox


FONT = ("Arial", 14, "bold")
DATA_FILE = "datafile.json"  # Relative path for the data file

# --------------------------- GENERATE PASSWORD------------------------------------------------------------------------#
def password_generator():
    alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabets_lower = 'abcdefghijklmnopqrstuvwxyz'
    symbols = '!@#$%^&*()_+-={}[]|\\:;\'<>,.?/'
    numbers = '1234567890'
    
    password = ""
    while len(password) < 10:
        password += random.choice(alphabets)
        password += random.choice(alphabets_lower)
        password += random.choice(symbols)
        password += random.choice(numbers)
    
    password_list = list(password)
    random.shuffle(password_list)  
    return "".join(password_list)


def display_password():
    text3entry.delete(0, END)
    text3entry.insert(0, password_generator())

#--------------------------------------------SAVE PASSWORD-----------------------------------------------------------------#
def save():
    website = text1entry.get()
    email = text2entry.get()
    password = text3entry.get()
    new_data = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please fill out all fields!")
        return
    
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as datafile:
                data = json.load(datafile)
        else:
            data = {}
        data.update(new_data)
        with open(DATA_FILE, "w") as datafile:
            json.dump(data, datafile, indent=4)
        pyperclip.copy(password)
        text1entry.delete(0, END)
        text3entry.delete(0, END)
        messagebox.showinfo(title="Success", message="Details added successfully!")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")

#---------------------------------------------SEARCH  PASSWORD---------------------------------------------------------#
def search():
    website = text1entry.get()
    if not os.path.exists(DATA_FILE):
        messagebox.showinfo(title="Error", message="No data file found!")
        return
    try:
        with open(DATA_FILE, "r") as datafile:
            data = json.load(datafile)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Details Found", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Not Found", message="No details for the entered website.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")

#------------------------------------------------------UI SETUP-----------------------------------------------------#
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200)
canvas.grid(row=0, column=1)
img = PhotoImage(file="logo.png") 
canvas.create_image(100, 100, image=img)


Label(text="Website:", font=FONT).grid(row=1, column=0)
text1entry = Entry(width=21)
text1entry.grid(row=1, column=1)

Label(text="Email/Username:", font=FONT).grid(row=2, column=0)
text2entry = Entry(width=40)
text2entry.insert(0, "example@gmail.com")  
text2entry.grid(row=2, column=1, columnspan=2)

Label(text="Password:", font=FONT).grid(row=3, column=0)
text3entry = Entry(width=21)
text3entry.grid(row=3, column=1)


Button(text="Search", width=15, command=search).grid(row=1, column=2)
Button(text="Generate Password", command=display_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save).grid(row=4, column=1, columnspan=2)


window.mainloop()
