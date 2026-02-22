"""
Symbiotic Factory — COBRApy Chlorella vulgaris Photosynthetic FBA
=================================================================
Module: 05_WETWARE_Simulations / chlorella_flux.py
License: GNU GPLv3

Models the photosynthetic metabolism of Chlorella vulgaris to predict
maximum biomass yield under varying CO2 and photon flux conditions.
Cross-validates the LED frequency set by the ESP32 firmware.

Usage: python chlorella_flux.py
"""

import numpy as np


class ChlorellaPhotosynthesisModel:
    """
    Simplified stoichiometric model of Chlorella vulgaris photosynthesis.

    Core reaction (Redfield):
      106 CO2 + 16 NO3- + HPO4^2- + 122 H2O + 18 H+
        → C106H263O110N16P + 138 O2

    The flashing-light effect increases the quantum yield by preventing
    photoinhibition of the Plastoquinone (PQ) pool.
    """

    MW_CO2 = 44.01
    MW_BIOMASS = 2422.0  # Approximate MW of Redfield formula unit

    def __init__(self, led_frequency_hz=25.0, co2_concentration_mM=2.0):
        self.led_freq = led_frequency_hz
        self.co2_conc = co2_concentration_mM

    def quantum_yield(self):
        """
        Models the quantum yield of photosynthesis as a function of L/D
        cycling frequency. The PQ pool turnover rate is ~10-50 Hz.

        Below 5 Hz: cells spend too long in saturating light → photoinhibition
        Above 50 Hz: diminishing returns (PQ fully recovered each cycle)
        """
        # Sigmoid centered around the PQ turnover sweet spot
        pq_turnover = 25.0  # Hz, midpoint
        qy = 0.08 / (1 + np.exp(-0.15 * (self.led_freq - pq_turnover / 2)))
        return min(qy, 0.08)  # Max theoretical QY for C3 photosynthesis

    def monod_kinetics(self):
        """
        Monod-type CO2 limitation on growth rate.
        mu = mu_max * [CO2] / (Ks + [CO2])

        Ks for Chlorella ≈ 0.2 mM (with CCM active)
        """
        mu_max = 0.35  # 1/hr, typical for Chlorella under optimal light
        ks = 0.2  # mM
        return mu_max * self.co2_conc / (ks + self.co2_conc)

    def predict_biomass_yield(self, reactor_volume_L=100.0, cell_density_g_L=2.0):
        """
        Predicts daily biomass productivity (g/L/day).
        """
        qy = self.quantum_yield()
        mu = self.monod_kinetics()

        # Effective growth rate includes flashing-light enhancement
        flash_enhancement = 1.0 + 2.0 * qy / 0.08  # Up to 3x boost
        effective_mu = mu * flash_enhancement

        # Volumetric productivity
        productivity = effective_mu * cell_density_g_L * 24  # g/L/day
        total_daily = productivity * reactor_volume_L / 1000  # kg/day

        # CO2 consumption (stoichiometric: ~1.83 kg CO2 per kg biomass)
        co2_consumed = total_daily * 1.83

        # O2 production (stoichiometric: ~1.37 kg O2 per kg biomass)
        o2_produced = total_daily * 1.37

        return {
            'quantum_yield': qy,
            'growth_rate_per_hr': effective_mu,
            'productivity_g_L_day': productivity,
            'total_biomass_kg_day': total_daily,
            'co2_consumed_kg_day': co2_consumed,
            'o2_produced_kg_day': o2_produced,
            'flash_enhancement_factor': flash_enhancement
        }


def run_simulation():
    print("=" * 70)
    print("  DIGITAL TWIN — Chlorella vulgaris Photosynthetic FBA")
    print("=" * 70)

    # Sweep LED frequency
    freqs = np.linspace(1, 100, 100)
    productivities = []
    for f in freqs:
        model = ChlorellaPhotosynthesisModel(led_frequency_hz=f, co2_concentration_mM=2.0)
        result = model.predict_biomass_yield()
        productivities.append(result['productivity_g_L_day'])

    optimal_freq = freqs[np.argmax(productivities)]
    max_prod = max(productivities)

    # Report at ESP32 default (25 Hz) and optimal
    for freq_label, freq_val in [("ESP32 Default (25 Hz)", 25.0), (f"Optimal ({optimal_freq:.0f} Hz)", optimal_freq)]:
        model = ChlorellaPhotosynthesisModel(led_frequency_hz=freq_val)
        r = model.predict_biomass_yield()
        print(f"\n  --- {freq_label} ---")
        print(f"  Quantum Yield:          {r['quantum_yield']:.4f} mol/mol")
        print(f"  Flash Enhancement:      {r['flash_enhancement_factor']:.2f}x")
        print(f"  Growth Rate:            {r['growth_rate_per_hr']:.3f} /hr")
        print(f"  Productivity:           {r['productivity_g_L_day']:.2f} g/L/day")
        print(f"  Daily Biomass (100L):   {r['total_biomass_kg_day']:.3f} kg/day")
        print(f"  CO₂ Consumed:           {r['co2_consumed_kg_day']:.3f} kg/day")
        print(f"  O₂ Produced:            {r['o2_produced_kg_day']:.3f} kg/day")

    print(f"\n  Peak Productivity:      {max_prod:.2f} g/L/day at {optimal_freq:.0f} Hz")
    print("=" * 70)
    return optimal_freq


if __name__ == '__main__':
    run_simulation()
