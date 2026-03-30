import random
import tkinter as tk
import time
import random

def clicker_simulator():
    root = tk.Tk()
    root.title("Clicker Simulator")
    
    click_count = 0
    click_label = tk.Label(root, text=f"Clicks: {click_count}", font=("Arial", 20))
    click_label.pack(pady=20)
    
    # Track used messages to avoid immediate repeats
    available_messages = [
        "wow, you are really good at clicking!",
        "you are really enjoying this, aren't you?",
        "you really want to click more?",
        "don't you have anything better to do?",
        "go find a girlfriend, you lonely piece of shit!"
    ]
    used_messages = []
    
    def show_message_window(message):
        """Create a new window to display a message"""
        msg_window = tk.Toplevel(root)
        msg_window.title("Message")
        msg_window.geometry("400x200")
        
        msg_label = tk.Label(msg_window, text=message, font=("Arial", 16), wraplength=350)
        msg_label.pack(pady=30, padx=20)
        
        close_button = tk.Button(msg_window, text="OK", command=msg_window.destroy, font=("Arial", 12))
        close_button.pack(pady=10)
    
    def get_random_message():
        """Get a random message that hasn't been used recently"""
        nonlocal available_messages, used_messages
        
        # If no messages available, reset the pool
        if not available_messages:
            available_messages = used_messages.copy()
            used_messages = []
        
        # Pick a random message from available ones
        message = random.choice(available_messages)
        available_messages.remove(message)
        used_messages.append(message)
        
        return message
    
    def on_click():
        nonlocal click_count
        click_count += 1
        click_label.config(text=f"Clicks: {click_count}")
        
        # Show first message when click count is 1
        if click_count == 1:
            first_message = "congratulations, your stupid head understood the concept!"
            show_message_window(first_message)
        
        # Show random message every 10 clicks (10, 20, 30, etc.)
        elif click_count % 10 == 0:
            random_message = get_random_message()
            show_message_window(random_message)
    
    click_button = tk.Button(root, text="Click Me!", font=("Arial", 20), command=on_click)
    click_button.pack(pady=20)

    root.mainloop()

clicker_simulator()