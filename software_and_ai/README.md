# The Cybernetic Nervous System

This directory contains the edge-control firmware and cloud/edge predictive AI models necessary to run the Symbiotic Factory autonomously.

## 1. ESP32 Edge Firmware (`esp32_firmware/`)
The ESP32 microcontroller handles real-time hardware interaction: high-speed LED pulsing to bypass photoinhibition (WATER), and strict PID loops for thermal/pH regulation during anaerobic fermentation (FIRE).

### How to Flash:
1. Install [PlatformIO](https://platformio.org/).
2. Open the `esp32_firmware` folder.
3. Update your `ssid` and `password` in `src/main.cpp`.
4. Compile and upload to your ESP32 board:
   ```bash
   pio run -t upload
   ```

## 2. Predictive AI Models (`ai_predictive_models/`)
These Python models run on an edge computer (like a Raspberry Pi) to ingest MQTT telemetry and optimize the biological kinetics continuously.

### How to Run:
1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Yield Optimization (WATER):**
   Runs an MQTT listener that calculates the exact LED pulse frequency needed to match the Plastoquinone pool turnover rate based on increasing optical density.
   ```bash
   python yield_optimization.py
   ```
3. **Subcritical HTL Thermodynamics (FIRE):**
   A formal physical model for predicting dielectric shifts and reaction kinetics during high-pressure thermal depolymerization.
   ```bash
   python htl_thermodynamics.py
   ```
