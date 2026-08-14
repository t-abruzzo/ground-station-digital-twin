#!/bin/bash

#System Health Check

#Get Current User
CURRENT_USER=$(whoami)

#Get hostname
HOSTNAME=$(hostname)

#Get disk usage
DISK_USAGE=$(df -h /)

#Get memory usage
MEMORY_USAGE=$(free -h)

#Display system infromation
echo "====== SYSTEM HEALTH CHECK ======"
echo
echo "User: $CURRENT_USER"
echo "Hostname: $HOSTNAME"
echo
echo "Disk Usage:"
echo "$DISK_USAGE"
echo "Memory Usage"
echo "$MEMORY_USAGE"
echo
echo "======CHECK COMPLETE======"
