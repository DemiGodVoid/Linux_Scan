import tkinter as tk

# Create the settings window
settings = tk.Tk()
settings.title("Settings")

# Set the dimensions of the window
window_width = 400
window_height = 300

# Center the window on the screen
screen_width = settings.winfo_screenwidth()
screen_height = settings.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
settings.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Set the background color to black
settings.configure(bg="black")

# Add a horizontal line
separator = tk.Frame(settings, height=2, bd=1, relief="sunken", bg="white")
separator.pack(fill="x", padx=20, pady=20)

# Add the "VERSION" label
version_label = tk.Label(settings, text="VERSION", font=("Arial", 16, "bold"), fg="white", bg="black")
version_label.pack(pady=(20, 5))  # Add some spacing at the top

# Add the version message
version_message = tk.Label(settings, text="2", font=("Arial", 14), fg="white", bg="black")
version_message.pack()

# Add a horizontal line
separator = tk.Frame(settings, height=2, bd=1, relief="sunken", bg="white")
separator.pack(fill="x", padx=20, pady=20)

# Add the "RELEASED" label
released_label = tk.Label(settings, text="RELEASED", font=("Arial", 16, "bold"), fg="white", bg="black")
released_label.pack(pady=(20, 5))  # Add some spacing at the top

# Add the RELEASED message
released_message = tk.Label(settings, text="1/10/25", font=("Arial", 14), fg="white", bg="black")
released_message.pack()

# Add a horizontal line
separator = tk.Frame(settings, height=2, bd=1, relief="sunken", bg="white")
separator.pack(fill="x", padx=20, pady=20)

# Add the "CREATOR" label
creator_label = tk.Label(settings, text="CREATOR", font=("Arial", 16, "bold"), fg="white", bg="black")
creator_label.pack(pady=(10, 5))

# Add the creator message
creator_message = tk.Label(settings, text="Made by void", font=("Arial", 14), fg="white", bg="black")
creator_message.pack()

# Add a horizontal line
separator = tk.Frame(settings, height=2, bd=1, relief="sunken", bg="white")
separator.pack(fill="x", padx=20, pady=20)

# Add the "UPDATES" label
updates_label = tk.Label(settings, text="UPDATES", font=("Arial", 16, "bold"), fg="white", bg="black")
updates_label.pack(pady=(10, 5))

# Add the updates message with line breaks and word wrapping
updates_message = tk.Label(
    settings,
    text="VERSION:2\n\nAdded: KILL ALL APPS option, this will kill apps that are running/running in the background.\n\nAdded: CountDown prompt, so you know for sure the scan has started.\n\nAdded:Settings Page.\n\nChanged: Scanners background page to black and text to red.\n\n\nUPDATES\n\nVERSION:1\n\nAdded:Scanner with menu.",
    font=("Arial", 14),
    fg="white",
    bg="black",
    wraplength=window_width - 40  # Adjust based on your window width
)
updates_message.pack()

# Run the settings window
settings.mainloop()
