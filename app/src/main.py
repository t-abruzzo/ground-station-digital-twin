#!/usr/bin/env python3

config = {}

with open("app/config/settings.conf", "r") as file:
    for line in file:
        line = line.strip()

        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            config[key] = value

print(f"Application: {config['APP_NAME']}")
print(f"Environment: {config['ENVIRONMENT']}")
print(f"Log Level: {config['LOG_LEVEL']}")
print("Ground Station Simulator starting...")

