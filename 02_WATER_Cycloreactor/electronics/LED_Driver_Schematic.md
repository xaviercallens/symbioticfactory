# 💡 KiCad Schematic: WS2812B LED Pulse Driver for Cycloreactor

**Module II (WATER) — Electronics**  
**Version:** 1.0.0 | **License:** CERN-OHL-S

## Overview

This document specifies the electronics layout for driving the WS2812B Addressable LED strips that implement the **Flashing-Light Effect** on the algal photobioreactor. The ESP32 microcontroller drives the LEDs at frequencies matching the Plastoquinone (PQ) pool turnover rate ($10-50\text{ Hz}$) to prevent photoinhibition and maximize photosynthetic quantum yield.

## Circuit Architecture

```
                    ┌──────────────────┐
                    │     ESP32-S3     │
                    │   DevKit v1.0    │
                    │                  │
  5V Power ──────── │ VIN         GND  │ ──── GND Rail
                    │                  │
  OD Sensor ─────── │ GPIO36 (ADC)     │
  pH Probe ──────── │ GPIO39 (ADC)     │
  Thermistor ────── │ GPIO34 (ADC)     │
                    │                  │
                    │ GPIO16 (DATA) ───│──── WS2812B Strip (DATA IN)
                    │ GPIO17 (DATA) ───│──── WS2812B Strip 2 (if >150 LEDs)
                    │                  │
  MQTT WiFi ─────── │ Internal WiFi    │
                    └──────────────────┘
```

## Wiring Specification

### Power Budget Calculation
Each WS2812B LED draws up to $60\text{mA}$ at full white. The flashing-light protocol only drives Red ($680\text{nm}$) and Blue ($450\text{nm}$) channels alternately:

| Parameter | Value |
|---|---|
| Red channel current per LED | $20\text{mA}$ |
| Blue channel current per LED | $20\text{mA}$ |
| Max simultaneous LEDs (one strip) | 150 |
| Peak current draw | $3.0\text{A}$ |
| Duty cycle (50% flash) | $1.5\text{A}$ average |

### Required Components

| Ref | Component | Specification | Qty |
|---|---|---|---|
| U1 | ESP32-S3 DevKit | WiFi + BLE, Dual Core, 240 MHz | 1 |
| PS1 | DC Power Supply | 5V / 10A Switching PSU | 1 |
| LED1 | WS2812B Strip | IP67 Waterproof, 60 LED/m, 5m | 1 |
| R1 | Data Line Resistor | $330\Omega$, 1/4W (between GPIO and DATA IN) | 1 |
| C1 | Bulk Decoupling Cap | $1000\mu\text{F}$, 6.3V Electrolytic | 1 |
| C2 | Per-strip Bypass Cap | $100\mu\text{F}$, 6.3V (at strip power injection) | 2 |
| R2 | OD Sensor Pull-down | $10k\Omega$ | 1 |
| J1 | Screw Terminal Block | 5mm pitch, 2-pos (Power) | 2 |

### Critical Wiring Notes

1. **Data Resistor (R1, $330\Omega$):** MANDATORY. Place inline on the DATA line, as close to the first LED as possible. This prevents ringing on the high-speed NZR signal.
2. **Power Injection:** For strips longer than $2\text{m}$ ($>120$ LEDs), inject $5\text{V}$ power at both ends of the strip to prevent voltage drop (the far LEDs will appear dimmer/redder).
3. **Common Ground:** The ESP32 GND and the LED strip GND MUST be tied together. Floating grounds will corrupt the data signal.
4. **Waterproofing:** The LED strips wrap around the exterior of the polycarbonate tube. Use IP67-rated strips and seal all wire connections with marine-grade heat shrink.

## Optical Density (OD) Sensor Circuit

The OD sensor provides real-time biomass concentration feedback to the ESP32, which dynamically adjusts the LED pulse frequency via the `yield_optimization.py` AI script.

```
                    ┌─────────────────┐
  3.3V ──── R_LED ──│ IR LED (880nm)  │──── GND
                    │   (Emitter)     │
                    └─────────────────┘
                           ↓ (through culture)
                    ┌─────────────────┐
  3.3V ──── R_pull ─│ Phototransistor │──── GPIO36 (ADC)
                    │   (Detector)    │
                    └─────────────────┘
```

| Component | Value | Purpose |
|---|---|---|
| IR LED (880nm) | $20\text{mA}$ (with $R_{LED} = 68\Omega$) | Emits through the algal culture |
| Phototransistor | BPW34 or equivalent | Detects transmitted light |
| R_pull | $10k\Omega$ to 3.3V | Voltage divider for ADC reading |

**OD Calibration:** At $OD_{680} = 0$ (clear water), the ADC reads ~3.3V. As biomass increases, transmitted light drops, and ADC voltage decreases linearly. An $OD_{680} > 2.0$ ($\approx 10\text{ g/L}$) triggers the harvest valve via the ESP32.

## PCB / Breadboard Layout

A KiCad project file will be added in a future contribution. For prototyping, assemble on a standard solderless breadboard following the schematic above.

### Pin Assignment Summary

| ESP32 Pin | Function | Connected To |
|---|---|---|
| GPIO16 | NeoPixel Data Out | LED Strip 1 DIN (via $330\Omega$) |
| GPIO17 | NeoPixel Data Out | LED Strip 2 DIN (if needed) |
| GPIO36 | ADC (OD Sensor) | Phototransistor voltage divider |
| GPIO39 | ADC (pH Probe) | pH 4502C module output |
| GPIO34 | ADC (Temperature) | NTC Thermistor divider ($10k\Omega$) |
| GPIO25 | PWM (Peristaltic Pump) | Acid dosing pump MOSFET gate |
| GPIO26 | Digital (Harvest Valve) | 3-way solenoid valve relay |
| VIN | 5V Power | From PSU (shared with LEDs) |
| GND | Common Ground | All components |
