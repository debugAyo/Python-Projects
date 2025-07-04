import tkinter as tk
from tkinter import messagebox
import time
import winsound

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.time_left = 0
        self.running = False
        self.paused = False
        self.after_id = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter seconds:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.entry.pack(pady=5)

        self.time_display = tk.Label(self.root, text="00:00", font=("Arial", 32))
        self.time_display.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.start_btn = tk.Button(btn_frame, text="Start", width=8, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=2)

        self.pause_btn = tk.Button(btn_frame, text="Pause", width=8, command=self.pause_timer, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=1, padx=2)

        self.resume_btn = tk.Button(btn_frame, text="Resume", width=8, command=self.resume_timer, state=tk.DISABLED)
        self.resume_btn.grid(row=0, column=2, padx=2)

        self.reset_btn = tk.Button(self.root, text="Reset", width=26, command=self.reset_timer, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)

    def start_timer(self):
        try:
            seconds = int(self.entry.get())
            if seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer.")
            return
        self.time_left = seconds
        self.update_display()
        self.running = True
        self.paused = False
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)
        self.countdown()

    def countdown(self):
        if self.running and not self.paused:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_display()
                self.after_id = self.root.after(1000, self.countdown)
            else:
                self.update_display()
                self.running = False
                self.pause_btn.config(state=tk.DISABLED)
                self.resume_btn.config(state=tk.DISABLED)
                self.start_btn.config(state=tk.NORMAL)
                self.entry.config(state=tk.NORMAL)
                winsound.Beep(1000, 500)
                messagebox.showinfo("Time's up!", "Countdown finished!")

    def pause_timer(self):
        if self.running and not self.paused:
            self.paused = True
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.NORMAL)

    def resume_timer(self):
        if self.running and self.paused:
            self.paused = False
            self.pause_btn.config(state=tk.NORMAL)
            self.resume_btn.config(state=tk.DISABLED)
            self.countdown()

    def reset_timer(self):
        self.running = False
        self.paused = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.time_left = 0
        self.update_display()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)

    def update_display(self):
        mins, secs = divmod(self.time_left, 60)
        self.time_display.config(text=f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
