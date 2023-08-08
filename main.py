from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        },
    }

    if len(password) == 0 or len(website) == 0 or len(email) == 0:
        messagebox.showerror(title='Empty Field', message='Please do not leave any field empty!')

    else:
        check_input = messagebox.askyesno(title='Check Details',
                                          message=f'Details Entered:\nEmail:{email}\nPassword: {password}\nContinue?')
        if check_input:
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
                    # Appends new_data into previous data
                    data.update(new_data)
            except FileNotFoundError:
                # Creates new data from new_data
                data = new_data

            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)

            website_input.delete(0, END)
            email_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_input.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No data file found!')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showerror(title="Error", message=f'No details for the {website} exists!')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)
window.title('Password Manager')

canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text='Website:')
website_label.config(padx=5, pady=1)
website_label.grid(row=1, column=0)
email_label = Label(text='Email/Username:')
email_label.config(padx=7, pady=1)
email_label.grid(row=2, column=0)
password_label = Label(text='Password:')
password_label.config(padx=5, pady=2)
password_label.grid(row=3, column=0)

# Inputs
website_input = Entry(width=34)
website_input.grid(row=1, column=1)
website_input.focus()
email_input = Entry(width=52)
email_input.grid(row=2, column=1, columnspan=2)
password_input = Entry(width=34)
password_input.grid(row=3, column=1)


# Buttons
generate_password_button = Button(text='Generate Password', width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text='Add', width=44, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text='Search', width=14, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
