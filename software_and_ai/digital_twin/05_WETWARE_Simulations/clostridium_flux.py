"""
Symbiotic Factory — COBRApy Clostridium Metabolic Flux Analysis
Module: 05_WETWARE_Simulations / clostridium_flux.py
License: GNU GPLv3

Models the Wood-Ljungdahl pathway in Clostridium autoethanogenum,
predicting CO→Ethanol/Butanol yields as a function of pH.
"""

import numpy as np

class WoodLjungdahlModel:
    MW_CO = 28.01
    MW_ETHANOL = 46.07
    MW_BUTANOL = 74.12

    def __init__(self, ph=6.0, temperature_celsius=37.0):
        self.ph = ph
        self.temperature = temperature_celsius

    def _ph_selectivity(self):
        eth = 0.6 * np.exp(-2.0 * (self.ph - 5.8)**2)
        but = 0.3 * np.exp(-3.0 * (self.ph - 5.5)**2)
        ace = max(0.1, 1.0 - eth - but)
        total = eth + but + ace
        return {'ethanol': eth/total, 'butanol': but/total, 'acetate': ace/total}

    def flux_balance_analysis(self, co_uptake=50.0):
        sel = self._ph_selectivity()
        co_per = sel['ethanol']*6 + sel['butanol']*12 + sel['acetate']*4
        prod_flux = co_uptake / co_per
        eth_flux = prod_flux * sel['ethanol']
        but_flux = prod_flux * sel['butanol']
        co_mass = co_uptake * self.MW_CO / 1000.0
        eth_mass = eth_flux * self.MW_ETHANOL / 1000.0
        but_mass = but_flux * self.MW_BUTANOL / 1000.0
        c_eff = (eth_flux*2 + but_flux*4 + prod_flux*sel['acetate']*2) / co_uptake
        return {
            'selectivity': sel,
            'ethanol_yield': eth_mass/co_mass if co_mass > 0 else 0,
            'butanol_yield': but_mass/co_mass if co_mass > 0 else 0,
            'carbon_efficiency': c_eff,
            'energy_kJ': eth_mass*29.7 + but_mass*36.1
        }

def run_simulation():
    print("="*70)
    print("  DIGITAL TWIN — Clostridium Metabolic FBA")
    print("="*70)
    for ph in [5.8, 6.4]:
        fba = WoodLjungdahlModel(ph=ph).flux_balance_analysis()
        print(f"\n  pH {ph}:")
        for k, v in fba['selectivity'].items():
            print(f"    {k}: {v*100:.1f}%")
        print(f"    Carbon Eff: {fba['carbon_efficiency']*100:.1f}%")
    print("="*70)

if __name__ == '__main__':
    run_simulation()
