import tkinter as tk
import re
from tkinter import tkk

def validate_fullname():
    fullname = fullname_entry.get()
    if not fullname.isalpha():
        return "Invalid full name. Please enter only alphabetical characters."

def validate_phone_number():
    phone_number = phone_entry.get()
    if not phone_number.isdigit() or len(phone_number) != 10:
        return "Invalid phone number. Please make ensure you  enter 10 numerical digits ."

def validate_email():
    email = email_entry.get()
    if "@" not in email:
        return "Invalid email. Please make sure to include '@'."

def validate_password():
    password = password_entry.get()
    if not password.isalnum():
        return "Invalid password. Password should contain only alphabetical and numerical characters."

def validate_business_name():
    business_name = business_entry.get()
    if not business_name.isalpha():
        return "Invalid business name. Please enter only alphabetical characters."

def submit_form():
    validation_functions = [
        validate_fullname,
        validate_phone_number,
        validate_email,
        validate_password,
        validate_business_name
    ]

    errors = []
    for validation_function in validation_functions:
        error = validation_function()
        if error:
            errors.append(error)

    if errors:
        error_label.config(text="\n".join(errors))
        return

    fullname = fullname_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    business_name = business_entry.get()

    print("Fullname:", fullname)
    print("Phone:", phone)
    print("Email:", email)
    print("Password:", password)
    print("Business Name:", business_name)

    # You can perform further processing or validation here

    # Close the window
    window.destroy()

window = tk.Tk()
window.title(" SIGN UP !")
window.geometry("500x500")

# Fullname
fullname_label = tk.Label(window, text="Fullname:")
fullname_label.pack()
fullname_entry = tk.Entry(window)
fullname_entry.pack()

# Phone
phone_label = tk.Label(window, text="Phone:")
phone_label.pack()
validate_phone_number_cmd = window.register(validate_phone_number)
phone_entry = tk.Entry(window, validate="key", validatecommand=(validate_phone_number_cmd, "%P"))
phone_entry.pack()

# Email
email_label = tk.Label(window, text="Email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

# Password
password_label = tk.Label(window, text="Password:")
password_label.pack()
validate_password_cmd = window.register(validate_password)
password_entry = tk.Entry(window, show="*", validate="key", validatecommand=(validate_password_cmd, "%P"))
password_entry.pack()

# Business Name
business_label = tk.Label(window, text="Business Name:")
business_label.pack()
business_entry = tk.Entry(window)
business_entry.pack()

# Error Label
error_label = tk.Label(window, fg="red")
error_label.pack()

# Submit button
submit_button = tk.Button(window, text="Proceed", command=submit_form)
submit_button.pack()

window.mainloop()

