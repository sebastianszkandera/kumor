import json
import os
import tkinter as tk
from tkinter import messagebox

# Store user data in a JSON file alongside this script.
DATA_FILE = os.path.join(os.path.dirname(__file__), "names_passwords.json")

# Load existing user data from JSON (or initialize an empty dictionary).
# If the file is missing, empty, or invalid, start with an empty store.
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        names_passwords = json.load(f) or {}
except (FileNotFoundError, json.JSONDecodeError):
    names_passwords = {}


def open_registration_window():
    """Open a registration dialog as a separate window."""

    def on_submit():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        password_confirm = password_confirm_entry.get().strip()
        if not username or not password or not password_confirm:
            messagebox.showwarning("Validation", "Please enter username, password and password confirmation.")
            return
        if password != password_confirm:
            messagebox.showwarning("Validation", "Passwords do not match.")
            return
        if username in names_passwords:
            messagebox.showwarning("Validation", "That username is already registered.")
            return

        # Save credentials (in a real app, never store plain-text passwords).
        names_passwords[username] = password
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(names_passwords, f, indent=2)
        except OSError as e:
            messagebox.showerror("Registration", f"Failed to save user data: {e}")
            return

        messagebox.showinfo("Registration", f"Registration successful!\nUsername: {username}")
        register_win.destroy()

    register_win = tk.Toplevel(root)
    register_win.title("Register")
    register_win.resizable(False, False)

    tk.Label(register_win, text="Username:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
    username_entry = tk.Entry(register_win)
    username_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(register_win, text="Password:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
    password_entry = tk.Entry(register_win, show="*")
    password_entry.grid(row=1, column=1, padx=8, pady=8)
    
    tk.Label(register_win, text="Confirm Password:").grid(row=2, column=0, padx=8, pady=8, sticky="e")
    password_confirm_entry = tk.Entry(register_win, show="*")
    password_confirm_entry.grid(row=2, column=1, padx=8, pady=8)

    submit_button = tk.Button(register_win, text="Submit", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(0, 8))
        


root = tk.Tk()
root.title("simple app")

reg_button = tk.Button(root, text="Register", command=open_registration_window)
reg_button.pack(padx=16, pady=(16, 8), fill="x")

login_button = tk.Button(root, text="Login", command=lambda: on_login(root))
login_button.pack(padx=16, pady=(0, 16), fill="x")


def on_login(parent):
    
    def on_submit():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Validation", "Please enter username and password.")
            return
        if username in names_passwords and names_passwords[username] == password:
            messagebox.showinfo("Login", f"Login successful!\nWelcome, {username}")
        else:
            messagebox.showerror("Login", "Invalid username or password.")
    login_win = tk.Toplevel(parent)
    login_win.title("Login")
    login_win.resizable(False, False)

    tk.Label(login_win, text="Username:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
    username_entry = tk.Entry(login_win)
    username_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(login_win, text="Password:").grid(row=1, column=0, padx=8, pady=8, sticky="e")
    password_entry = tk.Entry(login_win, show="*")
    password_entry.grid(row=1, column=1, padx=8, pady=8)

    submit_button = tk.Button(login_win, text="Submit", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2, pady=(0, 8))
root.mainloop()