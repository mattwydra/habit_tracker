import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import calendar

# Initialize Tkinter root first
root = tk.Tk()
root.title("Habit Tracker")

# Add this function to get the month name
def get_month_name(year, month):
    return f"{calendar.month_name[month]} {year}"

def update_calendar():
    for widget in calendar_frame.winfo_children():
        widget.destroy()
    
    # Update the label to show the current month and year
    month_label.config(text=get_month_name(current_year, current_month))

    # Get correct number of days in the current month
    num_days = calendar.monthrange(current_year, current_month)[1]

    for day in range(1, num_days + 1):
        date = f"{current_year}-{current_month:02d}-{day:02d}"
        button_color = update_day_status(date)
        day_button = tk.Button(
            calendar_frame, text=str(day),
            width=4, height=2,
            bg=button_color,
            command=lambda d=date: open_day_tasks(d)
        )
        day_button.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=2, pady=2)

# Modify `change_month` to update the label as well
def change_month(offset):
    global current_month, current_year
    current_month += offset
    if current_month == 13:
        current_month = 1
        current_year += 1
    elif current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()

# Create and place the label above the calendar
month_label = tk.Label(root, text=get_month_name(current_year, current_month), font=("Arial", 14, "bold"))
month_label.pack()

# Load habit data
DATA_FILE = "habit_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_today():
    return datetime.today().strftime("%Y-%m-%d")

def update_day_status(date):
    """Update the shade of green based on completed tasks"""
    tasks = data.get(date, {})
    
    # Ensure tasks is a dictionary, not a list
    if isinstance(tasks, list):
        tasks = {task: False for task in predefined_tasks}  # Default to all tasks incomplete
        data[date] = tasks
        save_data(data)
    
    total_tasks = len(tasks)
    completed_tasks = sum(tasks.values())
    
    if total_tasks == 0:
        return "white"
    
    intensity = int((completed_tasks / total_tasks) * 255)
    return f"#00{intensity:02x}00"


def toggle_task(date, task_name, task_button):
    data.setdefault(date, {})
    data[date][task_name] = not data[date].get(task_name, False)
    save_data(data)
    task_button.config(bg="green" if data[date][task_name] else "white")
    update_calendar()

from functools import partial

def open_day_tasks(date):
    task_window = tk.Toplevel(root)
    task_window.title(f"Tasks for {date}")
    
    for task_name in predefined_tasks:
        task_button = tk.Button(
            task_window, text=task_name,
            width=20, height=2,
            bg="green" if data.get(date, {}).get(task_name, False) else "white"
        )
        task_button.config(command=partial(toggle_task, date, task_name, task_button))
        task_button.pack(pady=5)


import calendar

def update_calendar():
    for widget in calendar_frame.winfo_children():
        widget.destroy()
    
    # Get the correct number of days in the month
    num_days = calendar.monthrange(current_year, current_month)[1]
    
    for day in range(1, num_days + 1):
        date = f"{current_year}-{current_month:02d}-{day:02d}"
        button_color = update_day_status(date)
        day_button = tk.Button(
            calendar_frame, text=str(day),
            width=4, height=2,
            bg=button_color,
            command=lambda d=date: open_day_tasks(d)
        )
        day_button.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=2, pady=2)


def change_month(offset):
    global current_month, current_year
    current_month += offset
    if current_month == 13:
        current_month = 1
        current_year += 1
    elif current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()

# Predefined tasks for each day
predefined_tasks = ["Exercise", "Read", "Meditate", "Drink Water"]

data = load_data()
current_year, current_month = datetime.today().year, datetime.today().month

root = tk.Tk()
root.title("Habit Tracker")
calendar_frame = tk.Frame(root)
calendar_frame.pack()

nav_frame = tk.Frame(root)
nav_frame.pack()
tk.Button(nav_frame, text="<", command=lambda: change_month(-1)).pack(side=tk.LEFT)
tk.Button(nav_frame, text=">", command=lambda: change_month(1)).pack(side=tk.RIGHT)

update_calendar()
root.mainloop()
