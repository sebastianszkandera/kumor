import json
import time
import datetime
import tkinter as tk
from tkinter import messagebox

class ReminderApp:
    def __init__(self, master):
        self.master = master
        master.title("Reminder App")
        master.geometry("360x320")
        self.reminders = []
        self.load_reminders()
        self.create_widgets()
        self.check_reminders()

    def create_widgets(self):
        tk.Label(self.master, text="Reminder text:").pack(pady=2)
        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(pady=2)

        tk.Label(self.master, text="Date (YYYY-MM-DD):").pack(pady=2)
        self.date_entry = tk.Entry(self.master, width=15)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.date_entry.pack(pady=2)

        tk.Label(self.master, text="Time (HH:MM, 24h):").pack(pady=2)
        self.time_entry = tk.Entry(self.master, width=15)
        self.time_entry.insert(0, datetime.datetime.now().strftime("%H:%M"))
        self.time_entry.pack(pady=2)

        tk.Label(self.master, text="Repeat every:").pack(pady=2)
        self.frequency_var = tk.StringVar(value="none")
        self.frequency_menu = tk.OptionMenu(self.master, self.frequency_var, "none", "daily", "weekly", "monthly")
        self.frequency_menu.pack(pady=2)

        self.add_button = tk.Button(self.master, text="Add Reminder", command=self.add_reminder)
        self.delete_button = tk.Button(self.master, text="Delete Reminder", command=self.delete_reminder)
        self.add_button.pack(pady=5)
        self.delete_button.pack(pady=5)

        self.reminder_listbox = tk.Listbox(self.master, width=40, height=8)
        self.reminder_listbox.pack(pady=10)
        self.update_reminder_listbox()

    def add_reminder(self):
        reminder_text = self.entry.get().strip()
        date_text = self.date_entry.get().strip()
        time_text = self.time_entry.get().strip()
        frequency = self.frequency_var.get()

        if not reminder_text:
            messagebox.showwarning("Validation", "Please enter reminder text.")
            return

        try:
            scheduled_dt = datetime.datetime.fromisoformat(f"{date_text}T{time_text}")
        except ValueError:
            messagebox.showerror("Invalid Date/Time", "Please enter date and time in correct format.")
            return

        if scheduled_dt < datetime.datetime.now():
            messagebox.showwarning("Past Time", "Selected time is in the past. Please choose future time.")
            return

        reminder = {
            "text": reminder_text,
            "next_time": scheduled_dt.timestamp(),
            "frequency": frequency,
            "orig_date": date_text,
            "orig_time": time_text,
        }

        self.reminders.append(reminder)
        self.save_reminders()
        self.update_reminder_listbox()
        self.entry.delete(0, tk.END)

    def delete_reminder(self):
        selected_index = self.reminder_listbox.curselection()
        if selected_index:
            self.reminders.pop(selected_index[0])
            self.save_reminders()
            self.update_reminder_listbox()

    def update_reminder_listbox(self):
        self.reminder_listbox.delete(0, tk.END)
        for reminder in self.reminders:
            due = datetime.datetime.fromtimestamp(reminder.get("next_time", 0))
            label = f"{reminder['text']} @ {due.strftime('%Y-%m-%d %H:%M')} [{reminder.get('frequency', 'none')} ]"
            self.reminder_listbox.insert(tk.END, label)

    def save_reminders(self):
        with open("reminders.json", "w") as f:
            json.dump(self.reminders, f)

    def load_reminders(self):
        try:
            with open("reminders.json", "r") as f:
                self.reminders = json.load(f)

            for reminder in self.reminders:
                if "next_time" not in reminder and "orig_date" in reminder and "orig_time" in reminder:
                    try:
                        dt = datetime.datetime.fromisoformat(f"{reminder['orig_date']}T{reminder['orig_time']}")
                        reminder["next_time"] = dt.timestamp()
                    except Exception:
                        reminder["next_time"] = time.time() + 60
                elif "next_time" not in reminder:
                    reminder["next_time"] = time.time() + 60
        except FileNotFoundError:
            self.reminders = []

    def check_reminders(self):
        now_ts = time.time()
        fired_any = False
        for reminder in list(self.reminders):
            if now_ts >= reminder.get("next_time", float('inf')):
                messagebox.showinfo("Reminder", f"{reminder['text']}\n(Repeated: {reminder.get('frequency','none')})")
                frequency = reminder.get("frequency", "none")
                if frequency == "daily":
                    next_dt = datetime.datetime.fromtimestamp(reminder["next_time"]) + datetime.timedelta(days=1)
                    reminder["next_time"] = next_dt.timestamp()
                elif frequency == "weekly":
                    next_dt = datetime.datetime.fromtimestamp(reminder["next_time"]) + datetime.timedelta(weeks=1)
                    reminder["next_time"] = next_dt.timestamp()
                elif frequency == "monthly":
                    current = datetime.datetime.fromtimestamp(reminder["next_time"])
                    month = current.month + 1
                    year = current.year
                    if month > 12:
                        month = 1
                        year += 1
                    day = min(current.day, [31, 29 if (year%4==0 and (year%100!=0 or year%400==0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
                    reminder["next_time"] = datetime.datetime(year, month, day, current.hour, current.minute).timestamp()
                else:
                    self.reminders.remove(reminder)
                fired_any = True

        if fired_any:
            self.save_reminders()
            self.update_reminder_listbox()

        self.master.after(1000, self.check_reminders)

    def callendar_selection_for_reminders(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
