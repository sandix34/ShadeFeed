# V1 Test Bench

## Purpose

The V1 test bench is designed to validate the complete system architecture before any field deployment.

The objectives are to:

- validate the 12 V power architecture
- verify PoE camera operation
- validate Raspberry Pi 5 + SSD operation
- verify network communication
- measure real power consumption
- monitor system stability
- prepare the 72-hour reliability test

---

## Current architecture

> **Status: draft — 2026-08**
>
> This diagram represents the current V1 test-bench architecture.
> Power supply sizing, fuse ratings and some electrical details still need to be validated experimentally.

![V1 test bench architecture](test-bench-v1-architecture.png)

---

## Power architecture

The test bench is based on a common **12 V DC distribution bus**.

The 230 V AC side remains fully enclosed inside a commercial AC/DC power supply.

All user-accessible wiring and measurements are performed on the low-voltage DC side.

### Main branches

**12 V → Teltonika RUT241**

Direct 12 V supply for the network router.

**12 V → PLANET IPOE-162 → Reolink RLC-811A**

The PoE injector powers the camera and carries Ethernet data.

**12 V → 5 V USB-C converter → Raspberry Pi 5**

The Raspberry Pi 5 is powered through a dedicated DC/DC converter.

The local SSD is connected to the Raspberry Pi through USB 3.

---

## Planned measurement points

### M1 — Complete system

Measurement at the main 12 V output before distribution.

Purpose:

- total voltage
- total current
- total system power

### M2 — Camera / PoE branch

Measurement before the IPOE-162.

Purpose:

- camera + PoE injector consumption
- day/night comparison
- IR impact

### M3 — Raspberry Pi / SSD branch

Measurement before the 12 V → 5 V converter.

Purpose:

- Raspberry Pi consumption
- SSD impact
- workload variations

---

## Safety principle

No exposed 230 V wiring will be used in the test bench.

The mains side will use a fully enclosed commercial power supply with a standard wall plug.

All experimental wiring, measurements and modifications will be performed on the **12 V DC side only**.

---

## Still to validate

- [ ] Exact 12 V power supply
- [ ] Exact fuse ratings
- [ ] 12 V → 5 V / 5 A Raspberry Pi converter
- [ ] Distribution connectors
- [ ] Wire sections
- [ ] Measurement equipment
- [ ] Final electrical diagram
- [ ] 72-hour test protocol