#!/usr/bin/env python3

# Imports:
# subprocess = allows Python to interact with Linux commands
# random = generates simulated telemetry values
# time = controls the delay between telemetry updates
import subprocess
import random
import time

#check_service:
# Checks whether a Linux service is currently active.
# Returns True if active False if inactive
def check_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True
    )

    return result.stdout.strip() == "active"

#load_config:
# Reads the application configuration file and stores the settings in Python dictionary.
def load_config():
    config = {}

    with open("app/config/settings.conf", "r") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key] = value

    return config

#show_status:
# Converts the service check result into human-readable ground station status message.
def show_status(online):
    if online:    
        print("GROUND STATION STATUS: ONLINE")
    else:
        print("GROUND STATION STATUS: OFFLINE")

#display_config():
# Displays the loaded application configuration so the operator can verify the current settings.
def display_config(config):
    print(f"Application: {config['APP_NAME']}")
    print(f"Environment: {config['ENVIRONMENT']}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Ground Station Simulator starting...")

#Satellite data:
# Stores the current state of each satellite.
# Each satellite is represented as a dictionary containing id, altitude, connection status, contact state, & TLM.
satellites = [
    {
        "satellite": "SAT-001",
        "altitude": 600,
        "connected": True,
        "contact_active": False,
        "contact_requirements": {
            "min_signal_strength": -80,
            "min_battery": 20,
            "min_altitude": 500,
            "max_altitude": 800
        },
        "telemetry": {
            "temperature": 22.5,
            "battery": 80,
            "signal_strength": -72
        }
    },
    {
        "satellite": "SAT-002",
        "altitude": 700,
        "connected": False,
        "contact_active": False,
        "contact_requirements": {
            "min_signal_strength": -89,
            "min_battery": 20,
            "min_altitude": 500,
            "max_altitude": 800
         },
        "telemetry": {
            "temperature": 19.8,
            "battery": 64,
            "signal_strength": -85
        }
     }
]
 
#display_satellites:
# Displays the available satellites in the simulator.
def display_satellites(satellites):
    for satellite in satellites:
        print()
        print(f"Satellite: {satellite['satellite']}")
        print(f"Altitude: {satellite['altitude']}km") 
        print(f"Connected: {satellite['connected']}")
        print()

#find_satellite:
# Searches the satellite list for a specific satellite name.
# Returns the matching satellite dictionary or None if not found.
def find_satellite(satellites, satellite_name):
    for satellite in satellites:
        if satellite["satellite"] == satellite_name:
            return satellite
    
    return None

#show_satellite_details:
# Displays the details of one selected satellite.
def show_satellite_details(satellite):
    if satellite is None:
        print("Satellite not found.")
        return
    print()
    print(f"Satellite: {satellite['satellite']}")
    print(f"Altitude: {satellite['altitude']}km")
    print(f"Connected: {satellite['connected']}")
    print()

#show_telemetry:
# Displays the current telemetry values for a selected satellite.
def show_telemetry(satellite):

    if satellite is None:
        print("Satellite not found")
        return

    telemetry = satellite["telemetry"]

    if satellite["contact_active"]:
        print(f"\nLIVE TELEMETRY for {satellite['satellite']}:")
    else:
        print(f"\nLAST KNOWN TELEMETRY for {satellite['satellite']}:")

    print()
    print(f"Telemetry for {satellite['satellite']}:")
    print(f"Temperature: {telemetry['temperature']} C")
    print(f"Battery: {telemetry['battery']}%")
    print(f"Signal Strength: {telemetry['signal_strength']} dbm")
    print()

#simulate_telemetry
# Generates random telemetry values within defined ranges to simulate changing satellite conditions.
def simulate_telemetry(satellite):
    if satellite is None:
        print("Satellite not found.")
        return
        
    satellite["telemetry"]["temperature"] = round(
        random.uniform(15.0, 30.0), 1
    )

    satellite["telemetry"]["battery"] = random.randint(50, 100)

    satellite["telemetry"]["signal_strength"] = random.randint(-90, -60)

