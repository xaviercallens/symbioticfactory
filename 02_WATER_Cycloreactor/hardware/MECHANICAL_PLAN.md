# 💧 MECHANICAL PLAN: Module II - WATER
**Designation:** Nano-Bubbling Algal Cycloreactor  
**Version:** 1.0.0 | **License:** CERN-OHL-S

## 1. System Objective
To achieve hyper-productive $CO_2$ absorption and algal biomass generation. The mechanics maximize gas-liquid mass transfer (via Laplace-pressured nano-bubbles) and bypass photoinhibition via a hydrodynamically induced "flashing-light" effect.

## 2. Mechanical Architecture (V1.0 Node - Hacker Scale)
*   **The Pressure Vessel:** A vertically oriented transparent cylinder ($150\text{mm}$ OD, $2000\text{mm}$ height). Constructed from clear Polycarbonate (PC) for superior impact resistance over Acrylic.
*   **The Helical Stator (The "Turbulator"):** A central 3D-printed helical baffle running down the center of the tube. Water is pumped in tangentially at the base, forcing the fluid to spin aggressively up the stator. This throws algae cells to the illuminated outer wall and sucks them back to the dark inner core continuously (10-50 Hz).
*   **The Venturi Nano-Bubbler Manifold:** At the base liquid inlet, a 3D-printed Venturi nozzle creates a pressure drop, shearing injected $CO_2$ violently through a sintered titanium frit (pore size $< 0.5 \mu\text{m}$). This dual-shear mechanism guarantees bubbles under $200\text{nm}$.
*   **Thermal/Optical Jacket:** Exterior wraps of WS2812B Addressable LED strips (tuned to Red 680nm / Blue 450nm) mounted on extruded aluminum heat sinks.

## 3. Industrial Scale-Up (Taylor-Couette PBRs)
*   **Topology:** $100 \text{ m}^3$ transparent fiberglass-reinforced polycarbonate silos. 
*   **Mechanics:** Instead of passive stators, industrial versions use active *Taylor-Couette flow*. A central rotating inner cylinder creates highly controlled, high-shear toroidal vortices, maximizing the flashing-light effect without damaging cell walls.
*   **Gas Transfer:** Industrial flue-gas is passed through massive arrays of hollow-fiber membrane (HFM) contactors made of hydrophobic PTFE, achieving $98\%$ $CO_2$ dissolution efficiency.

## 4. Open-Source CAD Manifest
*   `helical_stator_core_v2.step`: Parametric file. Adjust the pitch angle based on the viscosity of your specific algal strain.
*   `venturi_injector_nozzle.stl`: 3D-printable Venturi body (print in PETG or Nylon for pressure resistance). Requires a standard $1/4"$ NPT threaded insert.
*   `tangential_base_manifold.step`: The bottom cap of the reactor that directs incoming water at a $90^\circ$ angle to initiate the cyclonic vortex.

## 5. Bill of Materials (BOM) - V1.0 Node
| Item | Description | Material Spec | Qty |
|---|---|---|---|
| M2-01 | Main Tube | Polycarbonate (Clear, $3\text{mm}$ wall) | 1 |
| M2-02 | Helical Stator | PETG (3D Printed, 6 interlocking segments) | 1 Set |
| M2-03 | Mag-Drive Pump | Polypropylene/Ceramic ($15-30 \text{ L/min}$) | 1 |
| M2-04 | Venturi + Frit | PTFE / Sintered Titanium ($0.5 \mu\text{m}$) | 1 |
| M2-05 | LED Array Wrap | WS2812B (IP67 Waterproof) | 5 meters |

## 6. P&ID Routing
1. **Gas Inlet:** $CO_2$ source $\rightarrow$ Micro-compressor $\rightarrow$ Venturi Nozzle $\rightarrow$ Ceramic Frit $\rightarrow$ Bottom of the PBR.
2. **Liquid Loop:** Bottom drain $\rightarrow$ Recirculation Pump $\rightarrow$ Tangential inlet at the bottom.
3. **Harvest Outlet:** A 3-way motorized ball valve on the recirculation loop. When OD hits peak threshold ($>10 \text{ g/L}$), valve diverts $30\%$ of the liquid to harvest (Routes to **MODULE 4: FIRE**).
