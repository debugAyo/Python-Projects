import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_var.get())
        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4.")
            return

        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]
        if length > 4:
            all_chars = string.ascii_letters + string.digits + string.punctuation
            password += random.choices(all_chars, k=length-4)
        random.shuffle(password)
        password_str = ''.join(password)
        password_var.set(password_str)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def copy_to_clipboard():
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

root = tk.Tk()
root.title("Password Generator")
root.geometry("350x200")
root.resizable(False, False)


length_var = tk.StringVar(value="12")
password_var = tk.StringVar()

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=length_var, width=5, justify='center').grid(row=0, column=1, padx=5)

tk.Button(frame, text="Generate Password", command=generate_password).grid(row=1, column=0, columnspan=2, pady=10)

tk.Entry(frame, textvariable=password_var, width=30, font=("Arial", 12), justify='center', state='readonly').grid(row=2, column=0, columnspan=2, pady=5)

tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()