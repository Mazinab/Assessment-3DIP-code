import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3



# Create a database connection
conn = sqlite3.connect('business_planner.db')
cursor = conn.cursor()

# Create a user_info table
cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  full_name TEXT,
                  phone_number TEXT,
                  email TEXT,
                  password TEXT,
                  business_name TEXT)''')

# Create a tasks table
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name TEXT,
                  due_date TEXT)''')

# Function to save user information and proceed to the task entry window
def save_user_info_and_proceed():
    full_name = full_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    business_name = business_name_entry.get()
    
    # Check if all fields are filled
    if full_name and phone_number and email and password and business_name:
        cursor.execute('''INSERT INTO user_info (full_name, phone_number, email, password, business_name)
                          VALUES (?, ?, ?, ?, ?)''', (full_name, phone_number, email, password, business_name))
        conn.commit()
        
        # Clear the input fields
        full_name_entry.delete(0, tk.END)
        phone_number_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        business_name_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "User information saved!")
        
        # Hide the registration window
        registration_window.withdraw()
        
        # Show the task entry window
        task_entry_window.deiconify()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to add a task
def add_task():
    task_name = task_entry.get()
    due_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
    
    # Check if both task and due date are provided
    if task_name and due_date:
        cursor.execute('''INSERT INTO tasks (task_name, due_date)
                          VALUES (?, ?)''', (task_name, due_date))
        conn.commit()
        messagebox.showinfo("Success", "Task added!")
        
        # Clear the input fields
        task_entry.delete(0, tk.END)
        day_var.set(day_options[0])
        month_var.set(month_options[0])
        year_var.set(year_options[0])
        
        # Update the task calendar
        update_task_calendar()
    else:
        messagebox.showerror("Error", "Please provide both task and due date.")

# Function to delete a task
def delete_task():
    selected_item = task_delete.focus()
    if selected_item:
        task_id = task_delete.item(selected_item, "text")
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        update_task_calendar()
        messagebox.showinfo("Success", "Task deleted!")
    else:
        messagebox.showerror("Error", "Please select a task to delete.")

# Function to update the task calendar
def update_task_calendar():
    # Clear the treeview
    task_delete.delete(*task_delete.get_children())
        
    # Fetch tasks from the database
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    
    # Insert tasks into the treeview
    for task in tasks:
        task_delete.insert("", tk.END, text=task[0], values=(task[0], task[1], task[2]))

# Create the registration form window
registration_window = tk.Tk()
registration_window.title("Registration Form")

full_name_label = ttk.Label(registration_window, text="Full Name:")
full_name_label.pack()
full_name_entry = ttk.Entry(registration_window)
full_name_entry.pack()

phone_number_label = ttk.Label(registration_window, text="Phone Number:")
phone_number_label.pack()
phone_number_entry = ttk.Entry(registration_window)
phone_number_entry.pack()

email_label = ttk.Label(registration_window, text="Email:")
email_label.pack()
email_entry = ttk.Entry(registration_window)
email_entry.pack()

password_label = ttk.Label(registration_window, text="Password:")
password_label.pack()
password_entry = ttk.Entry(registration_window, show="*")
password_entry.pack()

business_name_label = ttk.Label(registration_window, text="Business Name:")
business_name_label.pack()
business_name_entry = ttk.Entry(registration_window)
business_name_entry.pack()

proceed_button = ttk.Button(registration_window, text="Proceed", command=save_user_info_and_proceed)
proceed_button.pack()

# Create the task entry window
task_entry_window = tk.Toplevel()
task_entry_window.title("Task Entry")

# Create the task entry tab
task_entry_tab = ttk.Frame(task_entry_window)
task_entry_tab.pack(padx=20, pady=20)

task_label = ttk.Label(task_entry_tab, text="Task:")
task_label.grid(row=0, column=0, sticky=tk.W)
task_entry = ttk.Entry(task_entry_tab)
task_entry.grid(row=0, column=1)

due_date_label = ttk.Label(task_entry_tab, text="Due Date:")
due_date_label.grid(row=1, column=0, sticky=tk.W)

# Create the day dropdown list
day_options = list(range(1, 31))
day_var = tk.StringVar(value=day_options[0])
day_dropdown = ttk.Combobox(task_entry_tab, textvariable=day_var, values=day_options)
day_dropdown.grid(row=1, column=1, padx=5)

# Create the month dropdown list
month_options = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_var = tk.StringVar(value=month_options[0])
month_dropdown = ttk.Combobox(task_entry_tab, textvariable=month_var, values=month_options)
month_dropdown.grid(row=1, column=2, padx=5)

# Create the year dropdown list
year_options = list(range(2023, 2031))
year_var = tk.StringVar(value=year_options[0])
year_dropdown = ttk.Combobox(task_entry_tab, textvariable=year_var, values=year_options)
year_dropdown.grid(row=1, column=3, padx=5)

add_task_button = ttk.Button(task_entry_tab, text="Add Task", command=add_task)
add_task_button.grid(row=2, column=0, columnspan=4, pady=10)

delete_task_button = ttk.Button(task_entry_tab, text="Delete Task", command=delete_task)
delete_task_button.grid(row=3, column=0, columnspan=4, pady=10)

# Create the task calendar tab
task_calendar_tab = ttk.Frame(task_entry_window)
task_calendar_tab.pack(padx=20, pady=20)

task_delete = ttk.Treeview(task_calendar_tab, columns=("Task Number", "Task Name", "Date"), show="headings")
task_delete.heading("Task Number", text="Task Number")
task_delete.heading("Task Name", text="Task Name")
task_delete.heading("Date", text="Date")
task_delete.pack()

# Update the task calendar
update_task_calendar()

# Hide the task entry window initially
task_entry_window.withdraw()

# Run the main loop
registration_window.mainloop()

# Close the database connection
conn.close() 
