"""
Controller manager for PS5 and Xbox controller support.
Uses pygame for cross-platform joystick input.
"""

import pygame
from threading import Thread
import time


class ControllerManager:
    """Manages game controller input."""
    
    def __init__(self, deadzone=0.1):
        self.deadzone = deadzone
        self.joystick = None
        self.running = False
        self.thread = None
        
        # Controller state
        self.axes = []
        self.buttons = []
        self.controller_name = "No Controller"
        
        # Callbacks
        self.on_controller_changed = None
        
        # Initialize pygame joystick module
        pygame.init()
        pygame.joystick.init()
    
    def start(self):
        """Start controller input thread."""
        self.running = True
        self.thread = Thread(target=self._input_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop controller input thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
    
    def _input_loop(self):
        """Background thread to read controller input."""
        while self.running:
            try:
                # Check for controller connection/disconnection
                pygame.event.pump()
                
                if pygame.joystick.get_count() > 0:
                    if self.joystick is None:
                        # Controller connected
                        self.joystick = pygame.joystick.Joystick(0)
                        self.joystick.init()
                        self.controller_name = self.joystick.get_name()
                        print(f"Controller connected: {self.controller_name}")
                        
                        if self.on_controller_changed:
                            self.on_controller_changed(True, self.controller_name)
                    
                    # Read controller state
                    num_axes = self.joystick.get_numaxes()
                    num_buttons = self.joystick.get_numbuttons()
                    
                    # Read axes
                    self.axes = []
                    for i in range(num_axes):
                        value = self.joystick.get_axis(i)
                        # Apply deadzone
                        if abs(value) < self.deadzone:
                            value = 0.0
                        self.axes.append(value)
                    
                    # Read buttons
                    self.buttons = []
                    for i in range(num_buttons):
                        self.buttons.append(self.joystick.get_button(i))
                
                else:
                    if self.joystick is not None:
                        # Controller disconnected
                        self.joystick.quit()
                        self.joystick = None
                        self.controller_name = "No Controller"
                        self.axes = []
                        self.buttons = []
                        print("Controller disconnected")
                        
                        if self.on_controller_changed:
                            self.on_controller_changed(False, self.controller_name)
                
                time.sleep(0.02)  # 50Hz update rate
                
            except Exception as e:
                print(f"Controller error: {e}")
                time.sleep(0.1)
    
    def get_axes(self):
        """Get current axis values."""
        return self.axes
    
    def get_buttons(self):
        """Get current button states."""
        return self.buttons
    
    def is_connected(self):
        """Check if a controller is connected."""
        return self.joystick is not None
    
    def get_controller_name(self):
        """Get the name of the connected controller."""
        return self.controller_name
    
    def set_deadzone(self, deadzone):
        """Set joystick deadzone."""
        self.deadzone = deadzone
