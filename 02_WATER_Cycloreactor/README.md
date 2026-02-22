# 💧 Module II: WATER (Nano-Bubbling Algal Cycloreactors)

**Objective:** Hyper-productive $CO_2$ absorption utilizing microalgal Carbon Concentrating Mechanisms (CCM).

To achieve volumetric carbon fixation rates orders of magnitude higher than terrestrial plants, this module relies on specific hydrodynamic hardware designed to bypass the physical bottlenecks of $CO_2$ solubility and photoinhibition. The required geometry cannot be purchased natively at a hardware store; it must be 3D printed.

## Hardware Components (CAD)

In the `hardware/` directory, you will find parametric 3D models written in **OpenSCAD**. By using OpenSCAD, you can open the `.scad` files, adjust the variables at the top of the file to match your local PVC pipe / acrylic tube diameters, and instantly generate a `.stl` file specifically for your build.

### 1. Venturi Nano-Bubbler (`venturi_nano_bubbler.scad`)
The absolute engineering bottleneck in algal cultivation is the low aqueous solubility of $CO_2$. 
This nozzle mathematically drops fluid pressure at the throat while drawing in a $CO_2$ air mix. The high-velocity shear forces the gas into **nano-bubbles**. Their extreme internal pressure ($\Delta P = 2\gamma/r$) according to Laplace's Law forces near-total gas dissolution into the liquid phase.

### 2. Helical Cyclonic Stator (`helical_stator.scad`)
Standard photobioreactors suffer from photoinhibition at the illuminated perimeter and light-starvation in the dark center.
This static baffle slides directly inside your vertical reactor tube. As water is pumped upwards, the helical fins induce a cyclonic vortex. This guarantees cells rapidly cycle between light and dark zones (the *flashing-light effect*), allowing you to bypass the photoinhibition rate constant entirely.
*Note: The script includes an interlocking peg-and-socket design so you can print multiple segments and stack them to fill tall reactor columns.*

---

## 🖨️ 3D Printing Instructions & Material Requirements

⚠️ **CRITICAL: DO NOT USE PLA** ⚠️
PLA (Polylactic Acid) is totally unsuitable for aquatic reactors. It hydrolyzes, becomes brittle, and dissolves back into lactic acid over time, ruining your pH and destroying the reactor internals.

**Recommended Materials:**
* **PETG (Polyethylene Terephthalate Glycol):** Excellent chemical resistance to water and weak acids/bases. Easy to print.
* **Polycarbonate (PC) / ASA:** Ideal for industrial UV resistance if you are building the reactor outdoors in direct sunlight.

**Recommended Print Settings:**
* **Infill:** 100% (Solid). Water under pressure will seep through any internal infill void geometries.
* **Perimeters/Walls:** Minimum 4 to 6 walls.
* **Layer Height:** $0.16\text{ mm} - 0.20\text{ mm}$ (Smaller layers help ensure watertight seals on angled pressure nozzles). 

## How to generate your STLs

1. Download [OpenSCAD](https://openscad.org/downloads.html).
2. Open `hardware/venturi_nano_bubbler.scad` or `hardware/helical_stator.scad`.
3. Modify the variables under the `// --- Core Parameters ---` header (e.g., set `reactor_inner_diameter = 90.0` to match your specific tube size).
4. Press `F5` to Preview.
5. Press `F6` to Render (this takes longer as it computes the final solid).
6. Click **File > Export > Export as STL**.
7. Slice and print!
