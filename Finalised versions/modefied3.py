import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

#Here I create a databse connectiojn using sqlite3 that i have imported
class Database:
# This is the construction of the Data base class
    def __init__(self, window_file):
        self.conn = sqlite3.connect(window_file)
        self.cursor = self.conn.cursor()
        self.create_tables()
#The following is the methods used for the Database class

# Create a user_info table
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              full_name TEXT,
                              phone_number TEXT,
                              email TEXT,
                              password TEXT,
                              business_name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              task_name TEXT,
                              due_date TEXT)''')
        self.conn.commit()

    def insert_user_info(self, full_name, phone_number, email, password, business_name):
        self.cursor.execute('''INSERT INTO user_info (full_name, phone_number, email, password, business_name)
                              VALUES (?, ?, ?, ?, ?)''', (full_name, phone_number, email, password, business_name))
        self.conn.commit()

    def insert_task(self, task_name, due_date):
        self.cursor.execute('''INSERT INTO tasks (task_name, due_date)
                              VALUES (?, ?)''', (task_name, due_date))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# This the start for the foirst window the start of making th labels and entry boxes for the user to enter their information
class RegistrationWindow(tk.Tk):
    
    #This is the Construction of the Riegistration window class
    def __init__(self, window):
        super().__init__()
        self.title("Registration Form")
        self.window = window
        self.create_widgets()

#The following is the methods for the regeistrationn window class

#Entrys and labels
    def create_widgets(self):
        full_name_label = ttk.Label(self, text="Full Name:")
        full_name_label.pack()
        self.full_name_entry = ttk.Entry(self)
        self.full_name_entry.pack()

        phone_number_label = ttk.Label(self, text="Phone Number:")
        phone_number_label.pack()
        self.phone_number_entry = ttk.Entry(self)
        self.phone_number_entry.pack()

        email_label = ttk.Label(self, text="Email:")
        email_label.pack()
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()

        password_label = ttk.Label(self, text="Password:")
        password_label.pack()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        business_name_label = ttk.Label(self, text="Business Name:")
        business_name_label.pack()
        self.business_name_entry = ttk.Entry(self)
        self.business_name_entry.pack()

        proceed_button = ttk.Button(self, text="Proceed", command=self.save_user_info_and_proceed)
        proceed_button.pack()


# This is the validation for the registartion code these validation functions make sure that all the users entrys are reliable
    def validate_fullname(self):
        fullname = self.full_name_entry.get()
        if not fullname.isalpha():
            return "Invalid full name. Please enter only alphabetical characters."

    def validate_phone_number(self):
        phone_number = self.phone_number_entry.get()
        if not phone_number.isdigit() or len(phone_number) != 10:
            return "Invalid phone number. Please enter 10 numerical digits."

    def validate_email(self):
        email = self.email_entry.get()
        if "@" not in email:
            return "Invalid email. Please make sure to include '@'."

    def validate_password(self):
        password = self.password_entry.get()
        if not password.isalnum():
            return "Invalid password. Password should contain only alphabetical and numerical characters."

    def validate_business_name(self):
        business_name = self.business_name_entry.get()
        if not business_name.isalpha():
            return "Invalid business name. Please enter only alphabetical characters."

    def save_user_info_and_proceed(self):
        validation_functions = [
            self.validate_fullname,
            self.validate_phone_number,
            self.validate_email,
            self.validate_password,
            self.validate_business_name
        ]

        errors = []
        for validation_function in validation_functions:
            error = validation_function()
            if error:
                errors.append(error)

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        full_name = self.full_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        business_name = self.business_name_entry.get()

        self.window.insert_user_info(full_name, phone_number, email, password, business_name)

        self.full_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.business_name_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "User information saved!")

        self.withdraw()
        TaskEntryWindow(self.window)

# This is the Task managment code begining
class TaskEntryWindow(tk.Toplevel):
    #This is the construction of the Taskentry window class
    def __init__(self, window):
        super().__init__()
        self.title("Task Entry")
        self.window = window
        self.create_widgets()
        self.update_task_calendar()

#The following is the Methods for the task entrywindow class

#all the labels for the second window 
    def create_widgets(self):
        task_entry_tab = ttk.Frame(self)
        task_entry_tab.pack(padx=20, pady=20)

        task_label = ttk.Label(task_entry_tab, text="Task:")
        task_label.grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(task_entry_tab)
        self.task_entry.grid(row=0, column=1)

        due_date_label = ttk.Label(task_entry_tab, text="Due Date:")
        due_date_label.grid(row=1, column=0, sticky=tk.W)

        #  the day dropdown list
        day_options = list(range(1, 31))
        self.day_var = tk.StringVar(value=day_options[0])
        day_dropdown = ttk.Combobox(task_entry_tab, textvariable=self.day_var, values=day_options)
        day_dropdown.grid(row=1, column=1, padx=5)

        #  the month dropdown list
        month_options = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.month_var = tk.StringVar(value=month_options[0])
        month_dropdown = ttk.Combobox(task_entry_tab, textvariable=self.month_var, values=month_options)
        month_dropdown.grid(row=1, column=2, padx=5)

        #  the year dropdown list
        year_options = list(range(2023, 2031))
        self.year_var = tk.StringVar(value=year_options[0])
        year_dropdown = ttk.Combobox(task_entry_tab, textvariable=self.year_var, values=year_options)
        year_dropdown.grid(row=1, column=3, padx=5)

        add_task_button = ttk.Button(task_entry_tab, text="Add Task", command=self.add_task)
        add_task_button.grid(row=2, column=0, columnspan=4, pady=10)

        delete_task_button = ttk.Button(task_entry_tab, text="Delete Task", command=self.delete_task)
        delete_task_button.grid(row=3, column=0, columnspan=4, pady=10)

        task_calendar_tab = ttk.Frame(self)
        task_calendar_tab.pack(padx=20, pady=20)

        self.task_delete = ttk.Treeview(task_calendar_tab, columns=("Task Number", "Task Name", "Date"), show="headings")
        self.task_delete.heading("Task Number", text="Task Number")
        self.task_delete.heading("Task Name", text="Task Name")
        self.task_delete.heading("Date", text="Date")
        self.task_delete.pack()


#This is the function to add the tasks on the task coloumn after the user adds it
    def add_task(self):
        task_name = self.task_entry.get()
        due_date = f"{self.year_var.get()}-{self.month_var.get()}-{self.day_var.get()}"

        if task_name and due_date:
            self.window.insert_task(task_name, due_date)
            messagebox.showinfo("Success", "Task added!")
            self.task_entry.delete(0, tk.END)
            self.day_var.set(self.day_var.get()[0])
            self.month_var.set(self.month_var.get()[0])
            self.year_var.set(self.year_var.get()[0])
            self.update_task_calendar()
        else:
            messagebox.showerror("Error", "Please provide both task and due date.")


# this function is for the user to use in order to
    def delete_task(self):
        selected_item = self.task_delete.focus()
        if selected_item:
            task_id = self.task_delete.item(selected_item, "text")
            self.window.delete_task(task_id)
            self.update_task_calendar()
            messagebox.showinfo("Success", "Task deleted!")
        else:
            messagebox.showerror("Error", "Please select a task to delete.")

    def update_task_calendar(self):
        self.task_delete.delete(*self.task_delete.get_children())
        tasks = self.window.get_tasks()
        for task in tasks:
            self.task_delete.insert("", tk.END, text=task[0], values=(task[0], task[1], task[2]))

#main routine
if __name__ == "__main__":
    window = Database('business_planner.window')
    registration_window = RegistrationWindow(window)
    registration_window.mainloop()
    window.close()














