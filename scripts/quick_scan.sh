#!/bin/bash
echo "===== QUICK NETWORK SCAN ====="
echo "[+] Scanning network..."
echo ""

TARGET="192.168.1.0/24"
DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT=~/cybersecurity/scans/scan_$DATE.txt

echo "[+] Target: $TARGET"
echo "[+] Output: $OUTPUT"

nmap -sn $TARGET -oN $OUTPUT

echo ""
echo "[+] Scan saved to $OUTPUT"
echo "[+] Devices found:"
grep "Nmap scan report" $OUTPUT
echo ""
echo "===== SCAN COMPLETE ====="
