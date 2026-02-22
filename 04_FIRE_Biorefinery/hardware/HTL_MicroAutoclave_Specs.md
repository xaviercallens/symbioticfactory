# 🔥 Subcritical HTL Micro-Autoclave Specifications
**Module IV (FIRE) Hardware Guide v1.0**

This document specifies the construction of the micro-autoclave required to perform **Subcritical Hydrothermal Liquefaction (HTL)**.
HTL is deployed to extract bio-crude oil directly from wet algal sludge (up to $85\%$ moisture content). By keeping the water in a subcritical liquid state at $300^\circ\text{C}$, we dramatically lower its dielectric constant, turning it into an organic solvent that depolymerizes the biomass without suffering the catastrophic thermodynamic penalty of boiling the water away.

## ⚠️ LETHAL PRESSURE WARNING (BLEVE)
* Water heated to $300^\circ\text{C}$ in a sealed container generates internal vapor pressures exceeding **$150\text{ bar}$ ($2100\text{ PSI}$)**.
* **DO NOT** attempt to build this out of standard hardware store plumbing (e.g., cast iron, brass, or standard PVC/CPVC). They will violently rupture, causing a Boiling Liquid Expanding Vapor Explosion (BLEVE) which is instantly lethal.
* **Only use** authentic Grade 316L Stainless Steel or Inconel instrumentation fittings (Swagelok, Parker, or equivalent) rated for at least $3000\text{ PSI}$ at elevated temperatures.

---

## 🛠️ The Bill of Materials (BOM)

To build a $100\text{mL}$ batch reactor, you will need the following Swagelok (or equivalent) components:

1. **The Core Cylinder:** 
   - $1 \times$ Swagelok $100\text{mL}$ Double-Ended Sample Cylinder, 316L SS, 1/4" Female NPT (Part No. `SS-4CS-TW-100`). Rated to $1800\text{ PSI}$ working pressure (sufficient, but bursting pressure is $>7000\text{ PSI}$). For higher safety margins at $350^\circ\text{C}$, up-rate to the Heavy-Wall cylinder (`SS-4FCS-100`).
2. **The Bottom Seal:** 
   - $1 \times$ Swagelok 1/4" Male NPT Hex Plug, 316 SS (Part No. `SS-4-P`).
3. **The Top Assembly (Valve & Safety):**
   - $1 \times$ Swagelok 316 SS Instrumentation Cross, 1/4" Male NPT (Part No. `SS-4-CS`).
   - $1 \times$ Swagelok Severe-Service Needle Valve, 316 SS, 1/4" Female NPT (Part No. `SS-1RS4`). This acts as your gas-purge and sampling valve.
   - $1 \times$ **CRITICAL:** Swagelok Rupture Disc Assembly, 1/4" NPT, set to rupture at $2800\text{ PSI}$ (Part No. `SS-RVM4-2800`).
   - $1 \times$ Analog or Digital Pressure Transducer (rated to $3000\text{ PSI}$), 1/4" NPT.
4. **Sealing:** Silver Goop™ (High-temp anti-seize) or high-density PTFE tape (only rated to $260^\circ\text{C}$, use liquid sealants designed for extreme heat if operating $\geq 300^\circ\text{C}$).

---

## 🏗️ Assembly & Thermal Heating Matrix

### Step 1: Vessel Assembly
1. Apply extreme-temperature thread sealant to the 1/4" Male NPT Hex Plug. Thread it into the bottom of the cylinder. Torque it to the manufacturer's specification (usually around $25\text{ ft-lbs}$ for 1/4" NPT).
2. Apply sealant to the bottom thread of the Cross fitting and install it into the top of the cylinder.
3. Install the Needle Valve, the Rupture Disc, and the Pressure Transducer into the remaining three ports of the top Cross.
4. **Safety Verification:** Ensure the Rupture disk exhaust port is pointing *away* from any area where a human operator might stand.

### Step 2: The Thermal Sand-Bath Matrix
**Do not apply a direct propane/acetylene flame to the cylinder.** localized "hot spots" weaken the steel and can cause catastrophic rupture.

1. Obtain a heavy steel crucible or a larger section of thick-walled steel pipe capped at one end.
2. Fill the crucible with fine-grain Alumina ($Al_2O_3$) sand or standard clean silica playground sand.
3. Bury the assembled HTL cylinder in the sand, leaving only the top Cross assembly and gauge exposed. 
4. Place the crucible on a high-temperature industrial electric hot plate or a regulated propane burner. The sand acts as a thermal mass, evenly distributing the $300^\circ\text{C}$ heat across the entire surface of the cylinder.

---

## ⚙️ Operating Procedures: The "60% Rule"

1. **Loading:** Open the top needle valve/cross. Pour in your wet algal biomass sludge.
   - **CRITICAL 60% RULE:** You MUST NOT fill the cylinder past 60% of its volume (e.g., max $60\text{mL}$ sludge in a $100\text{mL}$ cylinder). Subcritical water expands significantly as it approaches $300^\circ\text{C}$. In a $100\%$ full ("hydraulically locked") vessel, the expanding water will instantly exceed the bursting pressure of the steel, destroying the vessel.
2. **Purging:** Seal the vessel. Connect an inert gas line (Nitrogen or Argon) to the needle valve. Pressurize to $5\text{ bar}$, then vent. Repeat 3 times to completely purge oxygen (which would cause combustion, not liquefaction).
3. **The Cook:** Turn on the heat source under the sand bath. Heat the sand to $300^\circ\text{C}$.
4. Watch the pressure gauge. The pressure will rise autogenously as the water vaporizes to reach equilibrium. Hold at $300^\circ\text{C}$ for 30 to 60 minutes.
5. **Cooling:** Turn off the heat. Let the cylinder cool naturally in the sand. 
   - **DO NOT** quench the cylinder in cold water. Rapid thermal shock on stressed 316L SS can cause microfractures.
6. **Extraction:** Once the cylinder is fully cooled ($< 30^\circ\text{C}$), slowly crack the needle valve in a well-ventilated area to release any generated non-condensable gasses. Open the vessel and pour out your mixture of heavy bio-crude and aqueous phase nutrients!
