"""
Symbiotic Factory — Digital Twin Master Orchestrator
=====================================================
Runs all simulation phases sequentially and generates a unified report.
Usage: python run_digital_twin.py [--module SUN|WATER|TERRE|FIRE|ALL]
"""

import sys
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


SIMULATIONS = [
    ("Phase 3A: FIRE — HTL Subcritical Thermodynamics",
     "04_FIRE_Simulations/htl_subcritical.py", "run_htl_simulation", ["ALL", "FIRE"]),
    ("Phase 3B: TERRE — Pyrolysis Kinetics",
     "03_TERRE_Simulations/pyrolysis_kinetics.py", "run_pyrolysis_simulation", ["ALL", "TERRE"]),
    ("Phase 5A: WETWARE — Clostridium Metabolic FBA",
     "05_WETWARE_Simulations/clostridium_flux.py", "run_simulation", ["ALL", "FIRE"]),
    ("Phase 5A: WETWARE — Chlorella Photosynthetic FBA",
     "05_WETWARE_Simulations/chlorella_flux.py", "run_simulation", ["ALL", "WATER"]),
    ("Phase 1B: SYSTEM — IDAES Mass & Energy Flowsheet",
     "00_Orchestrator/idaes_master_flowsheet.py", "run_master_flowsheet", ["ALL"]),
    ("Phase 1A: SYSTEM — NASA OpenMDAO MDO Optimization",
     "00_Orchestrator/factory_mdo_model.py", "build_and_run", ["ALL"]),
]


def main():
    module_filter = "ALL"
    for i, arg in enumerate(sys.argv):
        if arg == "--module" and i + 1 < len(sys.argv):
            module_filter = sys.argv[i + 1].upper()

    print("\n" + "█" * 70)
    print("  🏭  SYMBIOTIC FACTORY — DIGITAL TWIN ORCHESTRATOR  🏭")
    print("  In-silico validation of the WEFC Biorefinery")
    print("█" * 70 + "\n")

    results = {}
    for title, path, func, filters in SIMULATIONS:
        if module_filter in filters:
            script = TWIN_DIR / path
            if script.exists():
                print(f"\n▶ {title}")
                results[path] = load_and_run(script, func)
            else:
                print(f"\n⏭ {title} — script not found, skipping")

    print("\n" + "█" * 70)
    print("  ✅  DIGITAL TWIN RUN COMPLETE")
    print(f"  Modules executed: {len(results)}")
    print("█" * 70 + "\n")
    return results


if __name__ == '__main__':
    main()
