# 🔥 Module IV: FIRE (Subcritical HTL & Photocatalytic Fermentation)

**Objective:** Direct conversion of wet algal waste into high-density drop-in biofuel without the massive thermodynamic penalty of drying, alongside the synthesis of extreme-efficiency bio-alcohols.

Standard biofuel extraction requires boiling off the 85% water content of harvested algae. This invokes the latent heat of vaporization penalty, utterly destroying the Energy Return on Investment (EROI). This module utilizes thermodynamic hacks to keep the water liquid while simultaneously altering its dielectric constant to act as an organic solvent. 

## The Hardware: Solid Stream Processing (HTL) 🛠️

The FIRE module actually operates in two strictly separated streams to maximize carbon capture. 

**Stream 1 (The Solid/Lipid Stream):** Wet algae is crushed under immense pressure ($\approx 150\text{ bar}$) and heat ($300^\circ\text{C}$) in a process known as Subcritical Hydrothermal Liquefaction (HTL). By holding the water in a subcritical phase, its dielectric constant drops from $\varepsilon_r \approx 80$ to $\varepsilon_r \approx 20$. The water begins acting like a non-polar solvent (e.g., acetone or benzene), causing the long-chain algal biopolymers to instantly depolymerize into a heavy, energy-dense bio-crude.

### 👉 [Click here for the HTL Micro-Autoclave Specs & Assembly Guide](hardware/HTL_MicroAutoclave_Specs.md)
*⚠️ WARNING: HTL generates lethal internal pressures. This guide details the strict Swagelok/Parker instrumentation Grade 316L Stainless Steel requirements and the mandatory pressure-relief safety implementations needed to prevent thermal explosions. Standard plumbing equipment will violently rupture under these conditions.*

## The Wetware: Gas Stream Processing (Z-Scheme Symbiosis) 🧪

**Stream 2 (The Gas Stream):** The WATER module isn't 100% efficient. Unused $CO_2$ that bubbles out of the top of the cycloreactors is routed into a specialized glass jar coated in a **synthesized $Ag/WO_3$ Z-Scheme Photocatalyst**. Under sunlight, this catalyst strips oxygen from the $CO_2$, converting it into **Carbon Monoxide (CO)**. This CO is bubbled into a dark fermentation tank where extremophile bacteria (*Clostridium autoethanogenum*) ingest the toxic gas and excrete pure Ethanol or Butanol via the Wood-Ljungdahl metabolic pathway.

### 👉 [Click here for the Z-Scheme Photocatalyst Synthesis Protocol](wetware_chemistry/Z_Scheme_Photocatalyst_Synthesis.md)

This detailed protocol covers exactly how to synthesize the $Ag/WO_3$ catalytic powder at home using basic precursor chemicals, and how to "paint" it onto the interior of a glass reactor to bridge the gap between your physical systems and biological extremophiles.
