#!/bin/bash
echo "===== SECURITY CHECK REPORT ====="
echo "[+] Date: $(date)"
echo ""

echo "[+] Users with login shell:"
grep -v "nologin\|false" /etc/passwd | cut -d: -f1
echo ""

echo "[+] Users in sudo group:"
grep "sudo" /etc/group
echo ""

echo "[+] Active services:"
systemctl list-units --type=service --state=running --no-pager | grep ".service"
echo ""

echo "[+] Open ports:"
ss -tulnp
echo ""

echo "[+] Recent sudo usage:"
journalctl | grep "sudo" | tail -5
echo""

echo "[+] Failed login attempts:"
journal | grep -i "Failed" | tail -5
echo ""

echo "===== CHECK COMPLETE ====="
