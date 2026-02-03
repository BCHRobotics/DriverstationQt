# Quick Start Guide

## For Users Who Just Want to Drive

### Windows
1. Double-click `run_driverstation.bat`
2. Wait for setup to complete
3. Enter your team number
4. Click "Connect"
5. Plug in Xbox or PS5 controller
6. Click "ENABLE"
7. Drive!

### macOS/Linux
1. Open terminal in this folder
2. Run: `./run_driverstation.sh`
3. Enter your team number
4. Click "Connect"
5. Plug in Xbox or PS5 controller
6. Click "ENABLE"
7. Drive!

## Common Team Numbers
- Team 2026 → Robot IP: 10.20.26.2
- Team 254 → Robot IP: 10.2.54.2
- Team 1114 → Robot IP: 10.11.14.2

## Safety
- 🛑 **Emergency Stop button is in the bottom right**
- Robot will disable if connection is lost
- Red button turns to green when robot is enabled

## What the Colors Mean

**Connection Status:**
- 🟢 Green = Connected to robot
- 🔴 Red = Not connected

**Battery Voltage:**
- 🟢 Green = > 11.5V (Good)
- 🟠 Orange = 10.0-11.5V (Low)
- 🔴 Red = < 10.0V (Critical - replace battery!)

**Enable Button:**
- 🟢 Green = Robot disabled (safe)
- 🔴 Red = Robot enabled (ROBOT WILL MOVE!)

## Controller Layout

**PS5 Controller:**
- Left Stick = Drive forward/backward + strafe
- Right Stick = Rotate
- All buttons and triggers work

**Xbox Controller:**
- Left Stick = Drive forward/backward + strafe
- Right Stick = Rotate
- All buttons and triggers work

## Troubleshooting

**"Cannot connect"**
→ Check robot is on and you're on the right WiFi network

**"No controller"**
→ Plug in controller, then restart driver station

**Telemetry shows all zeros**
→ Robot code may not be publishing data to NetworkTables

---

For more details, see README.md
