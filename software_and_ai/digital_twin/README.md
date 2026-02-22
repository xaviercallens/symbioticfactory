# 🖥️ Symbiotic Factory Digital Twin

**In-silico validation, multi-physics simulation, and Multidisciplinary Design Optimization (MDO) of the Symbiotic Factory using exclusively open-source, government-funded computational engines.**

## Architecture

The Digital Twin stitches together 7 open-source solvers to simulate every physical domain of the factory:

| Domain | Engine | Institution | Role |
|---|---|---|---|
| System Optimization | **OpenMDAO** | NASA Glenn | EROI Maximization via MDO |
| Process Flowsheet | **IDAES-PSE** | US DOE / NETL | Mass & Energy Balancing |
| Transient Dynamics | **OpenModelica** | EU / OSMC | PID tuning, cloud-cover response |
| Fluid Dynamics | **OpenFOAM** | Imperial College / EU | Nano-bubble CFD, vortex simulation |
| Chemical Kinetics | **Cantera** | Caltech / JPL | HTL thermodynamics, pyrolysis yields |
| Structural FEA | **Code_Aster** | EDF (France) | Pressure vessel BLEVE prevention |
| Biology | **COBRApy** | UCSD / NIH | Genome-scale metabolic flux analysis |
| Photonics | **MEEP** | MIT | LSPR nanoparticle optimization |

## Directory Structure

```
digital_twin/
├── requirements.txt              # Python dependencies
├── TODO.md                       # Implementation roadmap
├── run_digital_twin.py           # Master orchestration script
├── 00_Orchestrator/
│   ├── factory_mdo_model.py      # NASA OpenMDAO: system-level EROI optimization
│   └── idaes_master_flowsheet.py # DOE IDAES: mass & energy balance flowsheet
├── 01_SUN_Simulations/
│   └── lspr_nanoparticles.ctl    # MIT MEEP: plasmonic photon absorption FDTD
├── 02_WATER_Simulations/
│   └── openfoam_setup/           # OpenFOAM: nano-bubble CFD & vortex modeling
├── 03_TERRE_Simulations/
│   └── pyrolysis_kinetics.py     # Cantera: syngas yield & O:C ratio prediction
├── 04_FIRE_Simulations/
│   ├── htl_subcritical.py        # Cantera: subcritical water thermodynamics
│   ├── htl_autoclave_fea.comm    # Code_Aster: 250-bar pressure vessel FEA
│   └── heat_exchanger.dwxml      # DWSIM: thermal recovery optimization
└── 05_WETWARE_Simulations/
    ├── clostridium_flux.py       # COBRApy: Wood-Ljungdahl pathway FBA
    └── chlorella_flux.py         # COBRApy: algal photosynthetic yield FBA
```

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full Digital Twin
python run_digital_twin.py --mode full

# 3. Run a single module simulation
python run_digital_twin.py --module WATER

# 4. Generate the validation report
python run_digital_twin.py --report
```

## The Gate: EROI Validation

The Digital Twin enforces a hard thermodynamic gate:
- If the systemic **EROI > 3.5**, the design is approved for physical construction.
- If the systemic **EROI < 3.5**, the design is rejected and the optimizer suggests parameter adjustments.

This ensures no physical steel is bent or money spent until the physics are computationally proven.
