#!/bin/bash
CHECK_STATUS=0

#System Health Check

#Get Current User
CURRENT_USER=$(whoami)

#Get hostname
HOSTNAME=$(hostname)

#Get Current Uptime
UPTIME=$(uptime)

#Get disk usage
DISK_USAGE1=$(df -h)
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

#Get memory usage
MEMORY_USAGE1=$(free -h)
MEMORY_USAGE=$(free | awk '/Mem:/ {printf "%.0f", ($3/$2)*100}')

#Display system infromation
echo "================================="
echo "====== SYSTEM HEALTH CHECK ======"
echo "================================="
echo "================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "User: $CURRENT_USER"
echo "Hostname: $HOSTNAME"
echo "Uptime: $UPTIME"
echo "================================="
echo "================================="
echo "Disk Usage Check:"
if [ "$DISK_USAGE" -ge 80 ]; then
	echo "WARNING: Root filesystem is ${DISK_USAGE}% full"
	CHECK_STATUS=1
else
	echo "OK: Root filesystem is ${DISK_USAGE}% full"
fi
echo "Memory Usage Check:"
if [ "$MEMORY_USAGE" -ge 80 ]; then
	echo "WARNING: Memory usage is ${MEMORY_USAGE}%"
	CHECK_STATUS=1
else
	echo "OK: Memory usage is ${MEMORY_USAGE}%"
fi
echo "================================="
if [ "$CHECK_STATUS" -eq 0 ]; then
	echo "OVERALL STATUS: HEALTHY"
else
	echo "OVERALL STATUS: WARNING"
fi
echo "================================="
exit $CHECK_STATUS
echo "======CHECK COMPLETE======"