def validate_contact_requirements(satellite):
    signal_strength = satellite["telemetry"]["signal_strength"]
    minimum_signal = satellite["contact_requirements"]["min_signal_strength"]

    if signal_strength < minimum_signal:
        print(f"Contact requirements not met for {satellite['satellite']}.")
        print(f"Signal strength: {signal_strength} dBm")
        print(f"Minimum required: {minimum_signal} dBm")
        return
 
    battery = satellite["telemetry"]["battery"]
    minimum_battery = satellite["contact_requirements"]["min_battery"]
 
    if battery < minimum_battery:
        print(f"Contact requirements not met for {satellite['satellite']}.")
        print(f"Battery: {battery}%")
        print(f"Minimum required: {minimum_battery}%")
        return
 
    altitude = satellite["altitude"]
    minimum_altitude = satellite["contact_requirements"]["min_altitude"]
    maximum_altitude = satellite["contact_requirements"]["max_altitude"]
 
    if altitude < minimum_altitude or altitude > maximum_altitude:
        print(f"Contact requirements not met for {satellite['satellite']}.")
        print(f"Altitude: {altitude} km")
        print(
            f"Required altitude: "
            f"{minimum_altitude}-{maximum_altitude} km"
        )
        return False
    return True

def initiate_contact(satellite):
    if satellite is None:
        print("Satellite not found.")
        return
 
    if not satellite["connected"]:
        print(f"{satellite['satellite']} is not connected.")
        return
 
    if satellite["contact_active"]:
        print(f"Contact already active with {satellite['satellite']}.")
        return
    
    if not validate_contact_requirements(satellite):
        return

    satellite["contact_active"] = True
    print(f"Contact initiated with {satellite['satellite']}.")

def terminate_contact(satellite):
    if satellite is None:
        print("Satellite not found.")
        return

    if not satellite["contact_active"]:
        print(f"No active contact with {satellite['satellite']}.")
        return
    
    satellite["contact_active"] = False
    print(f"Contact terminated with {satellite['satellite']}.")

def show_contact_status(satellite):
    if satellite is None:
        print("Satellite not found.")
        return

    if satellite["contact_active"]:
        print(f"Contact ACTIVE with {satellite['satellite']}.")
    else:
        print(f"No active contact with {satellite['satellite']}.")

def show_menu():
    print()
    print("===== GROUND STATION MENU =====")
    print("1. List Satellites")
    print("2. Select Satellite")
    print("3. Show Telemetry")
    print("4. Update Telemetry")
    print("5. Initiate Contact")
    print("6. Terminate Contact")
    print("7. Show Contact Status")
    print("8. Exit")
    print("===============================")

#Main application flow:
# Select a satellite and continuously simulate telemetry updates for a limited number of readings.
config = load_config()
display_config(config)

selected_satellite = None
while True:
    show_menu()

    choice = input("Select an opion: ")
    
    if choice == "1":
        display_satellites(satellites)

    elif choice == "2":
        satellite_name = input("Enter satellite ID: ")
        selected_satellite = find_satellite(satellites, satellite_name)    
        if selected_satellite is None:
            print("Satellite not found.")
        else:
            print(f"{satellite_name} selected.")

    elif choice == "3":
        show_telemetry(selected_satellite)

    elif choice == "4":
        if selected_satellite is None:
            print("No satellite selected")
        elif not selected_satellite["contact_active"]:
            print(f"No active contact with {selected_satellite['satellite']}.")
            print("Telemetry cannot be updated")
        else:
            simulate_telemetry(selected_satellite)
            show_telemetry(selected_satellite)

    elif choice == "5":
        initiate_contact(selected_satellite)

    elif choice == "6":
        terminate_contact(selected_satellite)
  
    elif choice == "7":
        show_contact_status(selected_satellite)

    elif choice == "8":
        print("Ground Station Simulator shutting down.")
        break
    
    else:
        print("Invalid option. Please select 1-8.")

online = check_service("sshd")
show_status(online)

# Select satellite and simulate telemetry.
selected_satellite = find_satellite(satellites, "SAT-001")

for i in range(2):
    simulate_telemetry(selected_satellite)
    show_telemetry(selected_satellite)
    time.sleep(1)

# Test satellite contact lifecycle.
show_contact_status(selected_satellite)
initiate_contact(selected_satellite)
show_contact_status(selected_satellite)
terminate_contact(selected_satellite)
show_contact_status(selected_satellite)
