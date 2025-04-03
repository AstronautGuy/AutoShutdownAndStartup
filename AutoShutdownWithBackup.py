import subprocess
import sys
import psutil
import win32evtlog
import time
import os
from datetime import datetime
import requests

# Install missing modules
def install_if_missing(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_if_missing(["psutil", "pywin32", "requests"])

# Configuration
TERACOPY_PATH = "C:\\Program Files\\TeraCopy\\TeraCopy.exe"
SOURCE_FOLDER = "C:\\Users\\YourUsername\\Documents\\ImportantData"  # Change this
DESTINATION_FOLDER = "\\\\BackupServer\\Backups\\ImportantData"  # Change this
NOTIFY_SERVICE = "telegram"  # Options: 'telegram', 'pushover'
TELEGRAM_BOT_TOKEN = "your-bot-token"
TELEGRAM_CHAT_ID = "your-chat-id"

# Function to send notifications
def send_notification(message):
    if NOTIFY_SERVICE == "telegram":
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        })
    elif NOTIFY_SERVICE == "pushover":
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": "your-pushover-app-token",
            "user": "your-pushover-user-key",
            "message": message
        })

def check_login_attempts():
    server = 'localhost'
    log_type = 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    h = win32evtlog.OpenEventLog(server, log_type)
    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        for event in events:
            if event.EventID in [4624, 4648]:  # 4624 = Successful login, 4648 = Explicit credential logon
                print("User logged in! Server is awake.")
                return  # Exit the function if login detected
        time.sleep(10)  # Check every 10 seconds

def run_backup():
    print("Starting backup...")
    backup_command = f'"{TERACOPY_PATH}" copy "{SOURCE_FOLDER}" "{DESTINATION_FOLDER}" /overwrite /silent'
    result = subprocess.run(backup_command, shell=True)
    return result.returncode == 0

def check_inactivity():
    last_login_time = datetime.now()
    while True:
        now = datetime.now()
        if now.hour >= 23 and (now - last_login_time).seconds >= 1800:  # 30 min inactivity
            print("System inactive for 30 mins after 11:30 PM. Running backup...")
            if run_backup():
                send_notification("Backup successful. Shutting down...")
                os.system("shutdown /s /t 0")
            else:
                send_notification("Backup failed! System will stay on.")
        time.sleep(600)  # Check every 10 minutes

if __name__ == "__main__":
    check_login_attempts()  # Wake-up detection
    check_inactivity()  # Shutdown after inactivity
