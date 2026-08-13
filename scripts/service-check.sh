#!/bin/bash

SERVICE=sshd

{
if
	systemctl is-active "$SERVICE"
then
	echo "running"
else
	echo "not running"
fi
} 

