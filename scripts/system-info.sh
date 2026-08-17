#!/bin/bash

echo "==== SYSTEM INFORMATION" ====
echo "User: $USER"
echo "Hostname: $(hostname)"
echo "Operating System: $(cat /etc/redhat-release)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Uptime: $(uptime -p)"
echo ""
echo "====ROOT FILESYSTEM===="
df -h /

