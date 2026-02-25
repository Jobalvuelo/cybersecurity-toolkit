#!/bin/bash
echo "===== NETWORK COMPARE TOOL ====="
echo""

SCAN_DIR=~/cybersecurity/scans

echo "[+] Available scans:"
ls $SCAN_DIR
echo ""

echo "[+] Running new scan..."
nmap -sn 192.168.1.0/24 -oN $SCAN_DIR/latest_scan.txt > /dev/null

echo "[+] Devices in first scan:"
grep "Nmap scan report" $SCAN_DIR/first_scan.txt
echo""

echo "[+] Differences:"
diff <(grep "Nmap scan report" $SCAN_DIR/first_scan.txt) <(grep "Nmap scan report" $SCAN_DIR/latest_scan.txt)

if [ $? -eq 0 ]; then
    echo "No changes detected. Network is the same."
else
    echo "WARNING: Network changes detected!"
fi

echo""
echo "===== COMPARE COMPLETE ====="
