import subprocess
import time
import os
from datetime import datetime

def scan_network(network):
    try:
        result = subprocess.run(
            ["nmap", "-sn", network],
            capture_output=True, text=True, timeout=30
        )
        devices = []
        lines = result.stdout.split("\n")
        
        for i, line in enumerate(lines):
            if "Nmap scan report for" in line:
                host = line.replace("Nmap scan report for ", "")
                mac = "Unknown"
                for j in range(i + 1, min(i + 4, len(lines))):
                    if "MAC Address" in lines[j]:
                        mac = lines[j].split("MAC Address: ")[1]
                        break
                devices.append({"host": host, "mac": mac})
                
        return devices
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def compare_devices(old_devices, new_devices):
    old_hosts = set(d["host"] for d in old_devices)
    new_hosts = set(d["host"] for d in new_devices)
    
    added = new_hosts - old_hosts
    removed = old_hosts - new_hosts
    
    return added, removed

def save_log(message):
    with open("network_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        
def main():
    print("=" * 50)
    print("    NETWORK MONITOR v1.0 - by Ayoub")
    print("=" * 50)
    
    network = input("\nEnter network to monitor (e.g. 192.168.1.0/24): ")
    interval = input("Scan interval in seconds (default 60): ")
    
    if not interval:
        interval = 60
    else:
        interval = int(interval)
        
    print(f"\n[*] Monitoring {network} every {interval} seconds")
    print("[*] Press Ctrl+C to stop\n")
    
    print("[*] Running initial scan...")
    known_devices = scan_network(network)
    print(f"[+] Found {len(known_devices)} devices:")
    for d in known_devices:
        print(f"    {d['host']} ({d['mac']})")
        save_log(f"INITIAL: {d['host']} ({d['mac']})")
        
    scan_count = 1
    
    try:
        while True:
            time.sleep(interval)
            scan_count += 1
            print(f"\n[*] Scan #{scan_count} at {datetime.now().strftime('%H:%M:%S')}")
            
            current_devices = scan_network(network)
            added, removed = compare_devices(known_devices, current_devices)
            
            if added:
                for host in added:
                    print(f"    [ALERT] NEW DEVICE: {host}")
                    save_log(f"NEW DEVICE: {host}")
            
            if removed:
                for host in removed:
                    print(f" [ALERT] DEVICE LEFT: {host}")
                    save_log(f"DEVICE LEFT: {host}")
            
            if not added and not removed:
                print(f" [OK] No changes. {len(current_devices)} devices online.")
                
            known_devices = current_devices

    except KeyboardInterrupt:
        print(f"\n\n[*] Monitoring stopped.")
        print(f"[*] Total scans: {scan_count}")
        print(f"[*] Log saved to network_log.txt")
    
if __name__ == "__main__":
    main()
        