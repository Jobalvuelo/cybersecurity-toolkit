# Python Security Tools

Custom security tools built from scratch during cybersecurity training.

## port_scanner.py

TCP port scanner using socket connections to identify open ports.

**How it works:** Creates a TCP socket to each port. If connect_ex() returns 0, the port is open.

**What I learned:** TCP handshake, socket programming, comparing results with Nmap.

---

## web_scanner.py

Combines Nikto + Nmap + Gobuster in one script.

1. Checks 6 HTTP security headers
2. Scans 7 common ports
3. Probes 20 hidden directories

Tested against live WordPress site — found 4 open ports, 5 missing headers, 9 directories.

---

## hash_cracker.py

MD5/SHA256 hash cracker with dictionary attacks using wordlists.

Cracked 5 DVWA password hashes using rockyou.txt (14M passwords) in under 1 second.

---

## network_monitor.py

Real-time network monitoring. Runs Nmap at intervals, compares scans with Python set operations, alerts on changes.

Requires Nmap and sudo. Successfully detected devices connecting/disconnecting from hostel network during real audit.

---

## ir_toolkit.py

Incident Response toolkit combining all tools:

1. Network discovery
2. Port scanning (15 ports)
3. Security header analysis
4. Suspicious file detection
5. JSON report generation with risk level

Tested against live network + web server. Generated professional report.