# **AutoShutdownAndBackup**

## **Overview**

This Python script is designed to manage the power state of a **Windows cloud server** by:
- **Starting up** when a user logs in after **6:00 AM**.
- **Monitoring user logins after 11:30 PM** and shutting down the system **if no logins occur within 30 minutes**.
- **Performing a backup before shutdown** using **TeraCopy**.
- **Checking system activity every 10 minutes** to reduce resource usage.
- **Automatically installing missing dependencies** when first executed.
- **Sending a notification on backup success or failure** before shutdown.

This script ensures that the server is operational during the day, backs up critical data before shutting down at night, and optimizes power consumption.

---
### Features

✅ **Automatic Startup Handling** - The script detects user logins and prevents unnecessary wake-ups before 6:00 AM.

✅ **Intelligent Shutdown Management** - If no logins occur within **30 minutes after 11:30 PM**, the script first performs a backup and then shuts down.

✅ **Automatic Backup Before Shutdown** - Uses **TeraCopy** to copy data to a backup server before shutting down.

✅ **Resource-Efficient Monitoring** - The script checks system activity every **10 minutes** instead of running continuously.

✅ **Automatic Dependency Installation** - If required Python modules are missing, they are installed automatically.

✅ **Phone Notification for Backup Success/Failure** - Uses Telegram or Pushover to send alerts.

---
## Installation

### **Prerequisites**
Ensure you have **Python 3** installed on your Windows server.

### **Clone the Repository**
```sh
git clone https://github.com/AstronautGuy/AutoShutdownAndBackup.git
cd AutoShutdownAndBackup
```

### **Run the Script**
```sh
python AutoShutdownAndBackup.py
```

---
## How It Works

### **Step 1: Login Detection (After 6:00 AM)**
- The script starts listening for login events on the Windows **Security Event Log**.
- If a successful login event (Event ID **4624 or 4648**) is detected after **6:00 AM**, the script ensures the system remains awake.

### **Step 2: Inactivity Monitoring (After 11:30 PM)**
- After **11:30 PM**, the script periodically checks if a user logs in.
- If **no login** is detected for **30 minutes**, the backup process starts.

### **Step 3: Backup Process**
- The script runs **TeraCopy** to copy the specified folders to the backup server.
- If the backup is **successful**, a success notification is sent, and the system shuts down.
- If the backup **fails**, a failure notification is sent, and the system remains ON for troubleshooting.

### **Step 4: Shutdown Process**
- If the backup succeeds, the system shuts down using:
  ```sh
  shutdown /s /t 0
  ```

---
## Configuration
Modify `AutoShutdownAndBackup.py` to adjust settings like:
- **Startup time** (default: `6:00 AM`)
- **Shutdown monitoring start time** (default: `11:30 PM`)
- **Idle time before shutdown** (default: `30 minutes`)
- **Check interval** (default: `10 minutes`)
- **Source folder** for backup
- **Destination folder** (backup server path)
- **Notification service** (`telegram` or `pushover`)

---
## Dependencies
The script requires:
- `pywin32`
- `psutil`
- `requests`

If these modules are missing, the script will **automatically install** them.

---
## Troubleshooting

### **1. Script Doesn’t Run at Startup**
- Ensure the script is added to Windows **Task Scheduler** to run at boot.
- Use the following command to manually start it:
  ```sh
  python AutoShutdownAndBackup.py
  ```

### **2. Backup Fails**
- Check if **TeraCopy** is installed in `C:\Program Files\TeraCopy\TeraCopy.exe`.
- Ensure the source and destination paths are correctly set.

### **3. Shutdown Not Triggering**
- Ensure the script is running **continuously in the background**.
- Check the Windows **Security Event Logs** for login events.

### **4. Dependencies Not Found**
If you see `ModuleNotFoundError`, try running:
```sh
pip install pywin32 psutil requests
```

---
## License
This project is licensed under the **MIT License**.

---
## Author
**Devansh Rajan**  
GitHub: [AstronautGuy](https://github.com/AstronautGuy)  

Feel free to contribute or report issues!
