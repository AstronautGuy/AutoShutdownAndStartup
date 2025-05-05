import subprocess
import time
import os
from datetime import datetime, timedelta

# Function to wait until 7:00 AM
def wait_until_morning():
    wake_time = datetime.strptime("07:00:00", "%H:%M:%S").time()
    now = datetime.now().time()

    while now < wake_time:
        print(f"[{datetime.now()}] Waiting for 7:00 AM...")
        time.sleep(60)
        now = datetime.now().time()

    print(f"[{datetime.now()}] It's 7:00 AM. Starting monitoring.")

# Function to get last user login time from `who` or `last`
def get_last_login_time():
    try:
        output = subprocess.check_output("last -F -n 1", shell=True).decode()
        lines = output.strip().split("\n")
        for line in lines:
            if "still logged in" in line or "logged in" in line:
                parts = line.split()
                # Example format: user pts/0 192.168.x.x Fri May  3 22:48:21 2025
                date_str = " ".join(parts[-6:])  # Extract full datetime string
                try:
                    return datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                except:
                    continue
    except Exception as e:
        print(f"Error reading login time: {e}")
    return None

# Monitor inactivity after 11:30 PM
def monitor_inactivity():
    last_login = datetime.now()

    while True:
        now = datetime.now()

        if now.hour >= 23 and now.minute >= 30:
            print(f"[{now}] Checking for user activity...")
            new_login = get_last_login_time()

            if new_login and new_login > last_login:
                last_login = new_login
                print(f"User logged in at {last_login}. Timer reset.")

            if (now - last_login) > timedelta(minutes=30):
                print(f"No user activity for 30+ mins after 11:30 PM. Shutting down...")
                os.system("shutdown -h now")
                return

        time.sleep(600)  # Wait 10 minutes before next check

# Run everything
if __name__ == "__main__":
    wait_until_morning()
    monitor_inactivity()
