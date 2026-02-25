#!/bin/bash
echo "===== FIREWALL SETUP ====="
echo ""

echo "[+] Current rules:"
iptables -L --line-numbers
echo ""

echo "[+] Setting up basic firewall..."

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback (localhost)
iptables -A INPUT -i lo -j ACCEPT

# Allow ping
iptables -A INPUT -p icmp -j ACCEPT

# Block everything else incoming
iptables -A INPUT -j DROP

echo "[+] Firewall rules applied:"
iptables -L --line-numbers
echo ""
echo "===== FIREWALL ACTIVE ====="
echo ""
echo "To disable firewall run: sudo iptables -F"
