import json
import datetime
import os

DATA_FILE = "habit_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": {}, "last_opened": str(datetime.date.today())}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_task(data, task_name):
    if task_name not in data["tasks"]:
        data["tasks"][task_name] = {}
        print(f"Added task: {task_name}")
    else:
        print("Task already exists.")

def remove_task(data, task_name):
    if task_name in data["tasks"]:
        del data["tasks"][task_name]
        print(f"Removed task: {task_name}")
    else:
        print("Task not found.")

def mark_task(data, task_name, date, completed=True):
    if task_name in data["tasks"]:
        data["tasks"][task_name][date] = completed
        print(f"Marked '{task_name}' as {'completed' if completed else 'not completed'} on {date}.")
    else:
        print("Task not found.")

def show_tasks(data):
    print("\nHabit Tracker:")
    for task, days in data["tasks"].items():
        print(f"{task}: {days}")

def check_missed_days(data):
    last_opened = datetime.date.fromisoformat(data["last_opened"])
    today = datetime.date.today()
    missed_days = []
    
    while last_opened < today:
        last_opened += datetime.timedelta(days=1)
        missed_days.append(str(last_opened))
    
    if missed_days:
        print("\nYou haven't logged habits for these days:", ", ".join(missed_days))
    
    data["last_opened"] = str(today)

def main():
    data = load_data()
    check_missed_days(data)
    
    while True:
        cmd = input("\nEnter a command (add/remove/mark/unmark/show/quit): ").strip().lower()
        
        if cmd == "add":
            task = input("Enter task name: ").strip()
            add_task(data, task)
        elif cmd == "remove":
            task = input("Enter task name: ").strip()
            remove_task(data, task)
        elif cmd in ["mark", "unmark"]:
            task = input("Enter task name: ").strip()
            date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip()
            if not date:
                date = str(datetime.date.today())
            mark_task(data, task, date, completed=(cmd == "mark"))
        elif cmd == "show":
            show_tasks(data)
        elif cmd == "quit":
            save_data(data)
            print("Progress saved. Exiting...")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
