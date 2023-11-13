import tkinter as tk
from tkinter import simpledialog
import os
import subprocess
from time import sleep

# The directory to store the images
IMAGE_DIR = "/directory/to/save/images"

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

def set_interval():
    global interval
    interval = simpledialog.askinteger("Input", "Enter the time interval in seconds",
                                      parent=root)
    if interval is None:
        interval = 1  # Default to 1 second if no input is provided

def preview():
    # Command to preview the images using libcamera
    command = f"libcamera-vid -t 0 --display 0 --fullscreen"
    subprocess.run(command, shell=True)

# GUI setup
root = tk.Tk()
root.title("Time-Lapse Controller")

interval = 1  # Default interval of 1 second
running = False

# Set interval button
set_interval_button = tk.Button(root, text="Set Interval", command=set_interval)
set_interval_button.pack()

# Start/Stop button
start_stop_button = tk.Button(root, text="Start Time-Lapse", command=lambda: start_time_lapse(interval) if not running else stop_time_lapse())
start_stop_button.pack()

# Preview button
preview_button = tk.Button(root, text="Preview", command=preview)
preview_button.pack()

root.mainloop()
