#!/bin/bash
REPORT=~/linux-lab/logs/system-report.txt
ARCHIVE_DIR=~/linux-lab/archive
{
	echo "System Report"
echo "Generated:"
date

echo "User:"
whoami
echo "Hostname:"
hostnamectl
echo "Kernel:"
uname -r
echo "Disk:"
df -h
echo "Memory:"
free -h

} > "$REPORT"
mkdir -p "$ARCHIVE_DIR"
tar -czf "ARCHIVE_DIR/configs-backup.tar.gz" ~/linux-lab/configs
