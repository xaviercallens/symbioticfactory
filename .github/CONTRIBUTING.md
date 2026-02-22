# 🤝 How to Contribute to the Symbiotic Factory

We are decentralizing gigaton-scale carbon removal. We need a planetary coalition of hackers, engineers, and scientists. Here is how you can help:

---

## 📐 Hardware / CAD Engineers
**Current Bounties:** 
* Generate `.STEP` exports from the existing OpenSCAD scripts in `01_SUN`, `02_WATER` modules for direct use in FreeCAD/Fusion360.
* Design the tangential base manifold for the WATER cycloreactor that directs incoming water at $90^\circ$ to initiate the cyclonic vortex.
* Improve the TLUD retort air damper mechanism for finer temperature control during pyrolysis.

**Rules:** Prefer open-source CAD (FreeCAD, OpenSCAD, Blender). Always upload neutral formats (`.STEP`, `.IGES`, `.STL`).

## 💻 Embedded Devs / AI Engineers
**Current Bounties:**
* Build a web dashboard (ESP32 → MQTT → Node-RED or Grafana) for remote monitoring of reactor telemetry.
* Implement adaptive LED frequency control using live OD sensor feedback in the ESP32 firmware.
* Expand the Digital Twin to support multi-objective optimization (maximize EROI + minimize water use simultaneously).

**Rules:** Comment your code thoroughly. Include wiring diagrams (Fritzing/KiCad).

## 🧬 Chemists / Bio-Hackers
**Current Bounties:**
* Improve the $Ag/WO_3$ Z-Scheme photocatalyst synthesis protocol to increase solar-to-CO conversion efficiency using garage-accessible chemicals.
* Test alternative algal strains (*Nannochloropsis*, *Scenedesmus*) for higher lipid content and report growth curves.
* Establish a P2P mailing network for sharing high-lipid halotolerant microalgae and extreme gas-fermenting bacterial strains.

**Rules:** Always include Safety Data Sheets (SDS) and safe disposal protocols for chemical waste.

## 🖥️ Digital Twin Contributors
**Current Bounties:**
* **CRITICAL:** Optimize the heat exchanger design (`04_FIRE_Simulations/heat_exchanger_model.py`) to achieve $>85\%$ thermal recovery. The current 2m concentric tube only achieves 39% — this is the primary EROI bottleneck.
* Run OpenFOAM CFD simulations on the helical stator geometry and validate the $k_La$ mass transfer coefficient.
* Execute the Code_Aster FEA on a real `.STEP` mesh of the 500mL Swagelok cylinder and report the Von Mises stress map.
* Add CI/CD tests that automatically gate PRs on EROI $> 3.5$.

**Rules:** All simulation code must be reproducible. Use the provided `Dockerfile` for environment consistency.

---

## 🔄 Contribution Workflow

1. **Fork** the repository.
2. **Run the Digital Twin** (`python run_digital_twin.py`) to establish your baseline.
3. **Make your changes** (hardware, firmware, wetware, or simulation).
4. **Re-run the Digital Twin** to verify your change doesn't break the EROI.
5. **Open a PR** with your simulation results attached.

## ⚠️ Safety-Critical Contributions

Any PR that modifies `hardware/` files in the FIRE module **must** include:
- Updated pressure ratings and safety factors.
- A Code_Aster FEA screenshot or report showing SF $> 1.67$.
- Explicit review by at least 2 contributors before merge.
