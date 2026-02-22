# 🖥️ Digital Twin Implementation TODO

**Objective:** Build a complete in-silico simulation of the Symbiotic Factory using open-source computational engines (NASA OpenMDAO, DOE IDAES, Caltech Cantera, MIT MEEP, COBRApy, OpenFOAM, Code_Aster) to validate thermodynamic feasibility and optimize the WEFC loop before physical construction.

---

## Phase 0: Infrastructure & Scaffolding
- [ ] Create `software_and_ai/digital_twin/` directory structure per the spec
- [ ] Create `requirements.txt` with all Python dependencies
- [ ] Create a master `README.md` explaining the Digital Twin architecture and how to run it
- [ ] Create `Makefile` or `run_twin.sh` script to orchestrate the full simulation pipeline

## Phase 1: The Macro-System Twin (Plant-Wide Optimization)
### 1A — NASA OpenMDAO Orchestrator
- [ ] `00_Orchestrator/factory_mdo_model.py`: Build the top-level Multidisciplinary Design Optimization (MDO) model
  - [ ] Define the 4 module `ExplicitComponent` classes (SUN, WATER, TERRE, FIRE)
  - [ ] Wire inter-module mass/energy connections (distillate flow, biomass flux, syngas yield, nutrient recycling)
  - [ ] Define the objective function: maximize systemic EROI (target $> 3.5$)
  - [ ] Define design variables: LED frequency, HTL temperature, pyrolysis hold time, membrane area
  - [ ] Add constraints: pressure limits, pH bounds, O:C ratio $< 0.2$
  - [ ] Implement `ScipyOptimizeDriver` for gradient-based optimization

### 1B — DOE IDAES Master Flowsheet
- [ ] `00_Orchestrator/idaes_master_flowsheet.py`: Process-level mass & energy balances
  - [ ] Model the SUN evaporator unit (enthalpy of vaporization drop via nanoconfinement)
  - [ ] Model the WATER reactor unit (gas-liquid mass transfer, $CO_2$ dissolution)
  - [ ] Model the FIRE HTL unit (subcritical phase equilibrium, bio-crude separation)
  - [ ] Model the TERRE pyrolyzer unit (solid-phase carbonization, syngas generation)
  - [ ] Model nutrient recycling loop (N/P from HTL aqueous phase back to WATER)
  - [ ] Model thermal recovery loop (HTL Economizer heat exchanger)
  - [ ] Run mass balance check: verify $0$ unaccounted mass streams
  - [ ] Run energy balance check: verify net-positive energy across the loop

### 1C — OpenModelica Transient Dynamics
- [ ] `00_Orchestrator/transient_control.mo`: Modelica model for dynamic state simulation
  - [ ] Simulate cloud-cover interruption on SUN module (thermal buffering response)
  - [ ] Simulate algal density spike in WATER module (PID pH response)
  - [ ] Simulate HTL pressure overshoot scenario (PRV actuation timing)
  - [ ] Validate ESP32 PID tuning parameters ($K_p$, $K_i$, $K_d$) against the dynamic model

## Phase 2: The Fluid Twin (Multiphase CFD)
### 2A — OpenFOAM: WATER Module Cycloreactor
- [ ] `02_WATER_Simulations/openfoam_setup/`: Full CFD case directory
  - [ ] Generate 3D mesh from `helical_stator.scad` (export STL → `snappyHexMesh`)
  - [ ] Configure `multiphaseEulerFoam` solver for gas-liquid $CO_2$ nano-bubble simulation
  - [ ] Set boundary conditions: tangential inlet velocity, $CO_2$ gas fraction, wall slip
  - [ ] Simulate Laplace pressure ($\Delta P = 2\gamma/r$) for bubble sizes $< 200\text{nm}$
  - [ ] Compute volumetric mass transfer coefficient ($k_La$)
  - [ ] Verify cyclonic vortex frequency matches the $10-50\text{ Hz}$ flashing-light requirement
  - [ ] Compute maximum wall shear stress to confirm algal cell integrity ($< 1\text{ Pa}$)

### 2B — OpenFOAM: SUN Module Capillary Wicking
- [ ] `01_SUN_Simulations/capillary_wicking.py`: Setup script
  - [ ] Model porous media flow through the PAC biochar matrix
  - [ ] Simulate boundary-layer evaporation gradients at the air-sponge interface
  - [ ] Validate capillary pumping rate matches evaporation rate (steady-state condition)

## Phase 3: The Reaction Twin (Chemical Kinetics)
### 3A — Cantera: FIRE Module HTL
- [ ] `04_FIRE_Simulations/htl_subcritical.py`: Subcritical water thermodynamics
  - [ ] Define custom `Solution` object for subcritical water ($T = 300^\circ\text{C}$, $P = 150\text{ bar}$)
  - [ ] Calculate dielectric constant shift ($\varepsilon_r \approx 80 \rightarrow 20$) at operating conditions
  - [ ] Implement Arrhenius depolymerization kinetics for wet algal biomass
  - [ ] Predict bio-crude Higher Heating Value (HHV) as a function of temperature and hold time
  - [ ] Generate phase diagram: optimal $T$-$P$ operating window for maximum yield

### 3B — Cantera: TERRE Module Pyrolysis
- [ ] `03_TERRE_Simulations/pyrolysis_kinetics.py`: Anaerobic pyrolysis simulation
  - [ ] Model syngas composition ($CO$, $H_2$, $CH_4$) as a function of pyrolysis temperature
  - [ ] Calculate O:C atomic ratio of the resulting biochar vs. temperature
  - [ ] Verify the self-sustaining thermal loop: does the syngas combustion energy exceed the endothermic pyrolysis requirement?
  - [ ] Determine minimum hold time at $500^\circ\text{C}$ to achieve O:C $< 0.2$

