#!/usr/bin/env python3
"""
FRC Driver Station - Simple Platform-Independent Driver Station
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import DriverStationWindow
from network.robot_connection import RobotConnection
from controllers.controller_manager import ControllerManager
from utils.config import Config


def main():
    """Main application entry point."""
    print("=" * 60)
    print("FRC Driver Station - Simple Edition")
    print("=" * 60)
    
    # Load configuration
    config = Config()
    print(f"Team Number: {config.get('team_number')}")
    
    # Initialize robot connection
    robot = RobotConnection(team_number=config.get('team_number'))
    
    # Initialize controller manager
    controller = ControllerManager(deadzone=config.get('controller_deadzone', 0.1))
    controller.start()
    
    # Setup connection callback
    def on_connection_changed(connected):
        if connected:
            print(f"✓ Connected to robot")
        else:
            print("✗ Disconnected from robot")
    
    robot.on_connection_changed = on_connection_changed
    
    # Setup controller callback
    def on_controller_changed(connected, name):
        if connected:
            print(f"✓ Controller connected: {name}")
        else:
            print("✗ Controller disconnected")
    
    controller.on_controller_changed = on_controller_changed
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("FRC Driver Station")
    app.setOrganizationName("FRC")
    
    # Create main window
    window = DriverStationWindow(robot, controller, config)
    window.show()
    
    # Auto-connect if configured
    if config.get('connect_on_startup'):
        print("Auto-connecting to robot...")
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(500, window.on_connect_clicked)
    
    print("\nDriver Station Ready!")
    print("Plug in a PS5 or Xbox controller to send commands to the robot.")
    print("-" * 60)
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
