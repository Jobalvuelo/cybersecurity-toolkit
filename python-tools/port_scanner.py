import socket
from datetime import datetime

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except socket.error:
        return False

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP Proxy",
    8443: "HTTPS Alt"
}

def main():
    print("=" * 50)
    print("   PORT SCANNER v1.0 - by Jobalvuelo")
    print("=" * 50)
    
    target = input("\nEnter target IP: ")
    
    try:
        socket.inet_aton(target)
    except socket.error:
        print("[ERROR] Invalid IP address.")
        return
    
    print(f"\nScanning {target}...")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 40)
    
    start_time = datetime.now()
    opens_port = []
    
    for port, service in COMMON_PORTS.items():
        if scan_port(target, port):
            print(f"  [OPEN] Port {port} - {service}")
            opens_port.append((port, service))
            
    end_time = datetime.now()
    duration = end_time - start_time
        
    print("-" * 40)
    print(f"Scan complete. {len(opens_port)} open ports found.")
    print(f"Duration: {duration}")
        
if __name__ == "__main__":
    main()