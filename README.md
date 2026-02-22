# 🌍 The Symbiotic Factory (OS-WEFC-v1.0)
**The Open-Source Hardware, Software, and Wetware Blueprint for Planetary Regeneration.**

[![License: CERN-OHL-S](https://img.shields.io/badge/License-CERN--OHL--S-blue.svg)](https://cern.ch/cern-ohl)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](.github/CONTRIBUTING.md)
[![Scale](https://img.shields.io/badge/Scale-Garage_to_Planet-orange.svg)]()

Welcome to the **Symbiotic Factory**. This repository contains the canonical, open-source engineering specifications to build a closed-loop, carbon-negative Water-Energy-Food-Carbon (WEFC) biorefinery. 

By mapping advanced thermodynamics, hydrodynamics, and synthetic biology to the four classical elements of nature—**SUN, WATER, TERRE (EARTH), and FIRE**—we interconnect a system where the waste of one module is the absolute required feedstock of the next.

Whether you are building a 50-liter prototype in a garage or designing a $500,000 \text{ m}^3$ industrial facility, the physics remain identical. **This is the blueprint to hack the planet back to health.**

---

## ⚙️ The Four-Element Architecture & Build Plans

### ☀️ [Module 1: SUN (Desalination & Freshwater Generation)](./01_SUN_Desalination)
**Goal:** Battery-free purification of seawater/brine/wastewater to generate ultra-pure $H_2O$ for the Aqua-Reactors using **Plasmonic Interfacial Solar Steam Generation (ISSG)**.
* **Mechanism:** We float a highly porous Polycyclic Aromatic Carbon (PAC) sponge on saltwater. Doped with Silver (Ag) nanoparticles, it triggers Localized Surface Plasmon Resonance (LSPR). Water is "nanoconfined" in the biochar capillaries, dropping the enthalpy of vaporization from $2256 \text{ kJ/kg}$ to $\approx 1250 \text{ kJ/kg}$, completely bypassing the energy penalty of Reverse Osmosis.

### 💧 [Module 2: WATER (Nano-Bubbling Algal Cycloreactors)](./02_WATER_Cycloreactor)
**Goal:** Hyper-productive $CO_2$ absorption using halotolerant microalgae (e.g., *Chlorella*, *Tetraselmis*), achieving yields $>400\text{x}$ greater than terrestrial forests.
* **Mechanism:** Bypassing low $CO_2$ solubility via Laplace pressure ($\Delta P = 2\gamma/r$) using 3D-printed Venturi nozzles. A helical stator induces a cyclonic vortex. An ESP32 pulses WS2812B LEDs (Red 680nm / Blue 450nm) at $10-50\text{ Hz}$ to cycle cells between light and dark zones rapidly, avoiding photoinhibition (the "flashing-light effect").

### 🌍 [Module 3: TERRE (Millennial-Scale PAC Biochar Synthesis)](./03_TERRE_Biochar)
**Goal:** Thermochemical stabilization of waste biomass into a permanent ($>1000$ year) pedological carbon sink that radically alters agricultural soil hydrology.
* **Mechanism:** Slow, anaerobic pyrolysis ($400-600^\circ\text{C}$) in a Top-Lit Updraft (TLUD) gasifier. Fuses carbon into a recalcitrant graphene-like matrix (O:C ratio $<0.2$). When deployed in soil, its extreme microporosity acts as a permanent sponge, altering the van Genuchten hydrology curve to retain the pure water from Module SUN directly at the root zone.

### 🔥 [Module 4: FIRE (HTL & Z-Scheme Fermentation)](./04_FIRE_Biorefinery)
**Goal:** Direct conversion of wet algal waste into biofuel via Subcritical Hydrothermal Liquefaction (HTL), and conversion of remaining $CO_2$ into Ethanol/Butanol via hybrid photocatalytic fermentation.
* **Mechanism 1 (HTL):** Bypasses the massive latent heat penalty of drying algae. At $300^\circ\text{C}$ and $10-25 \text{ MPa}$, water acts as an organic solvent, depolymerizing wet biomass directly into a $35-39 \text{ MJ/kg}$ heavy bio-crude.
* **Mechanism 2 (Z-Scheme Symbiosis):** Unused $CO_2$ enters a glass reactor coated with $Ag/WO_3$, reducing $CO_2$ to Carbon Monoxide (CO). The CO is pumped into an anaerobic bioreactor where extremophiles (*Clostridium autoethanogenum*) metabolize it via the Wood-Ljungdahl pathway into Ethanol/Butanol.

---

## 🔄 The Symbiotic Execution Loop (Quickstart)
To boot up the factory at a local node, execute this sequence:
1. **Initialize TERRE:** Pyrolyze local organic waste to create your first PAC biochar.
2. **Initialize SUN:** Synthesize the biochar into an ISSG sponge. Produce your first $10\text{L}$ of distilled water.
3. **Inoculate WATER:** Fill the Cycloreactor with the distilled water + nutrients. Inoculate algae. Activate the nano-bubbler and LED sequence. Wait 7 days.
4. **Ignite FIRE:** Harvest wet algal paste. Process via HTL to extract bio-crude. Feed leftover $CO_2$ through the $Ag/WO_3$ photocatalyst into the *Clostridium* bioreactor.
5. **Close the Loop:** Route solid hydrochar waste back to **TERRE**. Route N/P-rich aqueous wastewater back to **WATER**. The cycle is now autonomous.

---

## ⚠️ Critical Safety Warnings
**READ [SAFETY.md](./SAFETY.md) BEFORE ASSEMBLY.**
* **High Pressure (HTL):** Subcritical water operates at up to $250\text{ bar}$. Use strictly certified stainless steel pressure vessels with mechanical pressure relief valves (PRVs) and burst disks. **Failure to do so will result in a lethal BLEVE explosion.**
* **Toxic Gas (Fermentation):** The $Ag/WO_3$ reactor generates Carbon Monoxide (CO). Ensure rigorous seals, use a residential CO detector, and operate in a well-ventilated space.
