#!/usr/bin/env python3

import subprocess

def check_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", "sshd"],
        capture_output=True,
        text=True
    )

    return result.stdout.strip() == "active"

def load_config():
    config = {}

    with open("app/config/settings.conf", "r") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key] = value

    return config

config = load_config()

def show_status(online):
    if online:    
        print("GROUND STATION STATUS: ONLINE")
    else:
        print("GROUND STATION STATUS: OFFLINE")


def display_config(config):
    print(f"Application: {config['APP_NAME']}")
    print(f"Environment: {config['ENVIRONMENT']}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Ground Station Simulator starting...")

config = load_config()
display_config(config)
online = check_service("sshd")
show_status(online)

