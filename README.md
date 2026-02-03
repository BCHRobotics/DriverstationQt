# FRC Driver Station - Simple Edition

A lightweight, cross-platform driver station for FRC robots built with Python.

## Features

✅ **Robot Control**
- Enable/Disable robot
- Mode selection (Teleop, Autonomous, Test)
- Emergency stop button
- NetworkTables communication

✅ **Controller Support**
- PS5 DualSense controller
- Xbox controllers
- Cross-platform joystick support via pygame
- Configurable deadzone

✅ **Telemetry**
- Battery voltage monitoring with color-coded warnings
- RoboRIO CPU usage
- RoboRIO RAM usage
- Connection status

✅ **Configuration**
- Persistent settings (team number, preferences)
- Auto-connect on startup option
- Window position/size remembered

## Requirements

- Python 3.7 or higher
- PS5 or Xbox controller (optional but recommended)
- Robot running WPILib with NetworkTables

## Installation

### Quick Start (Recommended)

**Windows (PowerShell):**
```powershell
.\run_driverstation.ps1
```

**Windows (Command Prompt):**
```cmd
run_driverstation.bat
```

**Linux/macOS:**
```bash
chmod +x run_driverstation.sh
./run_driverstation.sh
```

The launcher scripts will automatically:
1. Create a Python virtual environment
2. Install all dependencies
3. Launch the driver station

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the driver station
python main.py
```

## Usage

### First Launch

1. Launch the driver station using one of the methods above
2. Enter your team number (default: 2026)
3. Click "Connect" to connect to your robot
4. Plug in a PS5 or Xbox controller
5. Select the desired mode (Teleop, Autonomous, Test)
6. Click "ENABLE" to enable the robot

### Controls

**Connection:**
- Team Number: Set your FRC team number
- Connect/Disconnect: Connect to robot via NetworkTables

**Robot Control:**
- Mode: Select Teleop, Autonomous, or Test mode
- ENABLE/DISABLE: Enable or disable the robot
- Emergency Stop: Immediately disable the robot (with confirmation)

**Telemetry:**
- Battery Voltage: Real-time battery voltage with color coding
  - Green: > 11.5V
  - Orange: 10.0V - 11.5V
  - Red: < 10.0V
- RoboRIO CPU/RAM: Resource usage monitoring

**Controller:**
- Plug in any PS5 or Xbox controller
- Status shows controller name when connected
- Joystick data is automatically sent to robot when enabled

### Configuration File

Settings are saved to: `~/.frc_driverstation_config.json`

Default settings:
```json
{
  "team_number": 2026,
  "connect_on_startup": true,
  "alliance": "blue",
  "station": 1,
  "controller_deadzone": 0.1,
  "window_geometry": null
}
```

## Robot Integration

### Required NetworkTables Entries

Your robot code should publish these NetworkTables entries:

**SmartDashboard table:**
- `BatteryVoltage` (double): Battery voltage in volts
- `RoboRIO/CPU` (double): CPU usage percentage
- `RoboRIO/RAM` (double): RAM usage percentage

**DriverStation table (read by robot):**
- `Enabled` (boolean): Robot enable state
- `Mode` (string): Current mode ("teleop", "auto", "test")
- `Joystick/Axis{N}` (double): Joystick axis values
- `Joystick/Button{N}` (boolean): Button states

### Example Robot Code (Java)

```java
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;

public void robotPeriodic() {
    // Publish telemetry
    SmartDashboard.putNumber("BatteryVoltage", RobotController.getBatteryVoltage());
    SmartDashboard.putNumber("RoboRIO/CPU", /* CPU usage */);
    SmartDashboard.putNumber("RoboRIO/RAM", /* RAM usage */);
}

public void teleopPeriodic() {
    NetworkTable dsTable = NetworkTableInstance.getDefault().getTable("DriverStation");
    
    // Read joystick data
    double leftX = dsTable.getEntry("Joystick/Axis0").getDouble(0.0);
    double leftY = dsTable.getEntry("Joystick/Axis1").getDouble(0.0);
    boolean buttonA = dsTable.getEntry("Joystick/Button0").getBoolean(false);
    
    // Use joystick data for robot control
}
```

## Troubleshooting

### Cannot Connect to Robot

1. Verify robot is powered on
2. Check network connection (WiFi or Ethernet)
3. Confirm team number is correct
4. Try ping: `ping 10.TE.AM.2` (e.g., `ping 10.20.26.2` for team 2026)
5. Ensure robot code is running and publishing NetworkTables

### Controller Not Detected

1. Plug in controller before launching driver station
2. Try unplugging and replugging the controller
3. On Windows, ensure controller drivers are installed
4. On Linux, may need to run with sudo or add udev rules

### Telemetry Shows Zero

1. Verify robot code is publishing SmartDashboard values
2. Check NetworkTables connection is active
3. Ensure keys match exactly (case-sensitive)

### PyQt5 Installation Issues

**Windows:**
```powershell
pip install --upgrade pip setuptools wheel
pip install PyQt5
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyqt5
# Or use pip in venv
pip install PyQt5
```

**macOS:**
```bash
brew install pyqt5
# Or use pip in venv
pip install PyQt5
```

## Architecture

```
frc-driverstation/
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── run_driverstation.sh      # Linux/macOS launcher
├── run_driverstation.ps1     # Windows PowerShell launcher
├── run_driverstation.bat     # Windows batch launcher
├── gui/
│   └── main_window.py        # Main GUI window
├── network/
│   └── robot_connection.py   # NetworkTables client
├── controllers/
│   └── controller_manager.py # Controller input handling
└── utils/
    └── config.py             # Configuration management
```

## Development

### Adding Features

The codebase is designed to be simple and extensible:

- **GUI changes**: Edit `gui/main_window.py`
- **Network protocol**: Edit `network/robot_connection.py`
- **Controller mapping**: Edit `controllers/controller_manager.py`
- **Settings**: Edit `utils/config.py`

### Testing Without Robot

For testing the GUI without a robot:
1. Launch the driver station
2. Don't click "Connect"
3. Test UI interactions, controller detection, etc.

## Credits

Built for FRC Team 2026 using:
- PyQt5 for GUI
- pynetworktables for robot communication
- pygame for controller support

## License

Open source under WPILib BSD license.

---

**Questions or Issues?** Check the code comments or create an issue in the repository.
