import tkinter as tk
from tkinter import scrolledtext
import socket
import subprocess
import platform
import json
import threading


# === Core Logic === #
def scan_ports(host, ports=[21, 22, 23, 80, 443, 3306, 8080]):
    open_ports = []
    log(f"Scanning {host} for open ports...")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                log(f"[+] Port {port} is open")
                open_ports.append(port)
            sock.close()
        except socket.error as err:
            log(f"Socket error: {err}")
    return open_ports

def check_os_version():
    os_info = platform.platform()
    log(f"[+] Operating System Info: {os_info}")
    return os_info

def check_installed_packages():
    log("[+] Checking installed packages (requires pip)...")
    try:
        output = subprocess.check_output(["pip", "list", "--outdated", "--format", "json"], text=True)
        outdated_packages = json.loads(output)
        if outdated_packages:
            log("[!] Outdated packages found:")
            for pkg in outdated_packages:
                log(f"    - {pkg['name']} (Current: {pkg['version']}, Latest: {pkg['latest_version']})")
        else:
            log("[+] All packages are up to date.")
        return outdated_packages
    except Exception as e:
        log(f"[!] Could not check packages: {e}")
        return []

def check_default_credentials(host):
    log(f"[+] Checking for default credentials on {host} (dummy check)...")
    default_users = ['admin', 'root', 'user']
    for user in default_users:
        log(f"[*] Try logging in with username: {user} (This is a placeholder. Implement real tests here.)")

# === GUI Logic === #
def log(message):
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)

def run_assessment_gui():
    target = target_entry.get().strip()
    if not target:
        log("[!] Please enter a valid target hostname or IP.")
        return

    log("\n=== Starting Vulnerability Assessment ===\n")
    check_os_version()
    open_ports = scan_ports(target)
    check_installed_packages()
    check_default_credentials(target)
    log("\n=== Assessment Completed ===")
    log(f"Open Ports: {open_ports}")

def run_in_thread():
    thread = threading.Thread(target=run_assessment_gui)
    thread.start()


# === GUI Setup === #
window = tk.Tk()
window.title("Vulnerability Assessment Tool")
window.geometry("700x500")
window.resizable(False, False)

frame = tk.Frame(window)
frame.pack(pady=10)

tk.Label(frame, text="Enter Target IP or Hostname:").grid(row=0, column=0, padx=5)
target_entry = tk.Entry(frame, width=40)
target_entry.grid(row=0, column=1, padx=5)

start_button = tk.Button(frame, text="Run Assessment", command=run_in_thread)
start_button.grid(row=0, column=2, padx=5)

output_text = scrolledtext.ScrolledText(window, width=90, height=25, bg="black", fg="lightgreen")
output_text.pack(padx=10, pady=10)

window.mainloop()
