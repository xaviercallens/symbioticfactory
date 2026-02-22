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
