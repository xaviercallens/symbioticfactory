# 🌱 Soil Science: Biochar-Amended Pedological Hydrology

**Module III (TERRE) — Soil Science Data & Protocols**  
**Version:** 1.0.0 | **License:** CERN-OHL-S

## Overview

The ultimate destination for the Polycyclic Aromatic Carbon (PAC) biochar produced by the TERRE module is **agricultural soil**. When deployed into the pedosphere, the biochar's extreme microporosity ($>400\text{ m}^2/\text{g}$ BET surface area) fundamentally alters the soil's hydraulic properties, nutrient retention capacity, and microbial ecology.

This document provides the key equations, reference data, and measurement protocols needed to quantify these effects.

---

## 1. van Genuchten Water Retention Model

The van Genuchten equation describes the soil water retention curve (SWRC), relating volumetric water content ($\theta$) to matric suction ($\psi$):

$$\theta(\psi) = \theta_r + \frac{\theta_s - \theta_r}{[1 + (\alpha \psi)^n]^m}$$

where:
- $\theta_s$: Saturated water content (porosity)
- $\theta_r$: Residual water content
- $\alpha$: Inverse of air-entry pressure ($\text{cm}^{-1}$)
- $n$: Pore-size distribution parameter
- $m = 1 - 1/n$

### Biochar Amendment Effect on vG Parameters

Based on literature meta-analysis (Omondi et al., 2016; Blanco-Canqui, 2017):

| Parameter | Sandy Soil (Control) | Sandy Soil + 5% Biochar | Clay Soil (Control) | Clay Soil + 5% Biochar |
|---|---|---|---|---|
| $\theta_s$ | 0.38 | **0.44** (+16%) | 0.48 | **0.50** (+4%) |
| $\theta_r$ | 0.04 | 0.06 | 0.10 | 0.11 |
| $\alpha$ ($\text{cm}^{-1}$) | 0.035 | 0.028 | 0.008 | 0.007 |
| $n$ | 3.18 | 2.45 | 1.25 | 1.30 |
| Plant Available Water | 0.10 | **0.16** (+60%) | 0.18 | **0.20** (+11%) |

> **Key Insight:** Biochar has the greatest impact on **sandy soils**, increasing plant-available water by up to 60%. The micropores act as permanent reservoirs that hold water against gravity at the root zone.

---

## 2. Langmuir Adsorption Isotherm: Nutrient Retention

Biochar's surface chemistry allows it to adsorb and slowly release Nitrogen and Phosphorus ions, acting as a slow-release fertilizer battery. The Langmuir isotherm models this:

$$q_e = \frac{q_{max} \cdot K_L \cdot C_e}{1 + K_L \cdot C_e}$$

where:
- $q_e$: Amount of nutrient adsorbed per gram biochar ($\text{mg/g}$)
- $q_{max}$: Maximum adsorption capacity ($\text{mg/g}$)
- $K_L$: Langmuir constant (binding affinity, $\text{L/mg}$)
- $C_e$: Equilibrium concentration in solution ($\text{mg/L}$)

### Reference Adsorption Capacities (PAC Biochar at 500°C)

| Nutrient | $q_{max}$ (mg/g) | $K_L$ (L/mg) | Source |
|---|---|---|---|
| $NH_4^+$ (Ammonium) | 12.5 | 0.085 | Yao et al., 2012 |
| $NO_3^-$ (Nitrate) | 1.5 | 0.012 | Kameyama et al., 2012 |
| $PO_4^{3-}$ (Phosphate) | 8.7 | 0.145 | Yao et al., 2012 |
| $K^+$ (Potassium) | 15.2 | 0.068 | Hale et al., 2013 |

> **Key Insight:** The biochar acts as a closed-loop nutrient buffer. The N/P-rich aqueous wastewater from the FIRE module's HTL process is not wasted — it is adsorbed onto the biochar and slowly released to plant roots over months.

---

## 3. Measurement Protocols

### 3.1 BET Surface Area (Biochar Quality Check)

The Brunauer-Emmett-Teller (BET) method measures the total microporous surface area of the biochar. Target: **$> 300 \text{ m}^2/\text{g}$**.

**DIY Proxy (Without BET Equipment):**
- Weigh $10\text{g}$ of crushed biochar.
- Add to $100\text{mL}$ of methylene blue dye solution ($100\text{ mg/L}$).
- Shake for 24 hours. Filter.
- Measure remaining dye concentration with a colorimeter or UV-Vis.
- Higher dye removal = higher surface area.

### 3.2 O:C Ratio (Recalcitrance Quality Check)

The Oxygen-to-Carbon atomic ratio determines the millennial stability of the biochar:

| O:C Ratio | Estimated Half-Life | Status |
|---|---|---|
| $< 0.2$ | $> 1000$ years | ✅ Recalcitrant PAC |
| $0.2 - 0.6$ | $100 - 1000$ years | ⚠️ Semi-stable |
| $> 0.6$ | $< 100$ years | ❌ Will decompose |

**Measurement:** Requires elemental analysis (CHN analyzer) or can be estimated via the Digital Twin's `pyrolysis_kinetics.py` simulation.

### 3.3 pH & CEC (Cation Exchange Capacity)

- Biochar typically has pH $8 - 10$ (alkaline). It is ideal for **acidic soils** but should be applied cautiously on already-alkaline soils.
- CEC target: $> 20\text{ cmol/kg}$ (indicates strong nutrient retention).

---

## 4. Application Guidelines

| Soil Type | Recommended Biochar Rate | Expected Water Retention Improvement |
|---|---|---|
| Sandy | $20 - 50 \text{ t/ha}$ (2-5% by weight) | +40-60% |
| Loamy | $10 - 30 \text{ t/ha}$ | +15-30% |
| Clay | $5 - 15 \text{ t/ha}$ | +5-15% |
| Degraded/Arid | $50 - 100 \text{ t/ha}$ | +60-100% |

**Critical:** Always **charge** the biochar with nutrients before soil application. Mix the raw biochar with compost, liquid fertilizer, or the N/P-rich HTL aqueous phase for 48 hours before tilling into soil. Un-charged biochar will temporarily rob nutrients from the soil as it reaches adsorption equilibrium.
