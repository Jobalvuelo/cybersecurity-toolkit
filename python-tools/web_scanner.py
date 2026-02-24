import socket
import requests
from datetime import datetime

def scan_headers(url):
    print("\n[+] Scanning security headers...")
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        
        security_headers = {
            "X-Frame-Options": "Protects against clickjacking",
            "X-Content-Type-Options": "Prevents MIME type sniffing",
            "Strict-Transport-Security": "Forces HTTPS connections",
            "Content-Security-Policy": "Controls resource loading",
            "X-XSS-Protection": "Blocks XSS attacks",
            "Referrer-Policy": "Controls referrer information"
        }
        
        for header, description in security_headers.items():
            if header.lower() in [h.lower() for h in headers]:
                print(f"  [OK] {header} - Present")
            else:
                print(f"  [FAIL] {header} - MISSING ({description})")
                
        print(f"\n  [INFO] Server: {headers.get('Server', 'Hidden')}")
        print(f" [INFO] Powered by: {headers.get('X-Powered-By', 'Hidden')}")
        
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] {e}")

def scan_ports(ip):
    print("\n[+] Scanning common ports...")
    common_ports = {
        21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS",
        3306: "MySQL", 8080: "HTTP Proxy", 8443: "HTTPS Alt"    
    }
    
    for port, service in common_ports.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                print(f"  [OPEN] Port {port} - {service}]")
            else:
                print(f" [CLOSED] Port {port} - {service}")
        except socket.error:
            print(f"  [ERROR] Port {port}")
            
def scan_directories(url):
    print("\n[+] Scanning common directories...")
    dirs = [
        "admin", "login", "wp-admin", "wp-login.php",
        "administrator", "phpmyadmin", "backup", "backups",
        "config", "dashboard", "db", "debug",
        "robots.txt", "sitemap.xml", ".env", "server-status",
        "wp-content", "wp-includes", "uploads", "images"
    ]
    
    for d in dirs:
        try:
            r = requests.get(f"{url}/{d}", timeout=3)
            if r.status_code == 200:
                print(f" [FOUND] {url}/{d} (200 OK)")
            elif r.status_code == 301 or r.status_code == 302:
                print(f" [REDIRECT] {url}/{d} ({r.status_code})")
            elif r.status_code == 403:
                print(f" [FORBIDDEN] {url}/{d} (403 - Exists but blocked)")
        except requests.exceptions.RequestException:
            pass

def main():
    print("=" * 50)
    print(" WEB VULNERABILITY SCANNER v1.0")
    print(" by Ayoub")
    print("=" * 50)
    
    url = input("\nEnter target URL (https://example.com): ")
    
    if not url.startswith("http"):
        url = "https://" + url
        
    print(f"\n[*] Target: {url}")
    print(f"[*] Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    scan_headers(url)
    
    ip = input("\nEnter target IP for port scan (or press Enter to skip): ")
    if ip:
        scan_ports(ip)
    
    scan_directories(url)
    
    print(f"\n[*] Scan complete at: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()