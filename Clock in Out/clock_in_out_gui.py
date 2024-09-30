import csv
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox, font

class ClockInOut:
    def __init__(self, log_file='clock_in_out_log.csv'):
        self.log_file = log_file
        self.logs = self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        return []

    def clock_in(self):
        now = datetime.now()
        entry = {
            'action': 'clock_in',
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': now.strftime('%Y-%m-%d')  # Add date here
        }
        self.logs.append(entry)
        self.save_logs()
        return f"Clocked in at {entry['timestamp']}"

    def clock_out(self):
        now = datetime.now()
        entry = {
            'action': 'clock_out',
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': now.strftime('%Y-%m-%d')  # Add date here
        }
        self.logs.append(entry)
        self.save_logs()
        return f"Clocked out at {entry['timestamp']}"

    def save_logs(self):
        with open(self.log_file, 'w', newline='') as file:
            fieldnames = ['task', 'clock_in', 'clock_out', 'total_time', 'date']  # Add date to fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.logs)

    def view_logs(self):
        if not self.logs:
            return "No logs found."
        return "\n".join(f"{log['action'].capitalize()} at {log['timestamp']} on {log['date']}" for log in self.logs)


class ClockInOutApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Clock In / Clock Out Module")

        # Set the icon for the window
        self.master.iconbitmap(self.get_icon_path())

        self.master.configure(bg="#000000")

        # Container frame
        self.container = tk.Frame(master, bg="#000000", bd=4, relief=tk.RAISED)
        self.container.pack(padx=20, pady=20)

        # Define independent Georgia font sizes for each widget
        self.title_font = ('Georgia', 24)  # Larger font for title
        self.label_font = ('Georgia', 12)  # Standard font for labels
        self.entry_font = ('Georgia', 12)  # Font for entry
        self.button_font = ('Georgia', 12)  # Font for buttons
        self.time_display_font = ('Georgia', 10)  # Smaller font for time displays

        # Title label
        self.title_label = tk.Label(self.container, text="Clock In / Clock Out", bg="#000000", fg="#ffffff", font=self.title_font)
        self.title_label.pack(pady=10)

        # Task label
        self.task_label = tk.Label(self.container, text="Task:", bg="#000000", fg="#ffffff", font=self.label_font)
        self.task_label.pack(pady=5)

        # Task input field
        self.task_input = tk.Entry(self.container, font=self.entry_font)
        self.task_input.pack(pady=10)

        # Clock In button
        self.btn_clock_in = tk.Button(self.container, text="Clock In", command=self.clock_in, bg="#ffffff", fg="#000000", font=self.button_font)
        self.btn_clock_in.pack(pady=10)

        # Clock Out button
        self.btn_clock_out = tk.Button(self.container, text="Clock Out", command=self.clock_out, bg="#ffffff", fg="#000000", state=tk.DISABLED, font=self.button_font)
        self.btn_clock_out.pack(pady=10)

        # Time display
        self.clock_in_time_label = tk.Label(self.container, text="Clock In Time: Not yet", bg="#000000", fg="#ffffff", font=self.time_display_font)
        self.clock_in_time_label.pack(pady=5)

        self.clock_out_time_label = tk.Label(self.container, text="Clock Out Time: Not yet", bg="#000000", fg="#ffffff", font=self.time_display_font)
        self.clock_out_time_label.pack(pady=5)

        self.total_time_worked_label = tk.Label(self.container, text="Total Time Worked: N/A", bg="#000000", fg="#ffffff", font=self.time_display_font)
        self.total_time_worked_label.pack(pady=5)

        self.clock = ClockInOut()
        self.clock_in_time = None

    def get_icon_path(self):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'logo.ico')
        else:
            return 'logo.ico'
    def clock_in(self):
        self.clock_in_time = datetime.now()
        self.clock_in_time_label.config(text=f"Clock In Time: {self.clock_in_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.btn_clock_out.config(state=tk.NORMAL)
        self.btn_clock_in.config(state=tk.DISABLED)

    def clock_out(self):
        clock_out_time = datetime.now()
        self.clock_out_time_label.config(text=f"Clock Out Time: {clock_out_time.strftime('%Y-%m-%d %H:%M:%S')}")
        total_time_worked = self.calculate_time_difference(self.clock_in_time, clock_out_time)
        self.total_time_worked_label.config(text=f"Total Time Worked: {total_time_worked}")
        self.btn_clock_out.config(state=tk.DISABLED)
        self.btn_clock_in.config(state=tk.NORMAL)

        # Append log to the clock instance
        task_name = self.task_input.get()
        self.clock.logs.append({
            'task': task_name,
            'clock_in': self.clock_in_time.strftime('%H:%M:%S'),
            'clock_out': clock_out_time.strftime('%H:%M:%S'),
            'total_time': total_time_worked,
            'date': self.clock_in_time.strftime('%Y-%m-%d')  # Add date here
        })
        self.clock.save_logs()

    def calculate_time_difference(self, start_time, end_time):
        if start_time and end_time:
            diff = end_time - start_time
            hours, remainder = divmod(diff.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        return "00:00:00"

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockInOutApp(root)
    root.mainloop()
