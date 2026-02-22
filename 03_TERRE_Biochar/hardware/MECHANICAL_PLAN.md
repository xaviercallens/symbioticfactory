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
