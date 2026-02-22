detailed mechanical and industrial engineering blueprints for each of the four modules.

They are formatted as technical Markdown (`.md`) files. You can copy and paste these directly into the `hardware/MECHANICAL_PLAN.md` file within each module's respective directory in your GitHub repository.

---

### 📂 File Path: `01_SUN_Desalination/hardware/MECHANICAL_PLAN.md`

```markdown
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

```

---

### 📂 File Path: `02_WATER_Cycloreactor/hardware/MECHANICAL_PLAN.md`

```markdown
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

```

---

### 📂 File Path: `03_TERRE_Biochar/hardware/MECHANICAL_PLAN.md`

```markdown
# 🌍 MECHANICAL PLAN: Module III - TERRE
**Designation:** TLUD (Top-Lit Updraft) Double-Barrel Gasifier  
**Version:** 1.0.0 | **License:** CERN-OHL-S

## 1. System Objective
Thermochemical stabilization of waste biomass into Polycyclic Aromatic Carbon (PAC) via slow, anaerobic pyrolysis. Produces a permanent ($>1000$ yr) soil amendment and the carbon matrix for Module SUN.

## 2. Mechanical Architecture (V1.0 Node - Hacker Scale)
*   **Outer Heating Jacket (Barrel 1):** Standard 55-gallon steel drum. 
    *   *Modifications:* Cut off the top. Drill sixteen $20\text{mm}$ holes around the bottom perimeter for primary combustion air intake. Drill sixteen $10\text{mm}$ holes around the top perimeter for secondary air intake.
*   **Inner Anaerobic Retort (Barrel 2):** Standard 30-gallon steel drum.
    *   *Modifications:* Must have a tight-fitting clamp lid. Drill twelve $10\text{mm}$ holes *only in the bottom*. 
*   **Fluid Dynamics of the Retort:** The 30-gallon drum (packed with waste) is placed inside the 55-gallon drum. A fire is lit in the gap between them. As the inner drum heats up to $500^\circ\text{C}$, it outgasses volatile syngas ($CO$, $H_2$, $CH_4$). This gas is forced out the bottom holes, mixes with draft air in the outer jacket, and combusts. This forms a self-sustaining thermal loop that bakes the biochar without oxygenating the carbon.
*   **Quench Seal:** A high-temp silicone/fiberglass rope seal and mechanical clamp ring to completely starve the system of oxygen during the cooling phase.

## 3. Industrial Scale-Up (CSP-Driven Continuous Rotary Kiln)
*   **Topology:** A $15\text{m}$ long, horizontal Inconel tube with an internal Archimedes screw conveyor, operating at a $5^\circ$ incline.
*   **Thermodynamics:** Instead of burning biomass for heat, a Concentrated Solar Power (CSP) heliostat field heats inert ceramic Particle Heat Carriers (PHCs) to $800^\circ\text{C}$. These cascade over the exterior of the Inconel tube, providing zero-carbon endothermic heat.
*   **Air-Locks:** Double rotary-valve airlocks at the feed and discharge ends ensure $0\%$ oxygen ingress.

## 4. Open-Source CAD Manifest
*   `tlud_outer_jacket.dxf`: Sheet metal CNC plasma/laser cutting files for the outer drum air-intake dampers.
*   `inner_retort_flange.step`: High-temperature silicone/graphite gasket seating ring for the inner drum.
*   `syngas_recirculation_manifold.step`: Bottom pipe assembly to route volatile gases directly back into the fire zone.

## 5. Bill of Materials (BOM) - V1.0 Node
| Item | Description | Material Spec | Qty |
|---|---|---|---|
| M3-01 | Outer Jacket | 55-Gal Carbon Steel Drum (Clean, unlined) | 1 |
| M3-02 | Inner Retort | 30-Gal Carbon Steel Drum (With locking lid) | 1 |
| M3-03 | Chimney Tube | Galvanized Steel ($100\text{mm}$ OD, $1\text{m}$ length) | 1 |
| M3-04 | Lid Gasket | Ceramic / Fiberglass Rope ($800^\circ\text{C}$ rated) | 1 |
| M3-05 | Heavy Duty Clamp | Steel Drum Clamp Ring | 1 |

## 6. Assembly & Operation Routing
1. Fill the 30-gal inner drum with dried biomass (from Module 4). Seal it tightly.
2. Place it inside the 55-gal drum on refractory bricks. Pack scrap wood in the gap between the two drums. 
3. Light the scrap wood from the *top*. As the inner drum heats, it releases syngas out the bottom holes, which rises and feeds the fire cleanly.
4. **Quenching:** Once smoke turns clear/blue, block all air intakes and the chimney with wet clay or steel caps. Let cool for 24 hours to preserve the PAC structure.

```

---

### 📂 File Path: `04_FIRE_Biorefinery/hardware/MECHANICAL_PLAN.md`

