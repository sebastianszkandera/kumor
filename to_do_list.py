import json
import tkinter as tk

window = tk.Tk()
window.title("To-Do List")
window.geometry("300x400")
tasks = []
def add_task():
    task = entry.get()
    if task:
        tasks.append(task)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
def delete_task():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        listbox.delete(selected_task_index)
entry = tk.Entry(window, width=25)
entry.pack(pady=10)
add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.pack(pady=5)
delete_button = tk.Button(window, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)
listbox = tk.Listbox(window, width=25, height=15)
listbox.pack(pady=10)
window.mainloop()