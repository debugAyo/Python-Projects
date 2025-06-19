import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Variables
        self.current = ""
        self.operation = ""
        self.first_number = 0
        self.should_clear = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display
        self.display = tk.Entry(self.root, font=("Arial", 24), justify="right", bd=10)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # Create and place buttons
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            btn = tk.Button(self.root, text=button, font=("Arial", 18),
                          width=4, height=2, command=cmd)
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Clear button
        clear_btn = tk.Button(self.root, text="C", font=("Arial", 18),
                            width=4, height=2, command=self.clear)
        clear_btn.grid(row=5, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def click(self, key):
        if key == '=':
            try:
                result = eval(self.current)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current = str(result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current = ""
        else:
            if self.should_clear:
                self.display.delete(0, tk.END)
                self.should_clear = False
            self.current += key
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
    
    def clear(self):
        self.current = ""
        self.display.delete(0, tk.END)
        self.should_clear = False

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()