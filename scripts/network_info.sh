#!/bin/bash
echo "===== NETWORK INFO REPORT ====="
echo ""
echo "[+] Hostname:"
hostname
echo ""
echo "[+] IP Address:"
ip a | grep "inet " | grep -v "127.0.0.1"
echo ""
echo "[+] Open ports:"
ss -tulnp
echo ""
echo "[+] Date:"
date
echo "===== END OF REPORT ====="
