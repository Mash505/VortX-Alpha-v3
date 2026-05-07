import os
import time
import subprocess

# Configuration: Add ports you want to block/monitor
BANNED_PORTS = ["4444", "5555", "8888"]
WHITELIST_IPS = ["127.0.0.1"]

def notify(message):
    """Sends an Android notification via Termux-API."""
    os.system(f"termux-notification -t 'Firewall Action' -c '{message}'")

def kill_process(pid, name):
    """Terminates the suspicious process."""
    try:
        os.system(f"kill -9 {pid}")
        print(f"[SUCCESS] Terminated {name} (PID: {pid})")
        notify(f"Terminated unauthorized process: {name}")
    except Exception as e:
        print(f"[ERROR] Could not kill process {pid}: {e}")

def check_connections():
    print("[*] Scanning network stack...")
    # Get active TCP/UDP connections with PID and Command info
    try:
        output = subprocess.check_output(["lsof", "-i", "-n", "-P"]).decode()
        lines = output.split('\n')
        
        for line in lines[1:]: # Skip header
            if not line.strip():
                continue
                
            parts = line.split()
            # lsof output format: COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
            if len(parts) < 9:
                continue

            prog_name = parts[0]
            pid = parts[1]
            connection_info = parts[8] # e.g., 192.168.1.5:4444

            for port in BANNED_PORTS:
                if f":{port}" in connection_info:
                    print(f"[!] ALERT: Banned port {port} detected!")
                    print(f"[!] Process: {prog_name} | PID: {pid}")
                    
                    # Mitigation
                    kill_process(pid, prog_name)
                    
    except Exception as e:
        print(f"[!] Error running lsof: {e}")

if __name__ == "__main__":
    print("--- Termux Active Defense Watchdog Started ---")
    notify("Firewall Watchdog is now active.")
    try:
        while True:
            check_connections()
            time.sleep(5) # Scan every 5 seconds
    except KeyboardInterrupt:
        print("\n[!] Watchdog stopped by user.")

