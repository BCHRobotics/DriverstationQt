"""
Configuration management for FRC Driver Station.
Handles saving and loading user settings.
"""

import json
import os
from pathlib import Path


class Config:
    """Manages driver station configuration settings."""
    
    def __init__(self):
        self.config_file = Path.home() / ".frc_driverstation_config.json"
        self.settings = self.load()
    
    def load(self):
        """Load settings from config file."""
        default_settings = {
            "team_number": 2026,
            "connect_on_startup": True,
            "alliance": "blue",  # "red" or "blue"
            "station": 1,  # 1, 2, or 3
            "controller_deadzone": 0.1,
            "window_geometry": None,  # (x, y, width, height)
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new settings were added)
                    default_settings.update(loaded)
                    return default_settings
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
                return default_settings
        
        return default_settings
    
    def save(self):
        """Save current settings to config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save."""
        self.settings[key] = value
        self.save()