```markdown
# 🔥 MECHANICAL PLAN: Module IV - FIRE
**Designation:** Subcritical HTL Autoclave & Z-Scheme Fermenter  
**Version:** 1.0.0 | **License:** CERN-OHL-S

> ⚠️ **CRITICAL SAFETY WARNING:** THIS MODULE OPERATES AT EXTREME PRESSURES ($10-25 \text{ MPa}$ / $150-350 \text{ PSI}$). MECHANICAL FAILURE WILL RESULT IN A LETHAL BLEVE EXPLOSION. USE ONLY CERTIFIED COMPONENTS.

## 1. System Objective
Direct conversion of wet algal waste into high-density bio-crude (via Subcritical HTL) without latent heat drying penalties, and conversion of unused $CO_2$ into Ethanol/Butanol (via photocatalytic microbial fermentation).

## 2. Mechanical Architecture (HTL Micro-Autoclave - Hacker Scale)
*   **Reactor Body:** $500\text{mL}$ Sample Cylinder. Made of Grade 316L Stainless Steel or Inconel 625. Must be hydro-tested to $>300 \text{ bar}$.
*   **High-Pressure Sealing:** Standard O-rings will melt at $350^\circ\text{C}$. Use metallic C-rings (Silver-plated Inconel) or high-density Graphite gaskets.
*   **The Safety Manifold (MANDATORY):** A top-mounted SS-316 cross fitting holding:
    1.  *Rupture Disk (Burst Disk):* Calibrated to fail mechanically at $250 \text{ bar}$.
    2.  *Pressure Relief Valve (PRV):* Set to vent at $220 \text{ bar}$.
    3.  *Routing:* The PRV exhaust MUST be piped into a secondary steel catch-can to contain boiling bio-crude in the event of over-pressurization.
*   **Heating:** A fluidized sand bath heated by a $2000\text{W}$ electric coil, controlled by a PID relay. Sand ensures uniform heat distribution and prevents localized metal warping.

## 3. Mechanical Architecture (Z-Scheme Fermentation - Hacker Scale)
*   **Solar Gas Reactor:** A flat-panel borosilicate glass array coated internally with the $Ag/WO_3$ catalyst. $CO_2$ is pumped through this array under direct sunlight to produce CO.
*   **The CSTR (Continuous Stirred-Tank Reactor):** A sealed $20\text{L}$ HDPE carboy holding the *Clostridium* culture. 
*   **Agitation & Sparging:** A magnetically coupled top-mounted impeller (no physical drive shaft pierces the lid, ensuring strict anaerobic seals). A sintered stainless steel sparging ring at the bottom distributes the CO gas.

## 4. Industrial Scale-Up (Continuous PFR & CSTR)
*   **HTL Plug-Flow Reactor (PFR):** Constructed from concentric Inconel 625 tubing. High-pressure positive displacement diaphragm pumps push the algal slurry at $250 \text{ bar}$.
*   **Heat Recovery (The Economizer):** The outgoing $350^\circ\text{C}$ biocrude transfers its sensible heat counter-currently to the incoming $25^\circ\text{C}$ wet algal slurry, recovering $>85\%$ of the thermal energy to maintain a systemic EROI $> 3.5$.
*   **Gas Fermentation:** $100,000\text{L}$ 316L Stainless Steel CSTR. In-line membrane pervaporation continuously extracts the bio-alcohols as they are produced.

## 5. Open-Source CAD & P&ID Manifest
*   `htl_piping_and_instrumentation.pdf`: The P&ID showing the exact routing of valves, thermocouples, and burst disks.
*   `cstr_magnetic_impeller.step`: 3D-printable (Nylon/PTFE) Rushton turbine designed to house neodymium magnets for external magnetic drive coupling.
*   `diy_glovebox_chassis.dxf`: Laser-cut acrylic panels to build the anaerobic isolation chamber needed to handle the *Clostridium* bacteria safely.

## 6. Bill of Materials (BOM) - V1.0 Node (HTL Only)
| Item | Description | Material Spec | Qty |
|---|---|---|---|
| M4-01 | Sample Cylinder | 316L SS ($300 \text{ bar}$ rated, $500\text{mL}$) | 1 |
| M4-02 | High-Pressure Cross Fitting | 316L SS Swagelok/Parker | 1 |
| M4-03 | Rupture Disk | SS / Inconel ($250 \text{ bar}$ fail limit) | 1 |
| M4-04 | Pressure Relief Valve | 316L SS ($220 \text{ bar}$ release limit) | 1 |
| M4-05 | PID Temp Controller | REX-C100 + K-Type Thermocouple | 1 |

## 7. P&ID Routing (HTL Phase)
1. **Loading:** Load the 316L cylinder to an absolute **MAXIMUM of 60% capacity** with wet algal paste. Seal valves tightly.
2. **Heating:** Submerge in the sand bath. Use the PID controller to ramp temp to $320^\circ\text{C}$. Hold for 30 minutes. 
3. **Cooling:** Turn off heat. **Wait until the cylinder is completely at room temperature ($<30^\circ\text{C}$)** before opening the valve to vent residual gases. 
4. **Separation:** Decant the heavy bio-crude. The Aqueous phase (rich in N/P) is pumped back to **Module 2 (WATER)**. Solid hydrochar is sent to **Module 3 (TERRE)**.

