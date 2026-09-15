#!/usr/bin/env python3

# Imports:
# subprocess = allows Python to interact with Linux commands
# random = generates simulated telemetry values
import subprocess
import random

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
        "safe_mode": False,
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
        },
        "command_history":[],
        "command_queue":[],
        "contact_command_start": 0,
    },
    {
        "satellite": "SAT-002",
        "altitude": 700,
        "connected": False,
        "contact_active": False,
        "safe_mode": False,
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
        },
        "command_history":[],
        "command_queue":[],
        "contact_command_start": 0,
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
    print(f"Safe Mode: {satellite['safe_mode']}")
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

#validate_contact_requirements()
# Checks whether a satellite meets all requirements needed to establish contact.
# Returns True when all requirements pass and False when any requirement fails.
def validate_contact_requirements(satellite):
    signal_strength = satellite["telemetry"]["signal_strength"]
    minimum_signal = satellite["contact_requirements"]["min_signal_strength"]

    if signal_strength < minimum_signal:
        print(f"Contact requirements not met for {satellite['satellite']}.")
        print(f"Signal strength: {signal_strength} dBm")
        print(f"Minimum required: {minimum_signal} dBm")
        return False
 
    battery = satellite["telemetry"]["battery"]
    minimum_battery = satellite["contact_requirements"]["min_battery"]
 
    if battery < minimum_battery:
        print(f"Contact requirements not met for {satellite['satellite']}.")
        print(f"Battery: {battery}%")
        print(f"Minimum required: {minimum_battery}%")
        return False
 
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

#initiate_contact
# Attempts to establish communication with a selected satellite.
# Contact can only begin if the satellite is connected and all requirements pass.
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
    satellite["contact_command_start"] = len(satellite["command_history"])

    print(f"Contact initiated with {satellite['satellite']}.")

#terminate_contact
# Ends an active communication contact with the selected satellite.
def terminate_contact(satellite):
    if satellite is None:
        print("Satellite not found.")
        return

    if not satellite["contact_active"]:
        print(f"No active contact with {satellite['satellite']}.")
        return
    
    satellite["contact_active"] = False
    print(f"Contact terminated with {satellite['satellite']}.")

#show_contact_status
# Displays whether the selected satellite currently has an active contact.
def show_contact_status(satellite):
    if satellite is None:
        print("Satellite not found.")
        return

    if satellite["contact_active"]:
        print(f"Contact ACTIVE with {satellite['satellite']}.")
    else:
        print(f"No active contact with {satellite['satellite']}.")

#available_commands
# Defines the commands that the ground station is allowed to send.
available_commands = [
    "RESET",
    "TRANSMIT_STATUS",
    "SAFE_MODE",
    "TEST"
]

#validate_command:
# Checks whether a command is supported by the ground station.
# Returns True when the command is valid and False when it is invalid.
def validate_command(command):
    if command not in available_commands:
        print(f"INVALID COMMAND: {command}")
        print("AVAILABLE COMMANDS:")
        for available_command in available_commands:
            print(f"- {available_command}")
        return False

    return True

#execute_command:
# Executes a valid command and changes simulated satellite state.
def execute_command(satellite, command):
    if command == "RESET":
        satellite["telemetry"]["temperature"] = 20.0
        satellite["telemetry"]["battery"] = 100
        print(f"{satellite['satellite']} reset completed.")
        return True

    elif command == "TRANSMIT_STATUS":
        show_telemetry(satellite)
        return True

    elif command == "SAFE_MODE":
        satellite["safe_mode"] = True
        satellite["telemetry"]["temperature"] = 20.0
        print(f"{satellite['satellite']} entered SAFE MODE.")
        return True

    return False

#acknowledge_command:
# Simulates a satellite acknowledging receipt of a valid command.
def acknowledge_command(satellite, command):
    receipt = {
        "satellite": satellite["satellite"],
        "command": command,
        "status": "RECEIVED"
    }

    print(f"{satellite['satellite']} acknowledged command: {command}")

    return receipt

