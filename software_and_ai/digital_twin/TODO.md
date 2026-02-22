# 🖥️ Digital Twin Implementation TODO

**Objective:** Build a complete in-silico simulation of the Symbiotic Factory using open-source computational engines to validate thermodynamic feasibility and optimize the WEFC loop before physical construction.

---

## Phase 0: Infrastructure & Scaffolding
- [x] Create `software_and_ai/digital_twin/` directory structure per the spec
- [x] Create `requirements.txt` with all Python dependencies
- [x] Create a master `README.md` explaining the Digital Twin architecture
- [x] Create `run_digital_twin.py` master orchestration script

## Phase 1: The Macro-System Twin (Plant-Wide Optimization)
### 1A — NASA OpenMDAO Orchestrator
- [x] `00_Orchestrator/factory_mdo_model.py`: 4-module MDO with EROI objective

### 1B — DOE IDAES Master Flowsheet
- [x] `00_Orchestrator/idaes_master_flowsheet.py`: Complete mass & energy balance with N/P recycling

### 1C — OpenModelica Transient Dynamics
- [ ] `00_Orchestrator/transient_control.mo`: Modelica model for dynamic state simulation

## Phase 2: The Fluid Twin (Multiphase CFD)
### 2A — OpenFOAM: WATER Module Cycloreactor
- [x] `02_WATER_Simulations/openfoam_setup/system/controlDict`: multiphaseEulerFoam config
- [x] `02_WATER_Simulations/openfoam_setup/run_cfd.sh`: Mesh generation & solver pipeline

### 2B — OpenFOAM: SUN Module Capillary Wicking
- [ ] `01_SUN_Simulations/capillary_wicking.py`: Porous media flow setup

## Phase 3: The Reaction Twin (Chemical Kinetics)
### 3A — Cantera: FIRE Module HTL
- [x] `04_FIRE_Simulations/htl_subcritical.py`: Dielectric, Arrhenius, HHV prediction

### 3B — Cantera: TERRE Module Pyrolysis
- [x] `03_TERRE_Simulations/pyrolysis_kinetics.py`: Syngas, O:C ratio, self-sustainability

### 3C — DWSIM: Heat Exchanger
- [ ] `04_FIRE_Simulations/heat_exchanger.dwxml`: Counter-current economizer model

## Phase 4: The Hardware Twin (Mechanical FEA)
### 4A — Code_Aster: HTL Pressure Vessel
- [x] `04_FIRE_Simulations/htl_autoclave_fea.comm`: 250-bar Von Mises + fatigue analysis

## Phase 5: The Wetware & Photon Twin (Biology & Optics)
### 5A — COBRApy: Metabolic Flux Analysis
- [x] `05_WETWARE_Simulations/clostridium_flux.py`: Wood-Ljungdahl pH-dependent FBA
- [x] `05_WETWARE_Simulations/chlorella_flux.py`: Photosynthetic yield & LED frequency validation

### 5B — MIT MEEP: Plasmonic & Photocatalytic Optics
- [x] `01_SUN_Simulations/lspr_nanoparticles.ctl`: Ag nanoparticle FDTD absorption simulation
- [ ] `04_FIRE_Simulations/wo3_photocatalyst.ctl`: WO3 Z-scheme photon absorption

## Phase 6: Integration & CI/CD
- [x] `run_digital_twin.py`: Master orchestration script
- [x] `.github/workflows/digital_twin_ci.yml`: GitHub Actions CI pipeline
- [x] `Dockerfile`: Reproducible simulation environment

## Phase 7: Validation & Documentation
- [ ] Run the complete Digital Twin end-to-end
- [ ] Generate `SIMULATION_REPORT.md` with all results
- [ ] Cross-validate against published experimental literature
- [ ] Update `SCALING_AND_TESTING_GUIDE.md` with simulation-derived optimal setpoints
