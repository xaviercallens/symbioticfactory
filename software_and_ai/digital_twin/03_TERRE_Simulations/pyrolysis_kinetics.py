"""
Symbiotic Factory Digital Twin — Cantera Pyrolysis Kinetics
============================================================
Module: 03_TERRE_Simulations / pyrolysis_kinetics.py
License: GNU GPLv3

Simulates the anaerobic pyrolysis of hydrochar from Module IV (FIRE).
Calculates:
  1. Syngas composition (CO, H2, CH4) as a function of pyrolysis temperature
  2. O:C atomic ratio of the resulting biochar (must be < 0.2 for millennial sequestration)
  3. Self-sustainability: does the syngas combustion energy meet the endothermic pyrolysis demand?

Usage:
    python pyrolysis_kinetics.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# =============================================================================
# 1. Syngas Composition Model
# =============================================================================
def syngas_composition(T_celsius):
    """
    Empirical model for syngas composition during slow biomass pyrolysis.
    Based on thermogravimetric analysis (TGA) data from literature.
    
    Returns dict of mass fractions: CO, H2, CH4, CO2, tar
    """
    # CO increases with temperature (Boudouard equilibrium)
    co_frac = 0.10 + 0.0004 * (T_celsius - 300)
    
    # H2 increases sharply above 500°C (water-gas shift)
    h2_frac = 0.02 + 0.0006 * max(0, T_celsius - 400)
    
    # CH4 peaks around 500°C then decreases (thermal cracking)
    ch4_frac = 0.08 * np.exp(-0.5 * ((T_celsius - 500) / 100)**2)
    
    # CO2 decreases with temperature
    co2_frac = 0.30 - 0.0003 * (T_celsius - 300)
    
    # Tar decreases with temperature (more complete cracking)
    tar_frac = max(0.01, 0.25 - 0.0005 * (T_celsius - 300))
    
    total = co_frac + h2_frac + ch4_frac + co2_frac + tar_frac
    
    return {
        'CO': co_frac / total,
        'H2': h2_frac / total,
        'CH4': ch4_frac / total,
        'CO2': co2_frac / total,
        'Tar': tar_frac / total
    }


# =============================================================================
# 2. O:C Ratio Model
# =============================================================================
def oc_ratio(T_celsius, hold_time_hours=1.0):
    """
    Predicts the O:C atomic ratio of biochar as a function of pyrolysis conditions.
    
    Literature benchmarks (Spokas, 2010):
      - O:C < 0.2  → > 1000 years stability (GOAL)
      - O:C 0.2-0.6 → 100-1000 years
      - O:C > 0.6  → < 100 years
    
    Higher temperatures and longer hold times drive off more oxygen.
    """
    # Base O:C decreases exponentially with temperature
    oc_base = 0.55 * np.exp(-0.004 * (T_celsius - 300))
    
    # Hold time further reduces O:C (logarithmic effect)
    time_factor = 1.0 - 0.05 * np.log(max(hold_time_hours, 0.1))
    
    return max(0.02, oc_base * time_factor)


# =============================================================================
# 3. Energy Balance: Self-Sustaining Check
# =============================================================================
def energy_balance(T_celsius, feedstock_mass_kg=10.0):
    """
    Checks whether the thermal energy released by combusting the syngas
    is sufficient to sustain the endothermic pyrolysis reaction.
    
    Returns (syngas_energy_MJ, pyrolysis_demand_MJ, is_self_sustaining)
    """
    # Volatile fraction decreases with temperature
    volatile_fraction = 0.70 - 0.0005 * (T_celsius - 300)
    volatile_mass = feedstock_mass_kg * volatile_fraction
    
    # Average HHV of pyrolysis syngas: ~8-12 MJ/kg 
    syngas = syngas_composition(T_celsius)
    # Weighted HHV (MJ/kg): CO=10.1, H2=120, CH4=55.5, CO2=0, Tar=20
    hhv_mix = (syngas['CO'] * 10.1 + syngas['H2'] * 120.0 + 
               syngas['CH4'] * 55.5 + syngas['Tar'] * 20.0)
    
    syngas_energy = volatile_mass * hhv_mix
    
    # Endothermic pyrolysis demand: ~1.5-2.5 MJ/kg biomass
    pyrolysis_demand = feedstock_mass_kg * (1.5 + 0.003 * (T_celsius - 300))
    
    return syngas_energy, pyrolysis_demand, syngas_energy > pyrolysis_demand


# =============================================================================
# 4. Simulation Runner
# =============================================================================
def run_pyrolysis_simulation():
    temps = np.linspace(350, 700, 200)
    hold_time = 1.0  # hours
    
    oc_ratios = [oc_ratio(t, hold_time) for t in temps]
    
    syngas_profiles = {
        'CO': [], 'H2': [], 'CH4': [], 'CO2': [], 'Tar': []
    }
    for t in temps:
        comp = syngas_composition(t)
        for key in syngas_profiles:
            syngas_profiles[key].append(comp[key] * 100)
    
    energies = [energy_balance(t) for t in temps]
    syngas_e = [e[0] for e in energies]
    pyro_d = [e[1] for e in energies]
    
    # Find minimum temperature for O:C < 0.2
    target_temps = [t for t, oc in zip(temps, oc_ratios) if oc < 0.2]
    min_temp_for_pac = target_temps[0] if target_temps else float('inf')
    
    print("=" * 70)
    print("  SYMBIOTIC FACTORY DIGITAL TWIN — Pyrolysis Kinetics (TERRE)")
    print("=" * 70)
    print(f"  Hold Time:                {hold_time:.1f} hours")
    print(f"  Min Temp for O:C < 0.2:   {min_temp_for_pac:.0f} °C")
    print(f"  O:C at 500°C:             {oc_ratio(500, hold_time):.3f}")
    print(f"  O:C at 600°C:             {oc_ratio(600, hold_time):.3f}")
    ss_500 = energy_balance(500)
    print(f"  Self-sustaining at 500°C:  {'✅ YES' if ss_500[2] else '❌ NO'}")
    print(f"    Syngas Energy:           {ss_500[0]:.1f} MJ")
    print(f"    Pyrolysis Demand:        {ss_500[1]:.1f} MJ")
    print("=" * 70)
    
    # Generate plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Symbiotic Factory — Anaerobic Pyrolysis Simulation (TERRE)', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: O:C Ratio
    axes[0, 0].plot(temps, oc_ratios, 'k-', linewidth=2)
    axes[0, 0].axhline(y=0.2, color='r', linestyle='--', alpha=0.7,
                        label='O:C = 0.2 (1000yr threshold)')
    axes[0, 0].axvline(x=min_temp_for_pac, color='g', linestyle=':', alpha=0.7,
                        label=f'Min T = {min_temp_for_pac:.0f}°C')
    axes[0, 0].set_xlabel('Pyrolysis Temperature (°C)')
    axes[0, 0].set_ylabel('O:C Atomic Ratio')
    axes[0, 0].set_title('Biochar Recalcitrance vs. Temperature')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Syngas Composition
    for key, vals in syngas_profiles.items():
        axes[0, 1].plot(temps, vals, linewidth=2, label=key)
    axes[0, 1].set_xlabel('Pyrolysis Temperature (°C)')
    axes[0, 1].set_ylabel('Gas-Phase Fraction (%)')
    axes[0, 1].set_title('Syngas Composition')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Energy Balance
    axes[1, 0].plot(temps, syngas_e, 'g-', linewidth=2, label='Syngas Energy (Output)')
    axes[1, 0].plot(temps, pyro_d, 'r--', linewidth=2, label='Pyrolysis Demand (Input)')
    axes[1, 0].fill_between(temps, pyro_d, syngas_e,
                             where=[s > p for s, p in zip(syngas_e, pyro_d)],
                             alpha=0.2, color='green', label='Self-Sustaining Zone')
    axes[1, 0].set_xlabel('Pyrolysis Temperature (°C)')
    axes[1, 0].set_ylabel('Energy (MJ per 10 kg feedstock)')
    axes[1, 0].set_title('Thermal Self-Sustainability')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Biochar Yield
    char_yields = [max(0.20, 0.60 - 0.00075 * t) * 100 for t in temps]
    axes[1, 1].plot(temps, char_yields, 'brown', linewidth=2)
    axes[1, 1].set_xlabel('Pyrolysis Temperature (°C)')
    axes[1, 1].set_ylabel('Biochar Yield (%)')
    axes[1, 1].set_title('Solid Carbon Recovery')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pyrolysis_kinetics_report.png', dpi=150)
    print(f"\n  📊 Report saved to: pyrolysis_kinetics_report.png")
    
    return min_temp_for_pac


if __name__ == '__main__':
    run_pyrolysis_simulation()
