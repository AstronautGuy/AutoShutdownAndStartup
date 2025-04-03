import subprocess
import sys
import psutil
import win32evtlog
import time
import os
from datetime import datetime, timedelta

# Function to install missing modules (if needed)
def install_if_missing(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Ensure required modules are installed
install_if_missing(["pywin32", "psutil"])

# Function to start the server in the morning
def start_server_morning():
    wake_time = datetime.strptime("07:00:00", "%H:%M:%S").time()
    now = datetime.now().time()

    while now < wake_time:
        print(f"Waiting for {wake_time} to start the server...")
        time.sleep(60)  # Check every minute
        now = datetime.now().time()

    print("It's 8 AM. Server is now running.")

# Function to check the last login time
def get_last_login_time():
    server = 'localhost'
    log_type = 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    h = win32evtlog.OpenEventLog(server, log_type)

    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        for event in events:
            if event.EventID in [4624, 4648]:  # 4624 = Successful login, 4648 = Explicit credential logon
                return datetime.now()  # Return the latest login time

# Function to check inactivity and shut down
def check_inactivity():
    last_login = datetime.now()  # Assume login happened at script start

    while True:
        now = datetime.now()

        if now.hour >= 23 and now.minute >= 30:  # After 11:30 PM
            print("Checking for user activity...")
            new_login = get_last_login_time()  # Get latest login time

            if new_login and new_login > last_login:
                last_login = new_login  # Update last login time
                print(f"User logged in at {last_login}. Timer reset.")

            # If no login happened in the past 30 minutes
            if (now - last_login) > timedelta(minutes=30):
                print(f"No login for 30 mins after 11:30 PM. Shutting down at {now}.")
                os.system("shutdown /s /t 0")
                return

        time.sleep(600)  # Check every 10 minutes to save resources

# Run the script
if __name__ == "__main__":
    start_server_morning()  # Start server at 8 AM
    check_inactivity()  # Start monitoring inactivity after 11:30 PM
