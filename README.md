# **AutoShutdownAndStartup**

## **Overview**

This Python script is designed to manage the power state of a **Windows cloud server** by:
- **Starting up** when a user logs in after **6:00 AM**.
- **Monitoring user logins after 11:30 PM** and shutting down the system **if no logins occur within 30 minutes**.
- **Checking system activity every 5-10 minutes** to reduce resource usage.
- **Automatically installing missing dependencies** when first executed.

This script ensures that the server is operational during the day and powers off when it's no longer needed, optimizing power consumption.

---
### Features
**Automatic Startup Handling** - The script detects user logins and prevents unnecessary wake-ups before 6:00 AM.

**Intelligent Shutdown Management** - If no logins occur within **30 minutes after 11:30 PM**, the script shuts down the server.

**Resource-Efficient Monitoring** - The script checks system activity every **5-10 minutes** instead of running continuously.

**Automatic Dependency Installation** - If required Python modules are missing, they are installed automatically.

**Easy to Deploy & Run** - Simply execute the script, and it will handle everything on its own.

---
## Installation
### **Prerequisites**
Ensure you have **Python 3** installed on your Windows server.

### **Clone the Repository**
```sh
git clone https://github.com/AstronautGuy/AutoShutdownAndStartup.git
cd AutoShutdownAndStartup
```

### **Run the Script**
```sh
python AutoShutdownAndStartup.py
```

---
## How It Works
### **Step 1: Login Detection (After 6:00 AM)**
- The script starts listening for login events on the Windows **Security Event Log**.
- If a successful login event (Event ID **4624 or 4648**) is detected after **6:00 AM**, the script ensures the system remains awake.

### **Step 2: Inactivity Monitoring (After 11:30 PM)**
- After **11:30 PM**, the script periodically checks if a user logs in.
- If **no login** is detected for **30 minutes**, the system shuts down.
- It checks every **5-10 minutes** to conserve system resources.

### **Step 3: Shutdown Process**
- If the server remains inactive (CPU usage < 1%) for **30 minutes after 11:30 PM**, it triggers a shutdown command.
- Shutdown command:
  ```sh
  shutdown /s /t 0
  ```

---
## Configuration
Modify `main.py` to adjust settings like:
- **Startup time** (default: `6:00 AM`)
- **Shutdown monitoring start time** (default: `11:30 PM`)
- **Idle time before shutdown** (default: `30 minutes`)
- **Check interval** (default: `5-10 minutes`)

---
## Dependencies
The script requires:
- `pywin32`
- `psutil`

If these modules are missing, the script will **automatically install** them.

---
## Troubleshooting
### **1. Script Doesn’t Run at Startup**
- Ensure the script is added to Windows **Task Scheduler** to run at boot.
- Use the following command to manually start it:
  ```sh
  python main.py
  ```

### **2. Shutdown Not Triggering**
- Ensure the script is running **continuously in the background**.
- Check the Windows **Security Event Logs** for login events.
- Adjust the CPU inactivity threshold in the script if needed.

### **3. Dependencies Not Found**
If you see `ModuleNotFoundError`, try running:
```sh
pip install pywin32 psutil
```

---
## License
This project is licensed under the **MIT License**.

---
## Author
**Devansh Rajan**  
GitHub: [AstronautGuy](https://github.com/AstronautGuy)  

Feel free to contribute or report issues!

