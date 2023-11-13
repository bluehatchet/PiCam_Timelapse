import tkinter as tk
from tkinter import Toplevel
import os
import subprocess
from time import sleep

# The directory to store the images
IMAGE_DIR = "/path/to/save/images"

# Check if the image directory exists, if not create it
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def capture_image(image_number):
    # Command to capture an image using libcamera
    command = f"libcamera-still -o {IMAGE_DIR}/image{image_number:04d}.jpg"
    subprocess.run(command, shell=True)

def start_time_lapse(interval):
    global running
    running = True
    image_number = 0
    while running:
        capture_image(image_number)
        image_number += 1
        sleep(interval)

def stop_time_lapse():
    global running
    running = False

def set_interval(n):
    global interval
    interval = n
    # Close any open interval selection window
    if 'interval_popup' in globals():
        interval_popup.destroy()

def show_interval_popup():
    # Create a new pop-up window for interval selection
    global interval_popup
    interval_popup = Toplevel(root)
    interval_popup.title("Select Interval")
    intervals = [10, 20, 30, 60, 300, 600, 1800, 3600, 14400, 86400]
    for i, val in enumerate(intervals):
        tk.Button(interval_popup, text=str(val), command=lambda val=val: set_interval(val)).grid(row=i // 5, column=i % 5)
    interval_popup.transient(root)  # Set to be always on top of the main window

def preview():
    # Command to preview the images using libcamera
    command = f"libcamera-vid -t 0 --display 0 --fullscreen"
    subprocess.run(command, shell=True)

# GUI setup
root = tk.Tk()
root.title("Time-Lapse Controller")
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

interval = 10  # Default interval to the first in the list
running = False

# Set interval button
set_interval_button = tk.Button(button_frame, text="Set Interval", command=show_interval_popup)
set_interval_button.pack(side=tk.LEFT)

# Start/Stop button
start_stop_button = tk.Button(button_frame, text="Start Time-Lapse", command=lambda: start_time_lapse(interval) if not running else stop_time_lapse())
start_stop_button.pack(side=tk.LEFT)

# Preview button
preview_button = tk.Button(button_frame, text="Preview", command=preview)
preview_button.pack(side=tk.LEFT)

root.mainloop()
