import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Function to execute the command
def start_scanning():
    try:
        subprocess.run(["sudo", "python3", "scan.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Create the main application window
root = tk.Tk()
root.title("Linux Scan(DEBAIN)")

# Set the dimensions of the window (optional customization)
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

# Create the "Start Scanning" button
scan_button = tk.Button(root, text="Start Scan", font=("Arial", 16), bg="blue", fg="white", command=start_scanning)
scan_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the button

# Run the application
root.mainloop()
