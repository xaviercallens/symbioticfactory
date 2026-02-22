"""
Symbiotic Factory — DWSIM-style Heat Exchanger Optimization
=============================================================
Module: 04_FIRE_Simulations / heat_exchanger_model.py
License: GNU GPLv3

Models the concentric tube-in-tube counter-current heat exchanger
(The Economizer) that recovers thermal energy from the outgoing 300°C
bio-crude stream to pre-heat the incoming 25°C wet algal slurry.

Target: > 85% thermal recovery efficiency.

Usage: python heat_exchanger_model.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# =============================================================================
# Counter-Current Heat Exchanger Model (ε-NTU Method)
# =============================================================================
class CounterCurrentHeatExchanger:
    """
    ε-NTU method for a concentric tube counter-current heat exchanger.

    Hot side: outgoing bio-crude + subcritical water at ~300°C
    Cold side: incoming wet algal slurry at ~25°C
    """

    def __init__(self,
                 T_hot_in=300.0,      # °C
                 T_cold_in=25.0,      # °C
                 m_dot_hot=0.01,      # kg/s
                 m_dot_cold=0.01,     # kg/s
                 cp_hot=3800.0,       # J/(kg·K) — subcritical water + oil mix
                 cp_cold=4186.0,      # J/(kg·K) — water-algae slurry
                 U=150.0,             # Overall heat transfer coeff (W/(m²·K))
                 tube_length=2.0,     # m
                 tube_od=0.025,       # m (1 inch OD inner tube)
                 ):
        self.T_hot_in = T_hot_in
        self.T_cold_in = T_cold_in
        self.m_dot_hot = m_dot_hot
        self.m_dot_cold = m_dot_cold
        self.cp_hot = cp_hot
        self.cp_cold = cp_cold
        self.U = U
        self.L = tube_length
        self.d_o = tube_od

    def compute(self):
        # Heat capacity rates
        C_hot = self.m_dot_hot * self.cp_hot    # W/K
        C_cold = self.m_dot_cold * self.cp_cold
        C_min = min(C_hot, C_cold)
        C_max = max(C_hot, C_cold)
        C_r = C_min / C_max  # Capacity ratio

        # Heat transfer area
        A = np.pi * self.d_o * self.L  # m²

        # Number of Transfer Units
        NTU = self.U * A / C_min

        # ε-NTU for counter-current flow
        if abs(C_r - 1.0) < 1e-10:
            epsilon = NTU / (1 + NTU)
        else:
            epsilon = (1 - np.exp(-NTU * (1 - C_r))) / \
                      (1 - C_r * np.exp(-NTU * (1 - C_r)))

        # Maximum possible heat transfer
        Q_max = C_min * (self.T_hot_in - self.T_cold_in)
        Q_actual = epsilon * Q_max

        # Outlet temperatures
        T_hot_out = self.T_hot_in - Q_actual / C_hot
        T_cold_out = self.T_cold_in + Q_actual / C_cold

        # Log-Mean Temperature Difference
        dT1 = self.T_hot_in - T_cold_out
        dT2 = T_hot_out - self.T_cold_in
        if abs(dT1 - dT2) < 0.01:
            LMTD = dT1
        else:
            LMTD = (dT1 - dT2) / np.log(dT1 / dT2)

        return {
            'epsilon': epsilon,
            'NTU': NTU,
            'C_r': C_r,
            'Q_actual_W': Q_actual,
            'Q_max_W': Q_max,
            'T_hot_out': T_hot_out,
            'T_cold_out': T_cold_out,
            'LMTD': LMTD,
            'area_m2': A,
            'recovery_pct': epsilon * 100
        }


def run_simulation():
    print("=" * 70)
    print("  DIGITAL TWIN — DWSIM Heat Exchanger Optimization (FIRE)")
    print("=" * 70)

    # Baseline design
    hx = CounterCurrentHeatExchanger()
    result = hx.compute()

    print(f"\n  --- Baseline Design (L={hx.L}m, U={hx.U} W/(m²·K)) ---")
    print(f"  Heat Transfer Area:     {result['area_m2']:.4f} m²")
    print(f"  NTU:                    {result['NTU']:.2f}")
    print(f"  Effectiveness (ε):      {result['epsilon']:.3f}")
    print(f"  Thermal Recovery:       {result['recovery_pct']:.1f}%")
    print(f"  T_hot_out:              {result['T_hot_out']:.1f} °C")
    print(f"  T_cold_out:             {result['T_cold_out']:.1f} °C")
    print(f"  LMTD:                   {result['LMTD']:.1f} °C")
    print(f"  Heat Recovered:         {result['Q_actual_W']:.0f} W")
    print(f"  Target (>85%):          {'✅ PASS' if result['recovery_pct'] > 85 else '❌ FAIL'}")

    # Sweep tube length to find minimum length for 85% recovery
    lengths = np.linspace(0.5, 10.0, 200)
    recoveries = []
    for L in lengths:
        hx_sweep = CounterCurrentHeatExchanger(tube_length=L)
        r = hx_sweep.compute()
        recoveries.append(r['recovery_pct'])

    target_idx = next((i for i, r in enumerate(recoveries) if r >= 85.0), None)
    min_length = lengths[target_idx] if target_idx else float('inf')

    # Sweep U coefficient  
    u_values = np.linspace(50, 500, 200)
    recoveries_u = []
    for u in u_values:
        hx_u = CounterCurrentHeatExchanger(U=u)
        r = hx_u.compute()
        recoveries_u.append(r['recovery_pct'])

    print(f"\n  --- Optimization Results ---")
    print(f"  Min tube length for 85%: {min_length:.2f} m")
    print(f"  Recovery at L=5m:        {recoveries[np.argmin(np.abs(lengths-5.0))]:.1f}%")
    print("=" * 70)

    # Generate plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('FIRE Module — Counter-Current Heat Exchanger Optimization',
                 fontsize=14, fontweight='bold')

    axes[0].plot(lengths, recoveries, 'r-', linewidth=2)
    axes[0].axhline(y=85, color='g', linestyle='--', alpha=0.7, label='85% target')
    if target_idx:
        axes[0].axvline(x=min_length, color='b', linestyle=':', alpha=0.7,
                        label=f'Min L = {min_length:.1f} m')
    axes[0].set_xlabel('Tube Length (m)')
    axes[0].set_ylabel('Thermal Recovery (%)')
    axes[0].set_title('Recovery vs. Tube Length')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(u_values, recoveries_u, 'm-', linewidth=2)
    axes[1].axhline(y=85, color='g', linestyle='--', alpha=0.7, label='85% target')
    axes[1].set_xlabel('Overall U (W/(m²·K))')
    axes[1].set_ylabel('Thermal Recovery (%)')
    axes[1].set_title('Recovery vs. Heat Transfer Coefficient')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('heat_exchanger_report.png', dpi=150)
    print(f"\n  📊 Report saved to: heat_exchanger_report.png")

    return result


if __name__ == '__main__':
    run_simulation()
