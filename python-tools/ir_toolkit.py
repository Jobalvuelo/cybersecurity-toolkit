import subprocess
import hashlib
import os
import json
from datetime import datetime

def banner():
    print("=" * 50)
    print("    INCIDENT RESPONSE TOOLKIT v1.0")
    print("    by Ayoub")
    print("=" * 50)
    print(f"    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def scan_network(network):
    print(f"\n[1/5] NETWORK SCAN - {network}")
    print("-" * 40)
    try:
        result = subprocess.run(
            ["nmap", "-sn", network],
            capture_output=True, text=True, timeout=60
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
                print(f"    [FOUND] {host} ({mac})")
        print(f"    [TOTAL] {len(devices)} devices found")
        return devices
    except Exception as e:
        print(f"    [ERROR] {e}")
        return []

def scan_ports(ip):
    print(f"\n[2/5] PORT SCAN - {ip}")
    print("-" * 40)
    open_ports = []
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 8080: "HTTP Proxy", 8443: "HTTPS Alt"
    }
    import socket
    for port, service in common_ports.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                print(f"    [OPEN] Port {port} - {service}")
                open_ports.append({"port": port, "service": service})
            else:
                print(f"    [CLOSED] Port {port} - {service}")
        except socket.error:
            print(f"    [ERROR] Port {port}")
    print(f"    [TOTAL] {len(open_ports)} open ports")
    return open_ports

def check_security_headers(url):
    print(f"\n[3/5] SECURITY HEADERS - {url}")
    print("-" * 40)
    import requests
    results = []
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        security_headers = {
            "X-Frame-Options": "Clickjacking protection",
            "X-Content-Type-Options": "MIME sniffing protection",
            "Strict-Transport-Security": "Forces HTTPS",
            "Content-Security-Policy": "Controls resource loading",
            "X-XSS-Protection": "XSS atack blocking",
            "Referrer-Policy": "Referrer info control"
        }
        for header, desc in security_headers.items():
            if header.lower() in [h.lower() for h in headers]:
                print(f"    [OK] {header}")
                results.append({"header": header, "status": "present"})
            else:
                print(f"    [FAIL] {header} - MISSING ({desc})")
                results.append({"header": header, "status": "missing", "risk": desc})
        
        server = headers.get("Server", "Hidden")
        powered = headers.get("X-Powered-By", "Hidden")
        print(f"\n [INFO] Server: {server}")
        print(f" [INFO] Powered by: {powered}")
        if server != "Hidden":
            print(f"    [WARN] Server version exposed!")
        if powered != "Hidden":
            print(f"    [WARN] Technology stack exposed!")
    
    except Exception as e:
        print(f"    [ERROR] {e}")
    return results

def check_suspicious_files(directory):
    print(f"\n[4/5] SUSPICIOUS FILE CHECK - {directory}")
    print("-" * 40)
    suspicious_extensions = [
        ".exe", ".bat", ".ps1", ".vbs", ".js",
        ".sh", ".py", ".php"
    ]
    found_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                if ext in suspicious_extensions:
                    size = os.path.getsize(filepath)
                    with open(filepath, "rb") as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        print(f"    [ALERT] {filepath}")
                        print(f"    Size: {size} bytes | MD5: {file_hash}")
                        found_files.append({
                            "file": filepath,
                            "size": size,
                            "md5": file_hash
                        })
        if not found_files:
            print("    [OK] No suspicious files found")
        else:
            print(f"    [TOTAL] {len(found_files)} suspicious files found")
    except Exception as e:
        print(f"   [ERROR] {e}")
    return found_files

def generate_report(network_data, port_data, header_data, file_data):
    print(f"\n[5/5] GENERATING REPORT")
    print("-" * 40)
    
    report = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tool": "IR Toolkit v1.0 by Ayoub",
        "findings": {
            "devices": network_data,
            "open_ports": port_data,
            "security_headers": header_data,
            "suspicious_files": file_data
        },
    
        "summary": {
            "total_devices": len(network_data),
            "total_open_ports": len(port_data),
            "missing_headers": len([h for h in header_data if h.get("status") == "missing"]),
            "suspicious_files": len(file_data)
       }
    }
    filename = f"ir_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"    [SAVED] Report saved to {filename}")
    print(f"\n === SUMMARY ===")
    print(f"  Devices found:     {report['summary']['total_devices']}")
    print(f"  Open ports:        {report['summary']['total_open_ports']}")
    print(f"  Missing headers:   {report['summary']['missing_headers']}")
    print(f"  Suspicious files:  {report['summary']['suspicious_files']}")
    
    risk = report["summary"]["missing_headers"] + report["summary"]["suspicious_files"]
    if risk == 0:
        print(f"\n  [RISK LEVEL] LOW - System looks secure")
    elif risk <= 3:
        print(f"\n  [RISK LEVEL] MEDIUM - Some issues found")
    else:
        print(f"\n  [RISK LEVEL] HIGH - Immediate action needed")
    
    return report

def main():
    banner()
    
    print("\n[*] Starting Incident Response scan...")
    
    network = input("\nEnter netowrk (e.g. 192.168.1.0/24): ")
    target_ip = input("Enter target IP for port scan: ")
    target_url = input("Enetr target URL (e.g. https://example.com): ")
    scan_dir = input("Enter directory to check for suspicious files: ")
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
        
    network_data = scan_network(network)
    port_data = scan_ports(target_ip)
    header_data = check_security_headers(target_url)
    file_data = check_suspicious_files(scan_dir)
    generate_report(network_data, port_data, header_data, file_data)
    
    print(f"\n{'=' * 50}")
    print("    SCAN COMPLETE")
    print(f"{'=' * 50}")
    
if __name__ == "__main__":
    main() 