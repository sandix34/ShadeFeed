# Technical Decision Log

This document records important technical decisions made during the project.

---

## 2026-08 — One camera for V1

**Status:** Accepted

### Decision
V1 will use a single camera.

### Why
The objective of V1 is to validate the complete architecture before adding complexity.

### Alternative considered
Two cameras from the first prototype.

### Consequence
Dual-camera operation is postponed to V2.

---

## 2026-08 — 72-hour test bench before final power sizing

**Status:** Accepted

### Decision
Run a 72-hour test bench before selecting the final battery and solar system.

### Why
Real power consumption, including night operation and IR, must be measured before sizing the autonomous power system.

### Alternative considered
Sizing the battery and solar panel only from theoretical consumption estimates.

### Consequence
Battery, solar panel and MPPT remain provisional until measurements are available.

---

## 2026-08 — USB 3 SSD for local storage

**Status:** Accepted

### Decision
Use a USB 3 SSD for local storage.

### Why
It provides suitable storage performance while keeping the Raspberry Pi PCIe interface available.

### Future consideration
PCIe may later be used for an AI accelerator or another hardware extension.