#send_command:
# Sends a command to a satellite during an active contact.
# Stores the command in the satellites command history.
def send_command(satellite, command):
    if satellite is None:
        print("satellite not found.")
        return

    if not satellite["contact_active"]:
        print(f"No active contact with {satellite['satellite']}.")
        print("command cannot be sent.")
        return
    
    if not validate_command(command):
        return

    if satellite["safe_mode"] and command != "TRANSMIT_STATUS":
        print(f"{satellite['satellite']} is in SAFE MODE.")
        print(f"Command rejected: {command}")
        return

    command_record = {
        "command": command
    }    
    
    print(f"Command sent to {satellite['satellite']}: {command}")

    receipt = acknowledge_command(satellite, command)

    if receipt and receipt["status"] == "RECEIVED":
        command_record["receipt"] = "RECEIVED"
        print(f"Command receipt verified: {receipt['command']}")
    else:
        command_record["receipt"] = "NOT_RECEIVED"
        print(f"Command receipt NOT verified: {command}")

    execution_success = execute_command(satellite, command)

    if execution_success:
        command_record["execution"] = "SUCCESS"
        print(f"Command execution successful: {command}")
    else:
        command_record["execution"] = "FAILED"
        print(f"Command execution failed: {command}")
    
    satellite["command_history"].append(command_record)

#schedule_command:
# Adds a valid command to the satellite's command queue.
def schedule_command(satellite, command):
    if satellite is None:
        print("Satellite not found.")
        return

    if not validate_command(command):
        return
    
    command_record = {
        "command": command,
        "status": "QUEUED",
        "result": None
    }

    satellite["command_queue"].append(command_record)

    print(f"Command scheduled for {satellite['satellite']}: {command}")

#show_command_queue
# Displays commands currently waiting in the satellite's command queue.
def show_command_queue(satellite):
    if satellite is None:
        print("Satellite not found.")
        return
    
    print(f"\nCommand Queue for {satellite['satellite']}:")

    if not satellite["command_queue"]:
        print("No commands are currently queued.")
        return

    for command_record in satellite["command_queue"]:
        print(f"- Command: {command_record['command']}")
        print(f"  Status: {command_record['status']}")
        print(f"  Result: {command_record['result']}")

    print()

#process_command_queue:
# Sends all queued commands to the satellite during an active contact.
def process_command_queue(satellite):
    if satellite is None:
        print("Satellite not found")
        return

    if not satellite["contact_active"]:
        print("No active contact with {satellite['satellite']}.")
        print("command queue cannot be processed.")
        return

    if not satellite["command_queue"]:
        print("No commands are currently queued.")
        return

    print(f"\nProcessing command queue for {satellite['satellite']}...")
    
    while satellite["command_queue"]:
        command_record = satellite["command_queue"].pop(0)
        command = command_record["command"]

        command_record["status"] = "PROCESSING"
        print(f"\nProcessing queued command: {command}")

        send_command(satellite, command)

        command_record["status"] = "COMPLETED"
        command_record["result"] = "SUCCESS"

    satellite["command_queue"] = []
    
    print("\nCommand queue processing complete.")

#show_command_history
# Displays the commands that have been sent to the selected satellite.
def show_command_history(satellite):
    if satellite is None:
        print("Satellite not found.")
        return

    print(f"\nCommand History for {satellite['satellite']}:")

    if not satellite["command_history"]:
        print("No commands have been sent.")
        return

    current_contact_commands = satellite["command_history"][
        satellite["contact_command_start"]:
    ]
    
    for command_record in current_contact_commands:
        print(f"- Command: {command_record['command']}")
        print(f"  Receipt: {command_record['receipt']}")
        print(f"  Execution: {command_record['execution']}")

    print(f"Command Count: {len(satellite['command_history'])}")
    print()


#show_menu
# Displays the available ground station operations for the operator.
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
    print("8. Send Command")
    print("9. Show Command History")
    print("10. Schedule Command")
    print("11. Show Command Queue")
    print("12. Process Command Queue")
    print("13. Exit")
    print("===============================")

#Main application flow:
# Select a satellite and continuously simulate telemetry updates for a limited number of readings.
config = load_config()
display_config(config)

online = check_service("sshd")
show_status(online)

selected_satellite = None

while True:
    show_menu()

    choice = input("Select an option: ")
    
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
        command = input("Enter command: ")
        send_command(selected_satellite, command)

    elif choice == "9":
        show_command_history(selected_satellite)

    elif choice == "10":
        command = input("Enter command to schedule: ")
        schedule_command(selected_satellite, command)

    elif choice == "11":
        show_command_queue(selected_satellite)

    elif choice == "12":
        process_command_queue(selected_satellite)

    elif choice == "13":
        print("Ground Station Simulator shutting down.")
        break
    
    else:
        print("Invalid option. Please select 1-13.")

