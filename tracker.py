import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# File for saving progress
DATA_FILE = "habit_data.json"

# Load or initialize data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(habit_data, f, indent=4)

habit_data = load_data()

def get_current_date():
    return datetime.today().strftime("%Y-%m-%d")

def get_month_days(year, month):
    from calendar import monthrange
    return monthrange(year, month)[1]

# GUI Class
class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        
        self.current_year = datetime.today().year
        self.current_month = datetime.today().month
        self.selected_day = None

        self.create_widgets()
        self.load_month()

    def create_widgets(self):
        self.header = tk.Label(self.root, text=f"{self.current_month}/{self.current_year}", font=("Arial", 16))
        self.header.pack()

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()
        
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack()

        tk.Button(self.nav_frame, text="<", command=self.prev_month).pack(side=tk.LEFT)
        tk.Button(self.nav_frame, text=">", command=self.next_month).pack(side=tk.RIGHT)

    def load_month(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        days_in_month = get_month_days(self.current_year, self.current_month)
        
        for day in range(1, days_in_month + 1):
            day_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            color = "red" if day_str not in habit_data else "green"
            btn = tk.Button(self.grid_frame, text=str(day), bg=color, command=lambda d=day: self.open_day(d))
            btn.grid(row=(day-1)//7, column=(day-1) % 7)

    def open_day(self, day):
        day_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        self.selected_day = day_str
        
        top = tk.Toplevel(self.root)
        top.title(f"Tasks for {day_str}")
        
        tasks = habit_data.get(day_str, [])

        self.task_vars = {}
        for task in tasks:
            var = tk.BooleanVar(value=task["done"])
            chk = tk.Checkbutton(top, text=task["name"], variable=var)
            chk.pack(anchor="w")
            self.task_vars[task["name"]] = var

        tk.Button(top, text="Save", command=lambda: self.save_day(top)).pack()
        
    def save_day(self, window):
        if not self.selected_day:
            return
        
        tasks = [{"name": name, "done": var.get()} for name, var in self.task_vars.items()]
        habit_data[self.selected_day] = tasks
        save_data()
        self.load_month()
        window.destroy()
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.load_month()
        self.header.config(text=f"{self.current_month}/{self.current_year}")
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.load_month()
        self.header.config(text=f"{self.current_month}/{self.current_year}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()
