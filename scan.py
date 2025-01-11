import os
import hashlib
import subprocess
import psutil  # Install with 'pip install psutil'
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def log_message(log_widget, message):
    """Helper function to log messages to the GUI."""
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)


def install_dependencies(log_widget):
    """Check and install necessary dependencies."""
    log_message(log_widget, "\n[Dependency Check]")
    dependencies = {
        'psutil': 'pip install psutil',
        'rkhunter': 'sudo apt install rkhunter',
        'ss': 'sudo apt install iproute2'
    }

    installed = []
    not_installed = []

    # Check Python dependencies
    try:
        import psutil
        installed.append('psutil')
    except ImportError:
        not_installed.append('psutil')

    # Check system dependencies
    if subprocess.call(['which', 'rkhunter'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        installed.append('rkhunter')
    else:
        not_installed.append('rkhunter')

    if subprocess.call(['which', 'ss'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        installed.append('ss')
    else:
        not_installed.append('ss')

    log_message(log_widget, f"Installed: {', '.join(installed) if installed else 'None'}")
    log_message(log_widget, f"Not Installed: {', '.join(not_installed) if not_installed else 'None'}")

    # Install missing dependencies
    if not_installed:
        for dep in not_installed:
            if dep == 'psutil':
                subprocess.run(['pip', 'install', 'psutil'])
            elif dep == 'rkhunter':
                subprocess.run(['sudo', 'apt', 'install', '-y', 'rkhunter'])
            elif dep == 'ss':
                subprocess.run(['sudo', 'apt', 'install', '-y', 'iproute2'])


def check_file_integrity(log_widget, file_paths):
    """Verify integrity of critical files using SHA256."""
    log_message(log_widget, "\n[File Integrity Check]")
    for file in file_paths:
        if os.path.exists(file):
            with open(file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            log_message(log_widget, f"{file}: {file_hash}")
        else:
            log_message(log_widget, f"{file}: File not found!")


def check_for_rootkits(log_widget):
    """Scan for rootkits using rkhunter (if installed)."""
    log_message(log_widget, "\n[Rootkit Check]")
    try:
        result = subprocess.run(['rkhunter', '--check', '--skip-keypress'], capture_output=True, text=True)
        log_message(log_widget, result.stdout)
    except FileNotFoundError:
        log_message(log_widget, "rkhunter not found. Install it with: sudo apt install rkhunter")


def check_packages(log_widget):
    """Check for broken or missing packages."""
    log_message(log_widget, "\n[Package Verification]")
    try:
        subprocess.run(['dpkg', '--audit'], check=True)
        log_message(log_widget, "No broken packages detected.")
    except subprocess.CalledProcessError:
        log_message(log_widget, "Broken packages detected. Run 'sudo apt --fix-broken install' to resolve.")


def check_processes(log_widget):
    """Monitor running processes and resource usage."""
    log_message(log_widget, "\n[Process Monitoring]")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            log_message(
                log_widget,
                f"PID: {proc.info['pid']}, Name: {proc.info['name']}, "
                f"CPU: {proc.info['cpu_percent']}%, RAM: {proc.info['memory_info'].rss / 1024 / 1024:.2f} MB"
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def check_open_ports(log_widget):
    """Check open ports on the system."""
    log_message(log_widget, "\n[Open Ports]")
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        log_message(log_widget, result.stdout)
    except FileNotFoundError:
        log_message(log_widget, "ss command not found. Install iproute2 with: sudo apt install iproute2")


def check_logs(log_widget):
    """Search logs for security-related warnings or errors."""
    log_message(log_widget, "\n[System Logs Check]")
    log_files = ['/var/log/auth.log', '/var/log/syslog']
    for log in log_files:
        if os.path.exists(log):
            log_message(log_widget, f"Checking {log} for suspicious activity...")
            try:
                with open(log, 'r') as f:
                    for line in f:
                        if 'error' in line.lower() or 'failed' in line.lower():
                            log_message(log_widget, line.strip())
            except PermissionError:
                log_message(log_widget, f"Permission denied: {log}")
        else:
            log_message(log_widget, f"{log} not found.")


def check_disk_health(log_widget):
    """Automatically detect and check disk health using smartctl with device type handling."""
    log_message(log_widget, "\n[Disk Health Check]")
    try:
        # Scan for all available disks
        result = subprocess.run(['sudo', 'smartctl', '--scan'], capture_output=True, text=True)
        if result.returncode != 0:
            log_message(log_widget, "Failed to scan for disks. Ensure smartmontools is installed.")
            return

        disks = []
        for line in result.stdout.splitlines():
            if "/dev/" in line:
                disks.append(line.split()[0])  # Extract the disk path (e.g., /dev/sda)

        if not disks:
            log_message(log_widget, "No disks detected for SMART health checks.")
            return

        # Run SMART health checks on all detected disks
        for disk in disks:
            log_message(log_widget, f"Scanning {disk}...")
            try:
                # Try with default scan first
                health_check = subprocess.run(['sudo', 'smartctl', '--health', disk], capture_output=True, text=True)
                if health_check.returncode == 0:
                    log_message(log_widget, health_check.stdout)
                    continue

                # If default fails, retry with common USB or SCSI options
                log_message(log_widget, f"Retrying {disk} with USB/SCSI detection...")
                usb_check = subprocess.run(
                    ['sudo', 'smartctl', '-d', 'usb', '-T', 'permissive', '-a', disk], capture_output=True, text=True
                )
                if "unsupported field in scsi command" in usb_check.stderr.lower():
                    log_message(log_widget, f"Skipping {disk}: Device does not support SMART.")
                else:
                    log_message(log_widget, usb_check.stdout)
            except Exception as e:
                log_message(log_widget, f"Failed to scan {disk}: {str(e)}")
    except FileNotFoundError:
        log_message(log_widget, "smartctl not found. Install it with: sudo apt install smartmontools")


def main():
    """Main function to run the diagnostic tests."""
    # Create the GUI window
    root = tk.Tk()
    root.title("Linux System Scanner v2")
    root.geometry("800x600")

    # Create a scrollable text widget with black background and red text
    log_widget = ScrolledText(root, wrap=tk.WORD, width=100, height=30, bg='black', fg='red')
    log_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    log_message(log_widget, "Linux System Scanner v1.0\n")

    # Install dependencies
    install_dependencies(log_widget)

    # Define files to check for integrity (example paths)
    critical_files = ['/etc/passwd', '/etc/shadow', '/bin/bash']

    # Run diagnostic checks
    check_file_integrity(log_widget, critical_files)
    check_for_rootkits(log_widget)
    check_packages(log_widget)
    check_processes(log_widget)
    check_open_ports(log_widget)
    check_logs(log_widget)
    check_disk_health(log_widget)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == '__main__':
    main()
