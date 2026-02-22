# ☀️ MECHANICAL PLAN: Module I - SUN
**Designation:** Plasmonic Interfacial Solar Steam Generator (ISSG)  
**Version:** 1.0.0 | **License:** CERN-OHL-S

## 1. System Objective
To passively desalinate seawater, toxic brine, or wastewater using zero electricity. The system utilizes Localized Surface Plasmon Resonance (LSPR) and capillary nanoconfinement to break the theoretical limits of 1-Sun solar evaporation, delivering ultra-pure $H_2O$ to the WATER module.

## 2. Mechanical Architecture (V1.0 Node - Hacker Scale)
The SUN module requires no moving parts, relying entirely on capillary action, photothermal conversion, and gravity-fed condensation.
*   **The Basin (Brine Reservoir):** A $1000\text{mm} \times 1000\text{mm} \times 150\text{mm}$ structural basin made of black, food-grade High-Density Polyethylene (HDPE). Features a mechanical float-valve for continuous brine intake and a bottom-drain valve for flushing hypersaline discharge.
*   **The ISSG Membrane (The Sponge):** A $950\text{mm} \times 950\text{mm} \times 20\text{mm}$ bilayer matrix. 
    *   *Bottom Layer:* Expanded Polyethylene (EPE) foam for baseline buoyancy and thermal insulation from the bulk water.
    *   *Active Top Layer:* PAC Biochar (harvested from Module TERRE) bound with Polyvinyl Alcohol (PVA) and doped with Ag nanoparticles. Must float with exactly $2\text{mm}$ submerged to maintain optimal capillary pumping.
*   **The Condensation Canopy:** Single-pane UV-resistant PMMA (Acrylic) or tempered glass.
    *   *Critical Mechanical Angle:* Must be angled precisely between **15° and 22°**. If $< 15^\circ$, droplets will rain back into the brine. If $> 22^\circ$, optical reflection of incoming solar flux becomes inefficient.
    *   *Surface Coating:* Superhydrophilic silica nano-coating to ensure film-wise condensation.

## 3. Industrial Scale-Up (Gigafactory Scale)
*   **Topology:** Roll-to-roll continuous manufacturing produces kilometer-long biochar membranes floating on coastal brine raceways. 
*   **Optics:** Single-axis tracking Linear Fresnel reflectors concentrate 5-Sun irradiance onto the membrane.
*   **Vacuum Assist (ZLD):** Instead of passive condensation, industrial axial fans pull a slight vacuum across the membrane surface. The extracted vapor passes through concentric tube-in-tube heat exchangers to pre-heat the FIRE module, recovering the latent heat of condensation and achieving Zero Liquid Discharge (ZLD).

## 4. Open-Source CAD Manifest
*   `sun_basin_chassis.step`: Main structural trough with standard 1/2" NPT bulkheads.
*   `membrane_float_ring.stl`: 3D-printable corner brackets to assemble the EPS floating frame.
*   `condensate_gutter.step`: Extruded side-gutters that catch the pure water dripping from the canopy.

## 5. Bill of Materials (BOM) - V1.0 Node
| Item | Description | Material Spec | Qty |
|---|---|---|---|
| M1-01 | Main Basin | HDPE (Black, UV stabilized) | 1 |
| M1-02 | Condensation Canopy | PMMA / Acrylic ($3\text{mm}$ thick) | 1 |
| M1-03 | PAC Evaporator Matrix | Biochar + PVA Binder + $AgNO_3$ | 1 |
| M1-04 | Collection Gutter | Food-Grade PVC (Halved) | 1 |
| M1-05 | Level Float Valve | Standard mechanical float (Brass/Plastic) | 1 |

## 6. P&ID Routing
1. **Inlet:** Gravity-fed saltwater into the basin. Float-valve maintains exactly $10 \text{cm}$ of water depth.
2. **Evaporation Phase:** Solar flux hits the Ag-PAC matrix $\rightarrow$ LSPR heating $\rightarrow$ Vaporization.
3. **Condensation Phase:** Steam hits the angled cover, condenses, and runs via capillary action and gravity to the gutter.
4. **Outlet (Distillate):** Gravity drip into a sterile IBC tote (Routes to **MODULE 2: WATER**).
