---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 3
---

# Autonomous Wildlife Camera Project

## 1. Project objective

### Purpose
- Design an autonomous wildlife monitoring station
- Enable long-term field observation
- Allow remote system supervision
- Document each technical decision

### Main objectives
- Long-term autonomy
- Day and night operation
- 4G connectivity
- Local storage
- Solar power
- Reliable and scalable system

### Working method
- Design
- Test
- Measure
- Improve
- Document
- Deploy only after validation

## 2. General architecture

### Camera
- Reolink RLC-811A
- Ethernet
- PoE
- Night vision

### Main computer
- Raspberry Pi 5
- Linux
- Python scripts
- System monitoring
- Logging

### Storage
- USB 3 SSD
- Local data storage

### Connectivity
- Teltonika RUT241 4G router
- Remote access
- Local system network

### Power
- 12 V architecture
- Battery
- Solar panel
- Power regulation
- Final sizing based on real measurements

## 3. Why a test bench?

### Problem
- Real power consumption is not known yet
- Night operation may significantly affect power consumption
- Network stability must be validated
- Restarts and power failures must be tested

### Decision
- Build a test bench before finalizing the field system

### Test bench objectives
- Validate the complete architecture
- Measure real power consumption
- Test system stability
- Identify weak points
- Correct issues before deployment

## 4. V1 test bench

### Target duration
- 72 hours

### Scope
- One camera
- Raspberry Pi
- SSD
- Network
- 4G
- PoE
- Measurements
- No solar power during the first test phase

### Success criteria
- Stable system
- Usable measurements
- Controlled restart behaviour
- Known power consumption
- Known storage requirements
- Architecture understood and documented

## 5. Raspberry Pi

### Selected platform
- Raspberry Pi 5

### Associated hardware
- Active Cooler
- Case
- Suitable power supply

### Role
- Control the tests
- Communicate with the camera
- Run Python scripts
- Record results
- Generate logs
- Prepare for a future interface

## 6. Power / PoE

### Components under study
- IPOE-162
- Power supply
- Female DC jack connector with wires
- Required cabling
- Ethernet

### Safety
- Standard wall plug on the mains side
- No exposed or unsafe 230 V wiring
- Low-voltage work only during testing

### Measurement
- Multimeter
- Voltage checks
- Continuity checks
- Wiring diagnostics

## 7. Network

### Home development setup
- Raspberry Pi connected to the home Wi-Fi
- Computer connected to the same network
- No dedicated router required for the initial development phase

### Raspberry Pi access
- SSH
- VS Code Remote

### Field deployment
- RUT241 for 4G connectivity
- Local station network
- Remote access method to be defined precisely

## 8. Software

### Workstation
- Kali Linux
- Windows
- VS Code

### Raspberry Pi
- Linux
- Python
- Git

### Python
- Learned progressively through the project
- Simple scripts first
- Gradual automation

### GitHub
- Version control
- Documentation
- Decision history
- Future project sharing

### Security
- No passwords stored in the repository
- Environment variables
- Local files excluded from Git
- `.gitignore`

## 9. Planned measurements

### Power
- Voltage
- Power consumption
- Average consumption
- Consumption peaks
- Day / night differences

### Network
- Connectivity
- Latency
- Disconnections
- Reconnection
- 4G stability

### Camera
- Day operation
- Night operation
- IR behaviour
- Image quality
- Stream stability

### Storage
- Data volume generated
- Throughput
- Storage used over 72 hours

### Reliability
- Temperature
- Long-duration operation
- Raspberry Pi restart
- Camera restart
- Recovery after power loss

## 10. Final power system

### Before validation
- Battery and solar system are not finalized yet

### After the 72-hour test
- Calculate real daily energy requirements
- Size the battery
- Size the solar array
- Add safety margins
- Select the charge controller / MPPT

## 11. Project documentation

### Documents
- README
- Markmap
- Schematics
- BOM
- Test procedures
- Results
- Decision log

### Documentation rules
- Every important choice should be dated
- Every architecture change should explain why it was made
- Rejected or postponed options should remain documented

## 12. V2

### Possible future developments
- Two-camera architecture
- Advanced automation
- Result comparison
- Monitoring interface
- Automated analysis
- Embedded AI

## 13. Current status

### Defined
- Autonomous wildlife monitoring station concept
- Raspberry Pi 5
- Reolink RLC-811A
- USB 3 SSD
- Teltonika RUT241
- 12 V architecture
- 72-hour test bench
- One camera for V1
- Kali Linux + VS Code
- Python
- GitHub
- Markmap documentation

### To be finalized
- Test bench electrical diagram
- Exact power supply
- Final multimeter choice
- Raspberry Pi 5 purchase
- Case and cooling
- PoE assembly
- 72-hour test procedure
- GitHub repository structure