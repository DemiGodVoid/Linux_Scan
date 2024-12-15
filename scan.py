import os
import hashlib
import subprocess
import psutil  # Install with 'pip install psutil'

def install_dependencies():
    """Check and install necessary dependencies."""
    print("\n[Dependency Check]")
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

    print("Installed:", ", ".join(installed) if installed else "None")
    print("Not Installed:", ", ".join(not_installed) if not_installed else "None")

    # Install missing dependencies
    if not_installed:
        for dep in not_installed:
            if dep == 'psutil':
                subprocess.run(['pip', 'install', 'psutil'])
            elif dep == 'rkhunter':
                subprocess.run(['sudo', 'apt', 'install', '-y', 'rkhunter'])
            elif dep == 'ss':
                subprocess.run(['sudo', 'apt', 'install', '-y', 'iproute2'])

def check_file_integrity(file_paths):
    """Verify integrity of critical files using SHA256."""
    print("\n[File Integrity Check]")
    for file in file_paths:
        if os.path.exists(file):
            with open(file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"{file}: {file_hash}")
        else:
            print(f"{file}: File not found!")

def check_for_rootkits():
    """Scan for rootkits using rkhunter (if installed)."""
    print("\n[Rootkit Check]")
    try:
        result = subprocess.run(['rkhunter', '--check', '--skip-keypress'], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("rkhunter not found. Install it with: sudo apt install rkhunter")

def check_packages():
    """Check for broken or missing packages."""
    print("\n[Package Verification]")
    try:
        subprocess.run(['dpkg', '--audit'], check=True)
        print("No broken packages detected.")
    except subprocess.CalledProcessError:
        print("Broken packages detected. Run 'sudo apt --fix-broken install' to resolve.")

def check_processes():
    """Monitor running processes and resource usage."""
    print("\n[Process Monitoring]")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU: {proc.info['cpu_percent']}%, RAM: {proc.info['memory_info'].rss / 1024 / 1024:.2f} MB")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def check_open_ports():
    """Check open ports on the system."""
    print("\n[Open Ports]")
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("ss command not found. Install iproute2 with: sudo apt install iproute2")

def check_logs():
    """Search logs for security-related warnings or errors."""
    print("\n[System Logs Check]")
    log_files = ['/var/log/auth.log', '/var/log/syslog']
    for log in log_files:
        if os.path.exists(log):
            print(f"Checking {log} for suspicious activity...")
            try:
                with open(log, 'r') as f:
                    for line in f:
                        if 'error' in line.lower() or 'failed' in line.lower():
                            print(line.strip())
            except PermissionError:
                print(f"Permission denied: {log}")
        else:
            print(f"{log} not found.")

def main():
    print("Linux System Scanner v1.0")

    # Install dependencies
    install_dependencies()

    # Define files to check for integrity (example paths)
    critical_files = ['/etc/passwd', '/etc/shadow', '/bin/bash']

    # Run the checks
    check_file_integrity(critical_files)
    check_for_rootkits()
    check_packages()
    check_processes()
    check_open_ports()
    check_logs()

if __name__ == '__main__':
    main()
