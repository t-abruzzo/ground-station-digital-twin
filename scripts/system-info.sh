#!/bin/bash


#Hostname
{
	HOSTNAME=funnyguy
	
if	hostnamectl "funnyguy"; then
	echo "its funny guy"
else
	echo "not funny guy"
fi
}
#Current user
{
	ID=STUDENT 

if id "student"; then
	echo "ITS STUDENT"
fi
}
#Current date/time
date
#Kernel version
uname -r
#Disk Usage
df -h
#Memory Usage
free -h
#How long the system has been running
uptime
