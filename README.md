# 🦅 Autonomous Wildlife Camera

An autonomous wildlife monitoring station designed for long-term field observation.

The project combines nature observation with Linux, Raspberry Pi, networking, PoE, local storage, 4G connectivity and solar power.

> **Current status:** design and test-bench preparation.

---

## 🌿 Why this project?

Wildlife monitoring systems need more than a camera.

Long-term field deployment also requires reliable power, storage, networking, remote access and the ability to recover from failures.

The goal of this project is therefore not only to build a working system, but to understand and validate the complete technical chain before deploying it in the field.

**Observe → Test → Measure → Document → Improve**

---

## 🎯 Objectives

The station is being designed to provide:

- Long-term autonomous wildlife observation
- Day and night operation
- Remote 4G connectivity
- Local data storage
- Solar-powered operation
- System monitoring and logging
- Reliable recovery after power or network failures
- An architecture that can evolve over time

---

## 🧩 Planned architecture

### Camera

- Reolink RLC-811A
- Ethernet
- PoE
- Night vision

### Main computer

- Raspberry Pi 5
- Linux
- Python
- System monitoring
- Test automation and logging

### Storage

- USB 3 SSD
- Local storage for captured data and logs

### Connectivity

- Teltonika RUT241
- 4G connection
- Remote access
- Local network management

### Power

- 12 V architecture
- Battery
- Solar panel
- Charge controller / MPPT

The final battery and solar sizing will be based on **real measurements**, not only theoretical estimates.

---

## 🔬 Validation strategy

Before building the final autonomous station, a test bench will be used to validate the system.

### First test phase

A **72-hour test** is planned without solar power.

The test bench will be used to measure:

- Power consumption
- Day / night consumption differences
- Network stability
- 4G connectivity
- Camera and IR behaviour
- Storage usage
- System temperatures
- Long-duration stability
- Recovery after power loss
- Raspberry Pi and camera restart behaviour

The results will then be used to calculate the real energy requirements of the field system.

---

## 🚧 Current project stage

### Defined

- [x] Overall project concept
- [x] Raspberry Pi 5 architecture
- [x] Reolink RLC-811A camera
- [x] USB 3 SSD storage
- [x] Teltonika RUT241 for 4G
- [x] 12 V power architecture
- [x] 72-hour validation strategy
- [x] One-camera V1
- [x] Linux / VS Code development environment
- [x] GitHub documentation

### In progress

- [ ] Raspberry Pi 5 purchase
- [ ] Test-bench power supply
- [ ] PoE assembly
- [ ] Electrical measurements
- [ ] Multimeter selection
- [ ] Test procedure
- [ ] First Python scripts

---

## 🗺 Project map

The project architecture and technical decisions are documented in a living Markmap document:

🇫🇷 **[Project map — French](project-map-fr.md)**

The map will evolve together with the project.

---

## 🛠 Development environment

Current development environment:

- Kali Linux
- Windows
- Visual Studio Code
- Git
- GitHub
- Python
- Raspberry Pi

Python is being learned and applied progressively through the real needs of the project.

---

## 🔮 Future evolution

Once V1 has been validated, possible developments include:

- Two-camera architecture
- Automated test sequences
- Advanced monitoring interface
- Automated result comparison
- Data analysis
- Embedded AI

---

## 📚 Documentation philosophy

Important technical decisions will be documented with:

- What was chosen
- Why it was chosen
- What alternatives were considered
- What was measured
- What worked
- What failed
- What changed

The objective is to keep the project reproducible and understandable as it evolves.

---

## 🌱 Project philosophy

Technology is the tool.  
The field is the destination.