### 3C — DWSIM: Heat Exchanger Optimization
- [ ] `04_FIRE_Simulations/heat_exchanger.dwxml`: DWSIM flowsheet
  - [ ] Model the concentric tube-in-tube counter-current heat exchanger (The Economizer)
  - [ ] Calculate thermal recovery efficiency (target $> 85\%$)
  - [ ] Optimize tube length, flow rates, and insulation thickness

## Phase 4: The Hardware Twin (Mechanical FEA)
### 4A — Code_Aster / Salome-Meca: HTL Pressure Vessel
- [ ] `04_FIRE_Simulations/htl_autoclave_fea.comm`: FEA command file
  - [ ] Import 316L SS Sample Cylinder geometry (from `.STEP` file)
  - [ ] Define material properties: Young's Modulus, Poisson's Ratio, Yield Strength at $350^\circ\text{C}$
  - [ ] Apply boundary conditions: internal pressure $= 250\text{ bar}$, external temp $= 320^\circ\text{C}$
  - [ ] Run Von Mises stress analysis
  - [ ] Verify maximum stress $< 0.6 \times$ Yield Strength (Safety Factor $> 1.67$)
  - [ ] Simulate fatigue cycling: predict number of safe HTL batch cycles before replacement
  - [ ] Validate burst disk calibration: confirm mechanical failure at exactly $250\text{ bar}$

## Phase 5: The Wetware & Photon Twin (Biology & Optics)
### 5A — COBRApy: Metabolic Flux Analysis
- [ ] `05_WETWARE_Simulations/clostridium_flux.py`: *Clostridium autoethanogenum* model
  - [ ] Load the genome-scale metabolic model (GEM) for *C. autoethanogenum* (iCLAU786)
  - [ ] Set Carbon Monoxide (CO) uptake rate as the primary carbon source
  - [ ] Run Flux Balance Analysis (FBA) to predict Ethanol/Butanol yield per mol CO
  - [ ] Sensitivity analysis: how does pH (5.8 vs 6.4) affect the Ethanol:Butanol ratio?
- [ ] `05_WETWARE_Simulations/chlorella_flux.py`: *Chlorella vulgaris* model
  - [ ] Load the GEM for *C. vulgaris* (iCZ843)
  - [ ] Set $CO_2$ uptake and photon flux as inputs
  - [ ] Run FBA to predict maximum biomass yield ($\text{g/L/day}$)
  - [ ] Cross-validate with the LED frequency from the ESP32 firmware

### 5B — MIT MEEP: Plasmonic & Photocatalytic Optics
- [ ] `01_SUN_Simulations/lspr_nanoparticles.ctl`: MEEP FDTD simulation
  - [ ] Define Silver (Ag) nanoparticle geometry (spherical, $d = 20-80\text{nm}$)
  - [ ] Simulate LSPR absorption spectrum under AM1.5G solar irradiance
  - [ ] Sweep nanoparticle diameter to find the peak photothermal absorption efficiency
  - [ ] Output optimal Ag nanoparticle diameter for maximum broadband absorption
- [ ] `04_FIRE_Simulations/wo3_photocatalyst.ctl`: MEEP simulation for $Ag/WO_3$
  - [ ] Define $WO_3$ semiconductor lattice with Ag nanoparticle decoration
  - [ ] Simulate photon absorption and electron-hole pair generation under UV/Vis
  - [ ] Validate Z-scheme electron transfer pathway

## Phase 6: Integration & CI/CD
- [ ] Create `run_digital_twin.py`: Master orchestration script
  - [ ] Sequential execution: MEEP → OpenFOAM → Cantera → COBRApy → IDAES → OpenMDAO
  - [ ] Parallel execution mode for independent module simulations
  - [ ] Generate a unified `SIMULATION_REPORT.md` with all results, plots, and EROI score
- [ ] Create `.github/workflows/digital_twin_ci.yml`: GitHub Actions CI pipeline
  - [ ] On every PR touching `hardware/` or `wetware_chemistry/`: run the relevant simulation subset
  - [ ] Gate merging on EROI $> 3.5$ (the Digital Twin "approves" or "rejects" the design change)
- [ ] Create `Dockerfile` for reproducible simulation environment
  - [ ] Base image: Ubuntu 22.04
  - [ ] Install: Python 3.11, OpenMDAO, IDAES, Cantera, COBRApy, MEEP, OpenFOAM, Code_Aster
  - [ ] Pre-cache all genome-scale metabolic models (GEMs)
  - [ ] Expose Jupyter Lab port for interactive exploration

## Phase 7: Validation & Documentation
- [ ] Run the complete Digital Twin end-to-end
- [ ] Generate the `SIMULATION_REPORT.md` with:
  - [ ] Predicted EROI score
  - [ ] Optimal operating parameters for each module
  - [ ] Stress analysis pass/fail for the HTL vessel
  - [ ] Predicted bio-crude yield ($\text{MJ/kg}$)
  - [ ] Predicted Ethanol yield ($\text{mol/mol CO}$)
  - [ ] Predicted PAC O:C ratio
- [ ] Cross-validate simulation predictions against published experimental literature
- [ ] Update the master `SCALING_AND_TESTING_GUIDE.md` with simulation-derived optimal setpoints
- [ ] Push all simulation code and results to GitHub
