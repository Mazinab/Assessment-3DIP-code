import tkinter as tk

def submit_form():
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
phone_entry = tk.Entry(window)
phone_entry.pack()

# Email
email_label = tk.Label(window, text="Email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

# Password
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="**")
password_entry.pack()

# Business Name
business_label = tk.Label(window, text="Business Name:")
business_label.pack()
business_entry = tk.Entry(window)
business_entry.pack()

# Submit button
submit_button = tk.Button(window, text="Proceed", command=submit_form)
submit_button.pack()

window.mainloop()
