import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

#Database setup
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

#Functions
def add_transaction():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()
    if not date or not category or not amount:
        messagebox.showwarning("Input Error", "Date, Category, and Amount are required.")
        return
    try:
        float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return
    cursor.execute("INSERT INTO transactions (date, category, amount, description) VALUES (?, ?, ?, ?)",
                       (date, category, amount, description))
    conn.commit()
    refresh_transactions()
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)
def refresh_transactions():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT date, category, amount, description FROM transactions ORDER By date DESC")
        for row in cursor.fetchall():
            tree.insert('', tk.END, values=row)
def load_selected_transaction(event):
     selected = tree.focus()
     if not selected:
          return
          values = tree.item(selected, 'values')
          if values:
               entry_date.delete(0, tk.END)
               entry_date.insert(0, values[0])
               entry_category.delete(0, tk.END)
               entry_category.insert(0, values[1])
               entry_amount.delete(0, tk.END)
               entry_amount.insert(0, values[2])
               entry_description.delete(0, tk.END)
               entry_description.insert(0, values[3])

def update_transaction():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No selection", "Please select a transaction to update.")
        return

    values = tree.item(selected, 'values')
    if not values:
        messagebox.showwarning("No Data", "Selected row has no data.")
        return

    # Get new values from entry fields
    new_date = entry_date.get()
    new_category = entry_category.get()
    new_amount = entry_amount.get()
    new_description = entry_description.get()

    if not new_date or not new_category or not new_amount:
        messagebox.showwarning("Input Error", "Date, Category, and Amount are required.")
        return

    try:
        float(new_amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return

    # Update the transaction in the database
    cursor.execute("""
        UPDATE transactions
        SET date=?, category=?, amount=?, description=?
        WHERE date=? AND category=? AND amount=? AND description=?
    """, (
        new_date, new_category, new_amount, new_description,
        values[0], values[1], values[2], values[3]
    ))
    conn.commit()
    refresh_transactions()
    update_dashboard()
    messagebox.showinfo("Success", "Transaction updated successfully.")


     
    

    
    #GUI Setup
root = tk.Tk()
root.title("Beta Finance Tracker")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Date (YYYY-MM-DD:").grid(row=0, column=0)
entry_date = tk.Entry(frame)
entry_date.grid(row=0, column=1)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(frame, text="Category:").grid(row=1, column=0)
entry_category = tk.Entry(frame)
entry_category.grid(row=1, column=1)

tk.Label(frame, text="Amount:").grid(row=2, column=0)
entry_amount = tk.Entry(frame)
entry_amount.grid(row=2, column=1)

tk.Label(frame, text="Description:").grid(row=3, column=0)
entry_description = tk.Entry(frame)
entry_description.grid(row=3, column=1)

tk.Button(frame, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Update Transaction", command=update_transaction).grid(row=5, column=0, columnspan=2, pady=5)

tree= ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show="headings")
for col in ("Date", "Category", "Amount", "Description"):
        tree.heading(col, text=col)
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tree.bind('<<TreeviewSelect>>', load_selected_transaction)
refresh_transactions()

root.mainloop()






