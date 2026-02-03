"""
Main GUI window for FRC Driver Station.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QComboBox, QSpinBox, QGroupBox,
                              QGridLayout, QProgressBar, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import sys


class DriverStationWindow(QMainWindow):
    """Main driver station window."""
    
    def __init__(self, robot_connection, controller_manager, config):
        super().__init__()
        
        self.robot = robot_connection
        self.controller = controller_manager
        self.config = config
        
        self.setup_ui()
        self.setup_timers()
        
        # Restore window geometry
        geometry = self.config.get("window_geometry")
        if geometry:
            self.setGeometry(*geometry)
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("FRC Driver Station")
        self.setMinimumSize(1200, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top row: Connection and Robot Control
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_connection_group())
        top_layout.addWidget(self.create_robot_control_group())
        main_layout.addLayout(top_layout)
        
        # Middle row: Telemetry
        main_layout.addWidget(self.create_telemetry_group())
        
        # Bottom row: Controller status
        main_layout.addWidget(self.create_controller_group())
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_connection_group(self):
        """Create connection controls group."""
        group = QGroupBox("Connection")
        
        # Set larger font for group box
        group_font = QFont()
        group_font.setPointSize(16)
        group_font.setBold(True)
        group.setFont(group_font)
        
        layout = QVBoxLayout()
        
        # Set base font for labels and controls
        base_font = QFont()
        base_font.setPointSize(14)
        
        # Team number
        team_layout = QHBoxLayout()
        team_label = QLabel("Team Number:")
        team_label.setFont(base_font)
        team_layout.addWidget(team_label)
        self.team_spin = QSpinBox()
        self.team_spin.setFont(base_font)
        self.team_spin.setRange(1, 9999)
        self.team_spin.setValue(self.config.get("team_number", 2386))
        self.team_spin.valueChanged.connect(self.on_team_changed)
        team_layout.addWidget(self.team_spin)
        layout.addLayout(team_layout)
        
        # Connect button
        self.connect_btn = QPushButton("Connect")
        connect_font = QFont()
        connect_font.setPointSize(14)
        self.connect_btn.setFont(connect_font)
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        layout.addWidget(self.connect_btn)
        
        # Connection status
        self.connection_status = QLabel("● Disconnected")
        self.connection_status.setStyleSheet("color: red; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.connection_status)
        
        group.setLayout(layout)
        return group
    
    def create_robot_control_group(self):
        """Create robot control group."""
        group = QGroupBox("Robot Control")
        
        # Set larger font for group box
        group_font = QFont()
        group_font.setPointSize(16)
        group_font.setBold(True)
        group.setFont(group_font)
        
        layout = QVBoxLayout()
        
        # Set base font for labels and controls
        base_font = QFont()
        base_font.setPointSize(14)
        
        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        mode_label.setFont(base_font)
        mode_layout.addWidget(mode_label)
        self.mode_combo = QComboBox()
        self.mode_combo.setFont(base_font)
        self.mode_combo.addItems(["Teleop", "Autonomous", "Test"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)
        
        # Enable/Disable button
        self.enable_btn = QPushButton("ENABLE")
        self.enable_btn.setMinimumHeight(160)
        self.enable_btn.setEnabled(False)
        font = QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.enable_btn.setFont(font)
        self.enable_btn.clicked.connect(self.on_enable_clicked)
        self.enable_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        layout.addWidget(self.enable_btn)
        
        # Emergency Stop button
        self.estop_btn = QPushButton("🛑 EMERGENCY STOP")
        self.estop_btn.setMinimumHeight(100)
        estop_font = QFont()
        estop_font.setPointSize(24)
        estop_font.setBold(True)
        self.estop_btn.setFont(estop_font)
        self.estop_btn.clicked.connect(self.on_estop_clicked)
        self.estop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        layout.addWidget(self.estop_btn)
        
        group.setLayout(layout)
        return group
    
    def create_telemetry_group(self):
        """Create telemetry display group."""
        group = QGroupBox("Telemetry")
        
        # Set larger font for group box
        group_font = QFont()
        group_font.setPointSize(16)
        group_font.setBold(True)
        group.setFont(group_font)
        
        layout = QGridLayout()
        
        # Set base font for labels
        base_font = QFont()
        base_font.setPointSize(14)
        
        # Battery Voltage
        battery_label_text = QLabel("Battery Voltage:")
        battery_label_text.setFont(base_font)
        layout.addWidget(battery_label_text, 0, 0)
        self.battery_label = QLabel("0.00 V")
        self.battery_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        layout.addWidget(self.battery_label, 0, 1)
        
        self.battery_bar = QProgressBar()
        self.battery_bar.setRange(0, 130)  # 0-13.0V
        self.battery_bar.setValue(0)
        self.battery_bar.setMinimumHeight(40)
        layout.addWidget(self.battery_bar, 0, 2)
        
        # RoboRIO CPU
        cpu_label_text = QLabel("RoboRIO CPU:")
        cpu_label_text.setFont(base_font)
        layout.addWidget(cpu_label_text, 1, 0)
        self.cpu_label = QLabel("0%")
        self.cpu_label.setFont(base_font)
        layout.addWidget(self.cpu_label, 1, 1)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setMinimumHeight(40)
        layout.addWidget(self.cpu_bar, 1, 2)
        
        # RoboRIO RAM
        ram_label_text = QLabel("RoboRIO RAM:")
        ram_label_text.setFont(base_font)
        layout.addWidget(ram_label_text, 2, 0)
        self.ram_label = QLabel("0%")
        self.ram_label.setFont(base_font)
        layout.addWidget(self.ram_label, 2, 1)
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setMinimumHeight(40)
        layout.addWidget(self.ram_bar, 2, 2)
        
        group.setLayout(layout)
        return group
    
    def create_controller_group(self):
        """Create controller status group."""
        group = QGroupBox("Controller")
        
        # Set larger font for group box
        group_font = QFont()
        group_font.setPointSize(16)
        group_font.setBold(True)
        group.setFont(group_font)
        
        layout = QVBoxLayout()
        
        # Controller selector
        selector_layout = QHBoxLayout()
        selector_label = QLabel("USB Controller:")
        base_font = QFont()
        base_font.setPointSize(12)
        selector_label.setFont(base_font)
        selector_layout.addWidget(selector_label)
        
        self.controller_combo = QComboBox()
        self.controller_combo.setFont(base_font)
        self.controller_combo.currentIndexChanged.connect(self.on_controller_selected)
        selector_layout.addWidget(self.controller_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Controller status
        self.controller_status = QLabel("● No Controller")
        self.controller_status.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.controller_status)
        
        group.setLayout(layout)
        return group
    
    def setup_timers(self):
        """Setup update timers."""
        # Telemetry update timer (100ms)
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_telemetry)
        self.telemetry_timer.start(100)
        
        # Controller update timer (20ms / 50Hz)
        self.controller_timer = QTimer()
        self.controller_timer.timeout.connect(self.update_controller)
        self.controller_timer.start(20)
        
        # Controller list update timer (1 second)
        self.controller_list_timer = QTimer()
        self.controller_list_timer.timeout.connect(self.update_controller_list)
        self.controller_list_timer.start(1000)
    
    def on_connect_clicked(self):
        """Handle connect button click."""
        if not self.robot.is_connected():
            # Connect
            self.robot.team_number = self.team_spin.value()
            self.connect_btn.setEnabled(False)
            self.connect_btn.setText("Connecting...")
            
            # Connect in background (to avoid freezing UI)
            QTimer.singleShot(100, self.do_connect)
        else:
            # Disconnect
            self.robot.disconnect()
            self.on_connection_changed(False)
    
    def do_connect(self):
        """Actually perform the connection."""
        success = self.robot.connect()
        self.on_connection_changed(success)
    
    def on_connection_changed(self, connected):
        """Handle connection state change."""
        if connected:
            self.connection_status.setText("● Connected")
            self.connection_status.setStyleSheet("color: green; font-size: 28px; font-weight: bold;")
            self.connect_btn.setText("Disconnect")
            self.enable_btn.setEnabled(True)
            self.statusBar().showMessage(f"Connected to robot {self.team_spin.value()}")
        else:
            self.connection_status.setText("● Disconnected")
            self.connection_status.setStyleSheet("color: red; font-size: 28px; font-weight: bold;")
            self.connect_btn.setText("Connect")
            self.enable_btn.setEnabled(False)
            self.enable_btn.setText("ENABLE")
            self.enable_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
            self.statusBar().showMessage("Disconnected from robot")
        
        self.connect_btn.setEnabled(True)
    
    def on_enable_clicked(self):
        """Handle enable/disable button click."""
        if not self.robot.is_connected():
            return
        
        if not self.robot.enabled:
            # Enable robot
            self.robot.set_enabled(True)
            self.enable_btn.setText("DISABLE")
            self.enable_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            self.statusBar().showMessage("Robot ENABLED")
        else:
            # Disable robot
            self.robot.set_enabled(False)
            self.enable_btn.setText("ENABLE")
            self.enable_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            self.statusBar().showMessage("Robot DISABLED")
    
    def on_estop_clicked(self):
        """Handle emergency stop button click."""
        if self.robot.is_connected() and self.robot.enabled:
            reply = QMessageBox.question(self, 'Emergency Stop', 
                                         'Are you sure you want to emergency stop the robot?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.robot.set_enabled(False)
                self.enable_btn.setText("ENABLE")
                self.enable_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
                self.statusBar().showMessage("EMERGENCY STOP ACTIVATED")
    
    def on_mode_changed(self, mode_text):
        """Handle mode selection change."""
        mode_map = {
            "Teleop": "teleop",
            "Autonomous": "auto",
            "Test": "test"
        }
        mode = mode_map.get(mode_text, "teleop")
        self.robot.set_mode(mode)
        self.statusBar().showMessage(f"Mode changed to {mode_text}")
    
    def on_team_changed(self, team_number):
        """Handle team number change."""
        self.config.set("team_number", team_number)
    
    def update_telemetry(self):
        """Update telemetry displays."""
        if not self.robot.is_connected():
            return
        
        # Battery voltage
        voltage = self.robot.get_battery_voltage()
        self.battery_label.setText(f"{voltage:.2f} V")
        self.battery_bar.setValue(int(voltage * 10))
        
        # Color code battery voltage
        if voltage < 10.0:
            self.battery_label.setStyleSheet("font-size: 36px; font-weight: bold; color: red;")
        elif voltage < 11.5:
            self.battery_label.setStyleSheet("font-size: 36px; font-weight: bold; color: orange;")
        else:
            self.battery_label.setStyleSheet("font-size: 36px; font-weight: bold; color: green;")
        
        # RoboRIO status
        status = self.robot.get_roborio_status()
        cpu = status["cpu"]
        ram = status["ram"]
        
        self.cpu_label.setText(f"{cpu:.1f}%")
        self.cpu_bar.setValue(int(cpu))
        
        self.ram_label.setText(f"{ram:.1f}%")
        self.ram_bar.setValue(int(ram))
    
    def update_controller(self):
        """Update controller and send joystick data."""
        # Update controller status display
        if self.controller.is_connected():
            name = self.controller.get_controller_name()
            self.controller_status.setText(f"● {name}")
            self.controller_status.setStyleSheet("color: green; font-size: 28px; font-weight: bold;")
        else:
            self.controller_status.setText("● No Controller")
            self.controller_status.setStyleSheet("color: red; font-size: 28px; font-weight: bold;")
        
        # Send controller data to robot if enabled
        if self.robot.is_connected() and self.robot.enabled and self.controller.is_connected():
            axes = self.controller.get_axes()
            buttons = self.controller.get_buttons()
            self.robot.send_joystick_data(axes, buttons)
    
    def update_controller_list(self):
        """Update the list of available controllers."""
        available = self.controller.get_available_controllers()
        
        # Check if the list has changed
        current_count = self.controller_combo.count()
        if len(available) != current_count:
            # Block signals to avoid triggering selection change
            self.controller_combo.blockSignals(True)
            self.controller_combo.clear()
            
            if available:
                for index, name in available:
                    self.controller_combo.addItem(f"{index}: {name}", index)
            else:
                self.controller_combo.addItem("No controllers available", -1)
            
            self.controller_combo.blockSignals(False)
    
    def on_controller_selected(self, index):
        """Handle controller selection change."""
        if index >= 0:
            controller_index = self.controller_combo.itemData(index)
            if controller_index >= 0:
                self.controller.select_controller(controller_index)
                self.statusBar().showMessage(f"Controller {controller_index} selected")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Save window geometry
        geometry = self.geometry()
        self.config.set("window_geometry", (geometry.x(), geometry.y(), geometry.width(), geometry.height()))
        
        # Disconnect from robot
        if self.robot.is_connected():
            self.robot.disconnect()
        
        # Stop controller
        self.controller.stop()
        
        event.accept()
