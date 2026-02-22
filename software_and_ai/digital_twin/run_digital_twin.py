"""
Symbiotic Factory — Digital Twin Master Orchestrator
=====================================================
Runs all simulation phases sequentially and generates a unified report.
Usage: python run_digital_twin.py [--module SUN|WATER|TERRE|FIRE|ALL]
"""

import sys
import os
import importlib.util
from pathlib import Path

TWIN_DIR = Path(__file__).parent

def load_and_run(module_path, func_name):
    """Dynamically load a Python module and run a function."""
    spec = importlib.util.spec_from_file_location("mod", module_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return getattr(mod, func_name)()
    except Exception as e:
        print(f"  ⚠️  Skipped {module_path.name}: {e}")
        return None

def main():
    module_filter = sys.argv[2].upper() if len(sys.argv) > 2 else 'ALL'
    
    print("\n" + "█"*70)
    print("  🏭  SYMBIOTIC FACTORY — DIGITAL TWIN ORCHESTRATOR  🏭")
    print("  In-silico validation of the WEFC Biorefinery")
    print("█"*70 + "\n")

    results = {}

    # Phase 3A: HTL Thermodynamics
    if module_filter in ('ALL', 'FIRE'):
        print("\n▶ Phase 3A: FIRE — HTL Subcritical Thermodynamics (Cantera)")
        htl_script = TWIN_DIR / "04_FIRE_Simulations" / "htl_subcritical.py"
        if htl_script.exists():
            results['htl'] = load_and_run(htl_script, 'run_htl_simulation')

    # Phase 3B: Pyrolysis Kinetics
    if module_filter in ('ALL', 'TERRE'):
        print("\n▶ Phase 3B: TERRE — Pyrolysis Kinetics (Cantera)")
        pyro_script = TWIN_DIR / "03_TERRE_Simulations" / "pyrolysis_kinetics.py"
        if pyro_script.exists():
            results['pyrolysis'] = load_and_run(pyro_script, 'run_pyrolysis_simulation')

    # Phase 5A: Clostridium Metabolic FBA
    if module_filter in ('ALL', 'FIRE'):
        print("\n▶ Phase 5A: WETWARE — Clostridium Metabolic FBA (COBRApy)")
        cobra_script = TWIN_DIR / "05_WETWARE_Simulations" / "clostridium_flux.py"
        if cobra_script.exists():
            results['clostridium'] = load_and_run(cobra_script, 'run_simulation')

    # Phase 1: System-Level MDO (requires OpenMDAO)
    if module_filter == 'ALL':
        print("\n▶ Phase 1: SYSTEM — NASA OpenMDAO MDO Optimization")
        mdo_script = TWIN_DIR / "00_Orchestrator" / "factory_mdo_model.py"
        if mdo_script.exists():
            results['mdo'] = load_and_run(mdo_script, 'build_and_run')

    print("\n" + "█"*70)
    print("  ✅  DIGITAL TWIN RUN COMPLETE")
    print("█"*70 + "\n")
    return results

if __name__ == '__main__':
    main()
