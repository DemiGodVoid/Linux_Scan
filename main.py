import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from PIL import Image, ImageTk
import subprocess
import os
import time

# Function to execute the scanning command after the countdown
def start_scanning():
    def countdown_and_start():
        # Create a new popup window for the countdown
        countdown_popup = Toplevel(root)
        countdown_popup.title("Starting Scan")
        countdown_popup.geometry("300x150")
        countdown_popup.configure(bg="black")
        
        # Add countdown label
        countdown_label = Label(countdown_popup, text="Starting in 4 seconds", font=("Arial", 14), fg="white", bg="black")
        countdown_label.pack(pady=10)

        # Add instruction label
        instruction_label = Label(
            countdown_popup, 
            text="Scanner takes awhile to scan, sit back and drink some coffee.", 
            font=("Arial", 12), 
            fg="white", 
            bg="black",
            wraplength=250
        )
        instruction_label.pack(pady=10)

        # Countdown logic
        for i in range(4, 0, -1):
            countdown_label.config(text=f"Starting in {i} seconds")
            countdown_popup.update()
            time.sleep(1)

        # Close the popup and start scanning
        countdown_popup.destroy()
        try:
            subprocess.run(["sudo", "python3", "scan.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    # Run countdown in the main loop
    root.after(10, countdown_and_start)

# Function to kill user applications (excluding critical ones)
def kill_all_apps():
    try:
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Action",
            "Are you sure you want to KILL ALL APPS?\n\n"
            "May cause your computer to crash/restart."
        )
        if not confirm:
            return  # Exit if the user selects "No"

        # List of processes to exclude (e.g., shell, desktop environment, etc.)
        exclude_list = ["gnome-shell", "Xorg", "wayland", "kdeinit", "plasmashell", "systemd"]

        # Get a list of running processes for the user
        result = subprocess.run(["ps", "-u", os.getlogin(), "-o", "pid,comm"], text=True, capture_output=True)
        processes = result.stdout.splitlines()[1:]  # Skip the header line

        # Kill processes not in the exclude list
        for process in processes:
            pid, command = process.strip().split(maxsplit=1)
            if command not in exclude_list:
                subprocess.run(["kill", "-9", pid])  # Force kill the process

        print("Non-critical applications have been terminated.")
    except subprocess.CalledProcessError as e:
        print(f"Error while killing applications: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to open the settings file
def open_settings():
    try:
        subprocess.run(["python3", "settings.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening settings: {e}")
    except FileNotFoundError:
        print("Error: 'settings.py' not found.")

# Create the main application window
root = tk.Tk()
root.title("Linux Scan(DEBIAN)")

# Set the dimensions of the window
window_width = 800
window_height = 600

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Load and set the background image
if os.path.exists("test.jpg"):
    image = Image.open("test.jpg")
    image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # Resize image to fit window
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the window
else:
    print("Error: Background image 'test.jpg' not found.")

# Create a frame to stack the center buttons vertically
button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create the "Start Scanning" button
scan_button = tk.Button(button_frame, text="Start Scan", font=("Arial", 16), bg="blue", fg="white", command=start_scanning)
scan_button.pack(pady=10)  # Add vertical spacing between buttons

# Create the "KILL ALL APPS" button
kill_button = tk.Button(button_frame, text="KILL ALL APPS", font=("Arial", 16), bg="red", fg="white", command=kill_all_apps)
kill_button.pack(pady=10)  # Add vertical spacing between buttons

# Add the "Settings" button in the top-right corner
settings_button = tk.Button(root, text="⚙", font=("Arial", 16), bg="grey", fg="white", command=open_settings)
settings_button.place(relx=0.98, rely=0.02, anchor=tk.NE)  # Top-right corner

# Run the application
root.mainloop()
