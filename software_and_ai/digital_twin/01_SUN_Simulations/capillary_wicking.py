"""
Symbiotic Factory — SUN Module Capillary Wicking Simulation
============================================================
Module: 01_SUN_Simulations / capillary_wicking.py
License: GNU GPLv3

Models the porous media transport through the PAC biochar matrix to
verify that the capillary pumping rate matches the evaporation rate
under LSPR-enhanced solar conditions.

Physics: Washburn equation + Darcy flow in a porous sponge.

Usage: python capillary_wicking.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# =============================================================================
# 1. Washburn Equation: Capillary Rise Dynamics
# =============================================================================
def washburn_height(t_seconds, pore_radius_m, contact_angle_deg=20.0):
    """
    Lucas-Washburn equation for capillary rise in a cylindrical pore:
        h(t) = sqrt(r * γ * cos(θ) * t / (2η))
    
    Parameters:
        t_seconds: time (s)
        pore_radius_m: average pore radius (m)
        contact_angle_deg: water-biochar contact angle (hydrophilic ~20°)
    """
    gamma = 0.0728     # Surface tension of water (N/m) at 25°C
    eta = 1.002e-3      # Dynamic viscosity of water (Pa·s) at 20°C
    theta = np.radians(contact_angle_deg)

    h = np.sqrt(pore_radius_m * gamma * np.cos(theta) * t_seconds / (2 * eta))
    return h


# =============================================================================
# 2. Darcy Permeability: Steady-State Flow Rate Through the Sponge
# =============================================================================
def darcy_flow_rate(sponge_thickness_m, pore_radius_m, porosity=0.65):
    """
    Darcy's law: volumetric flow rate per unit area through the biochar.
        q = (K / η) * (ΔP / L)
    
    K (permeability) estimated via Kozeny-Carman:
        K = (d² * ε³) / (180 * (1-ε)²)
    """
    eta = 1.002e-3
    d = pore_radius_m * 2
    epsilon = porosity

    # Kozeny-Carman permeability
    K = (d**2 * epsilon**3) / (180 * (1 - epsilon)**2)

    # Capillary pressure driving flow
    gamma = 0.0728
    theta_rad = np.radians(20)
    delta_P = 2 * gamma * np.cos(theta_rad) / pore_radius_m

    q = (K / eta) * (delta_P / sponge_thickness_m)  # m³/(m²·s) = m/s
    return q, K


# =============================================================================
# 3. Evaporation Rate Under LSPR Enhancement
# =============================================================================
def lspr_evaporation_rate(ghi_W_m2=800.0, efficiency=0.92, h_vap_eff_J_kg=1250e3):
    """
    Mass flux of water evaporated from the ISSG membrane surface.
        m_dot = (GHI * η) / ΔH_vap   [kg/(m²·s)]
    """
    return ghi_W_m2 * efficiency / h_vap_eff_J_kg


# =============================================================================
# 4. Steady-State Matching: Does Supply Meet Demand?
# =============================================================================
def run_simulation():
    pore_radii = np.logspace(-8, -5, 200)  # 10nm to 10μm
    sponge_thickness = 0.020  # 20mm

    evap_rate = lspr_evaporation_rate()  # kg/(m²·s)
    evap_rate_m_s = evap_rate / 1000.0   # Convert to m/s (m³/m²/s)

    darcy_rates = []
    washburn_times = []
    for r in pore_radii:
        q, _ = darcy_flow_rate(sponge_thickness, r)
        darcy_rates.append(q)
        # Time to wick through full sponge thickness
        t_wick = (sponge_thickness**2 * 2 * 1.002e-3) / (r * 0.0728 * np.cos(np.radians(20)))
        washburn_times.append(t_wick)

    darcy_rates = np.array(darcy_rates)

    # Find pore radius where supply = demand
    crossover_idx = np.argmin(np.abs(darcy_rates - evap_rate_m_s))
    optimal_pore = pore_radii[crossover_idx]

    print("=" * 70)
    print("  DIGITAL TWIN — SUN Module Capillary Wicking Analysis")
    print("=" * 70)
    print(f"  Sponge Thickness:         {sponge_thickness*1000:.0f} mm")
    print(f"  LSPR Evaporation Rate:    {evap_rate*3600:.2f} kg/(m²·hr)")
    print(f"  Evaporation Rate (m/s):   {evap_rate_m_s:.2e}")
    print(f"  ---")
    print(f"  Optimal Pore Radius:      {optimal_pore*1e6:.2f} μm")
    print(f"  Darcy Flow at Optimal:    {darcy_rates[crossover_idx]:.2e} m/s")
    print(f"  Washburn Wick Time:       {washburn_times[crossover_idx]:.1f} s")
    print(f"  Supply/Demand Ratio:      {darcy_rates[crossover_idx]/evap_rate_m_s:.2f}")
    print(f"  Status:                   {'✅ BALANCED' if 0.8 < darcy_rates[crossover_idx]/evap_rate_m_s < 1.5 else '⚠️ MISMATCH'}")
    print("=" * 70)

    # Generate plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('SUN Module — Capillary Wicking vs Evaporation', fontsize=14, fontweight='bold')

    axes[0].loglog(pore_radii * 1e6, darcy_rates, 'b-', linewidth=2, label='Darcy Supply Rate')
    axes[0].axhline(y=evap_rate_m_s, color='r', linestyle='--', linewidth=2, label='LSPR Evaporation Demand')
    axes[0].axvline(x=optimal_pore * 1e6, color='g', linestyle=':', alpha=0.7,
                    label=f'Optimal: {optimal_pore*1e6:.2f} μm')
    axes[0].set_xlabel('Pore Radius (μm)')
    axes[0].set_ylabel('Flow Rate (m/s)')
    axes[0].set_title('Supply-Demand Matching')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].loglog(pore_radii * 1e6, washburn_times, 'purple', linewidth=2)
    axes[1].set_xlabel('Pore Radius (μm)')
    axes[1].set_ylabel('Wicking Time (s)')
    axes[1].set_title('Washburn Capillary Rise Time')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('capillary_wicking_report.png', dpi=150)
    print(f"\n  📊 Report saved to: capillary_wicking_report.png")

    return optimal_pore


if __name__ == '__main__':
    run_simulation()
