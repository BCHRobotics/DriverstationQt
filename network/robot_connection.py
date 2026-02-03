"""
NetworkTables client for robot communication.
Handles connection, telemetry, and robot state.
"""

from networktables import NetworkTables
import time
from threading import Thread


class RobotConnection:
    """Manages NetworkTables connection to robot."""
    
    def __init__(self, team_number=2026):
        self.team_number = team_number
        self.connected = False
        self.nt = None
        self.ds_table = None
        self.robot_table = None
        
        # Telemetry data
        self.battery_voltage = 0.0
        self.roborio_cpu = 0.0
        self.roborio_ram = 0.0
        
        # Robot state
        self.enabled = False
        self.mode = "teleop"  # "teleop", "auto", "test"
        
        # Callbacks
        self.on_connection_changed = None
    
    def connect(self):
        """Connect to robot via NetworkTables."""
        try:
            # Calculate robot IP from team number
            team_str = str(self.team_number)
            if len(team_str) == 4:
                ip = f"10.{team_str[:2]}.{team_str[2:]}.2"
            else:
                ip = f"10.0.{team_str}.2"
            
            print(f"Connecting to robot at {ip}...")
            
            # Initialize NetworkTables
            NetworkTables.initialize(server=ip)
            
            # Get tables
            self.nt = NetworkTables
            self.ds_table = NetworkTables.getTable("DriverStation")
            self.robot_table = NetworkTables.getTable("SmartDashboard")
            
            # Wait for connection
            start_time = time.time()
            while not NetworkTables.isConnected() and time.time() - start_time < 5:
                time.sleep(0.1)
            
            self.connected = NetworkTables.isConnected()
            
            if self.connected:
                print(f"✓ Connected to robot")
                # Start telemetry update thread
                self._start_telemetry_thread()
            else:
                print(f"✗ Failed to connect to robot")
            
            if self.on_connection_changed:
                self.on_connection_changed(self.connected)
            
            return self.connected
            
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
            if self.on_connection_changed:
                self.on_connection_changed(False)
            return False
    
    def disconnect(self):
        """Disconnect from robot."""
        if self.connected:
            self.set_enabled(False)  # Disable robot before disconnecting
            NetworkTables.shutdown()
            self.connected = False
            if self.on_connection_changed:
                self.on_connection_changed(False)
            print("Disconnected from robot")
    
    def set_enabled(self, enabled):
        """Enable or disable the robot."""
        if not self.connected:
            return False
        
        try:
            self.enabled = enabled
            self.ds_table.putBoolean("Enabled", enabled)
            self.ds_table.putString("Mode", self.mode)
            return True
        except Exception as e:
            print(f"Error setting enabled state: {e}")
            return False
    
    def set_mode(self, mode):
        """Set robot mode (teleop, auto, test)."""
        if mode not in ["teleop", "auto", "test"]:
            return False
        
        self.mode = mode
        if self.connected:
            try:
                self.ds_table.putString("Mode", mode)
                return True
            except Exception as e:
                print(f"Error setting mode: {e}")
                return False
        return True
    
    def send_joystick_data(self, axes, buttons):
        """Send joystick data to robot."""
        if not self.connected or not self.enabled:
            return
        
        try:
            # Send axis values
            for i, value in enumerate(axes):
                self.ds_table.putNumber(f"Joystick/Axis{i}", value)
            
            # Send button states
            for i, pressed in enumerate(buttons):
                self.ds_table.putBoolean(f"Joystick/Button{i}", pressed)
        
        except Exception as e:
            print(f"Error sending joystick data: {e}")
    
    def _start_telemetry_thread(self):
        """Start background thread to update telemetry."""
        def update_telemetry():
            while self.connected and NetworkTables.isConnected():
                try:
                    # Read telemetry from SmartDashboard
                    self.battery_voltage = self.robot_table.getNumber("BatteryVoltage", 0.0)
                    self.roborio_cpu = self.robot_table.getNumber("RoboRIO/CPU", 0.0)
                    self.roborio_ram = self.robot_table.getNumber("RoboRIO/RAM", 0.0)
                    
                    time.sleep(0.1)  # Update at 10Hz
                except Exception as e:
                    print(f"Telemetry error: {e}")
                    break
            
            # Connection lost
            if self.connected:
                self.connected = False
                if self.on_connection_changed:
                    self.on_connection_changed(False)
                print("Lost connection to robot")
        
        thread = Thread(target=update_telemetry, daemon=True)
        thread.start()
    
    def get_battery_voltage(self):
        """Get current battery voltage."""
        return self.battery_voltage
    
    def get_roborio_status(self):
        """Get RoboRIO CPU and RAM usage."""
        return {"cpu": self.roborio_cpu, "ram": self.roborio_ram}
    
    def is_connected(self):
        """Check if connected to robot."""
        return self.connected and NetworkTables.isConnected()
