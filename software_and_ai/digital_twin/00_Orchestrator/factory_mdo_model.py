"""
Symbiotic Factory Digital Twin — NASA OpenMDAO System Optimizer
==============================================================
Module: 00_Orchestrator / factory_mdo_model.py
License: GNU GPLv3

This script uses NASA Glenn Research Center's OpenMDAO framework to perform
Multidisciplinary Design Optimization (MDO) across all four modules of the
Symbiotic Factory. It wires the thermodynamic outputs of each module into a
unified optimization problem that maximizes the Energy Return on Investment (EROI).

Usage:
    python factory_mdo_model.py
"""

import openmdao.api as om
import numpy as np


# =============================================================================
# Module I: SUN — Plasmonic Interfacial Solar Steam Generator
# =============================================================================
class SUNModule(om.ExplicitComponent):
    """
    Calculates freshwater production rate based on solar irradiance,
    membrane area, and the LSPR-enhanced evaporation efficiency.
    """

    def setup(self):
        # Inputs
        self.add_input('solar_irradiance', val=1000.0, units='W/m**2',
                        desc='Global Horizontal Irradiance (GHI)')
        self.add_input('membrane_area', val=1.0, units='m**2',
                        desc='Active ISSG membrane area')
        self.add_input('lspr_efficiency', val=0.92,
                        desc='Photothermal conversion efficiency of Ag-PAC')
        self.add_input('enthalpy_vap_effective', val=1250.0, units='kJ/kg',
                        desc='Nanoconfined enthalpy of vaporization')

        # Outputs
        self.add_output('freshwater_rate', val=0.0, units='kg/s',
                         desc='Distilled freshwater production rate')
        self.add_output('sun_thermal_power', val=0.0, units='W',
                         desc='Thermal power absorbed by the membrane')

    def compute(self, inputs, outputs):
        q_solar = inputs['solar_irradiance'] * inputs['membrane_area']
        q_absorbed = q_solar * inputs['lspr_efficiency']
        outputs['sun_thermal_power'] = q_absorbed
        # kg/s = W / (kJ/kg * 1000 J/kJ)
        outputs['freshwater_rate'] = q_absorbed / (inputs['enthalpy_vap_effective'] * 1000.0)


# =============================================================================
# Module II: WATER — Nano-Bubbling Algal Cycloreactor
# =============================================================================
class WATERModule(om.ExplicitComponent):
    """
    Calculates algal biomass production rate from CO2 mass-transfer,
    light/dark cycling frequency, and freshwater availability.
    """

    def setup(self):
        # Inputs
        self.add_input('freshwater_rate', val=0.0, units='kg/s',
                        desc='Freshwater from SUN module')
        self.add_input('co2_flow_rate', val=0.001, units='kg/s',
                        desc='CO2 injection rate')
        self.add_input('kla', val=0.05, units='1/s',
                        desc='Volumetric mass transfer coefficient')
        self.add_input('led_frequency', val=25.0, units='Hz',
                        desc='LED flashing-light frequency')
        self.add_input('reactor_volume', val=0.050, units='m**3',
                        desc='Total photobioreactor volume')

        # Outputs
        self.add_output('biomass_rate', val=0.0, units='kg/s',
                         desc='Wet algal biomass production rate')
        self.add_output('co2_absorbed', val=0.0, units='kg/s',
                         desc='Net CO2 absorbed by the algae')
        self.add_output('co2_exhaust', val=0.0, units='kg/s',
                         desc='Unabsorbed CO2 vented to FIRE Z-scheme')

    def compute(self, inputs, outputs):
        # CO2 dissolution rate (Henry's Law + Laplace enhancement)
        co2_dissolved = inputs['kla'] * inputs['reactor_volume'] * inputs['co2_flow_rate']

        # Flashing-light efficiency factor (peaks around 25 Hz for Chlorella)
        flash_eff = 1.0 - np.exp(-0.08 * inputs['led_frequency'])

        # Simplified algal yield: ~1.8 kg biomass per kg CO2 fixed
        co2_fixed = co2_dissolved * flash_eff * 0.85  # 85% biological fixation efficiency
        outputs['co2_absorbed'] = co2_fixed
        outputs['co2_exhaust'] = inputs['co2_flow_rate'] - co2_fixed
        outputs['biomass_rate'] = co2_fixed * 1.8  # stoichiometric ratio


# =============================================================================
# Module III: TERRE — TLUD Anaerobic Pyrolyzer
# =============================================================================
class TERREModule(om.ExplicitComponent):
    """
    Calculates PAC biochar yield and syngas energy from solid waste pyrolysis.
    """

    def setup(self):
        # Inputs
        self.add_input('solid_waste_rate', val=0.0, units='kg/s',
                        desc='Solid hydrochar waste from FIRE module')
        self.add_input('pyrolysis_temp', val=773.15, units='K',
                        desc='Pyrolysis temperature (default 500°C)')
        self.add_input('hold_time', val=3600.0, units='s',
                        desc='Pyrolysis hold time (default 1 hour)')

        # Outputs
        self.add_output('biochar_rate', val=0.0, units='kg/s',
                         desc='PAC biochar production rate')
        self.add_output('syngas_energy', val=0.0, units='W',
                         desc='Thermal energy from syngas combustion')
        self.add_output('oc_ratio', val=0.0,
                         desc='Oxygen:Carbon atomic ratio of the biochar')

    def compute(self, inputs, outputs):
        # Biochar yield decreases with temperature (more volatiles driven off)
        t_celsius = inputs['pyrolysis_temp'] - 273.15
        # Empirical: yield drops from ~45% at 400°C to ~30% at 600°C
        char_yield = 0.60 - 0.00075 * t_celsius
        char_yield = max(char_yield, 0.20)

        outputs['biochar_rate'] = inputs['solid_waste_rate'] * char_yield

        # Syngas energy: volatile fraction * average HHV of syngas (~10 MJ/kg)
        volatile_rate = inputs['solid_waste_rate'] * (1.0 - char_yield)
        outputs['syngas_energy'] = volatile_rate * 10e6  # W = kg/s * J/kg

        # O:C ratio decreases with temperature (more oxygen driven off)
        outputs['oc_ratio'] = max(0.05, 0.45 - 0.0008 * t_celsius)


# =============================================================================
# Module IV: FIRE — HTL Autoclave & Z-Scheme Fermenter
# =============================================================================
class FIREModule(om.ExplicitComponent):
    """
    Calculates bio-crude yield from HTL and ethanol yield from Z-scheme
    CO-to-alcohol fermentation.
    """

    def setup(self):
        # Inputs
        self.add_input('biomass_rate', val=0.0, units='kg/s',
                        desc='Wet algal biomass from WATER module')
        self.add_input('co2_exhaust', val=0.0, units='kg/s',
                        desc='Unabsorbed CO2 from WATER module')
        self.add_input('htl_temp', val=573.15, units='K',
                        desc='HTL operating temperature (default 300°C)')
        self.add_input('htl_pressure', val=15e6, units='Pa',
                        desc='HTL operating pressure (default 150 bar)')
        self.add_input('htl_hold_time', val=1800.0, units='s',
                        desc='HTL reaction hold time (default 30 min)')

        # Outputs
        self.add_output('biocrude_rate', val=0.0, units='kg/s',
                         desc='Heavy bio-crude output rate')
        self.add_output('biocrude_hhv', val=0.0, units='J/kg',
                         desc='Higher Heating Value of the bio-crude')
        self.add_output('ethanol_rate', val=0.0, units='kg/s',
                         desc='Ethanol production from Clostridium')
        self.add_output('solid_waste_rate', val=0.0, units='kg/s',
                         desc='Solid hydrochar waste → TERRE module')
        self.add_output('htl_energy_required', val=0.0, units='W',
                         desc='Thermal energy needed for HTL')

    def compute(self, inputs, outputs):
        t_celsius = inputs['htl_temp'] - 273.15

        # Bio-crude yield: ~35% of dry biomass at 300°C, peaks around 320°C
        # Wet algae is ~85% water, so dry fraction = 0.15
        dry_biomass = inputs['biomass_rate'] * 0.15
        crude_yield_frac = 0.25 + 0.001 * (t_celsius - 250)
        crude_yield_frac = min(max(crude_yield_frac, 0.15), 0.45)

        outputs['biocrude_rate'] = dry_biomass * crude_yield_frac

        # HHV of algal bio-crude: typically 35-39 MJ/kg
        outputs['biocrude_hhv'] = (35.0 + 0.02 * (t_celsius - 250)) * 1e6

        # Solid residue (hydrochar) → TERRE
        outputs['solid_waste_rate'] = dry_biomass * (1.0 - crude_yield_frac) * 0.6

        # Z-Scheme: CO2 → CO → Ethanol via Clostridium
        # Approximate: 6 CO + 3 H2O → C2H5OH + 4 CO2 (Wood-Ljungdahl)
        # ~30% of exhaust CO2 is converted to CO by the photocatalyst
        co_produced = inputs['co2_exhaust'] * 0.30
        # Stoichiometric: ~0.27 kg ethanol per kg CO consumed
        outputs['ethanol_rate'] = co_produced * 0.27

        # Energy required: heating water from 25°C to 300°C at 150 bar
        water_mass_rate = inputs['biomass_rate'] * 0.85
        cp_water = 4200.0  # J/(kg·K)
        delta_t = t_celsius - 25.0
        outputs['htl_energy_required'] = water_mass_rate * cp_water * delta_t


# =============================================================================
# EROI Calculator — The Systemic Objective Function
# =============================================================================
class EROICalculator(om.ExplicitComponent):
    """
    Computes the Energy Return on Investment (EROI) for the entire
    Symbiotic Factory. EROI = Energy_Out / Energy_In.
    The optimization target is EROI > 3.5.
    """

    def setup(self):
        # Energy Outputs
        self.add_input('biocrude_rate', val=0.0, units='kg/s')
        self.add_input('biocrude_hhv', val=35e6, units='J/kg')
        self.add_input('ethanol_rate', val=0.0, units='kg/s')
        self.add_input('syngas_energy', val=0.0, units='W')

        # Energy Inputs
        self.add_input('htl_energy_required', val=0.0, units='W')
        self.add_input('sun_thermal_power', val=0.0, units='W')

        # Parasitic electrical loads
        self.add_input('pump_power', val=150.0, units='W',
                        desc='Recirculation pump for WATER module')
        self.add_input('led_power', val=50.0, units='W',
                        desc='WS2812B LED strips for flashing-light effect')

        # Output
        self.add_output('eroi', val=0.0, desc='Systemic EROI')

    def compute(self, inputs, outputs):
        ethanol_hhv = 29.7e6  # J/kg

        energy_out = (
            inputs['biocrude_rate'] * inputs['biocrude_hhv'] +
            inputs['ethanol_rate'] * ethanol_hhv +
            inputs['syngas_energy']
        )

        energy_in = (
            inputs['htl_energy_required'] +
            inputs['pump_power'] +
            inputs['led_power']
        )

        if energy_in > 0:
            outputs['eroi'] = energy_out / energy_in
        else:
            outputs['eroi'] = 0.0


# =============================================================================
# MAIN: Build the MDO Problem & Run the Optimizer
# =============================================================================
def build_and_run():
    prob = om.Problem()
    model = prob.model

    # --- Add Subsystems (The Four Elements) ---
    model.add_subsystem('sun', SUNModule(), promotes=['*'])
    model.add_subsystem('water', WATERModule(), promotes_inputs=['freshwater_rate'],
                         promotes_outputs=['biomass_rate', 'co2_absorbed', 'co2_exhaust'])
    model.add_subsystem('fire', FIREModule(), promotes_inputs=['biomass_rate', 'co2_exhaust'],
                         promotes_outputs=['biocrude_rate', 'biocrude_hhv', 'ethanol_rate',
                                           'solid_waste_rate', 'htl_energy_required'])
    model.add_subsystem('terre', TERREModule(), promotes_inputs=['solid_waste_rate'],
                         promotes_outputs=['biochar_rate', 'syngas_energy', 'oc_ratio'])
    model.add_subsystem('eroi_calc', EROICalculator(),
                         promotes_inputs=['biocrude_rate', 'biocrude_hhv', 'ethanol_rate',
                                          'syngas_energy', 'htl_energy_required',
                                          'sun_thermal_power'],
                         promotes_outputs=['eroi'])

    # --- Design Variables (What the optimizer can tweak) ---
    model.add_design_var('membrane_area', lower=0.5, upper=10.0)
    model.add_design_var('led_frequency', lower=5.0, upper=100.0)
    model.add_design_var('htl_temp', lower=523.15, upper=623.15)  # 250°C - 350°C
    model.add_design_var('pyrolysis_temp', lower=673.15, upper=873.15)  # 400°C - 600°C

    # --- Objective: Maximize EROI ---
    model.add_objective('eroi', scaler=-1.0)  # Negative scaler for maximization

    # --- Constraints ---
    model.add_constraint('oc_ratio', upper=0.2,
                          ref=0.2)  # PAC must be recalcitrant

    # --- Configure the Optimizer ---
    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'
    prob.driver.options['maxiter'] = 200
    prob.driver.options['tol'] = 1e-8

    # --- Setup & Run ---
    prob.setup()

    # Set initial conditions
    prob.set_val('solar_irradiance', 800.0)  # W/m² (typical mid-latitude)
    prob.set_val('co2_flow_rate', 0.005)     # 5 g/s CO2 injection
    prob.set_val('reactor_volume', 0.100)    # 100L photobioreactor

    print("=" * 70)
    print("  SYMBIOTIC FACTORY DIGITAL TWIN — NASA OpenMDAO MDO")
    print("  Optimizing the Water-Energy-Food-Carbon (WEFC) Nexus")
    print("=" * 70)

    prob.run_driver()

    # --- Report Results ---
    print("\n" + "=" * 70)
    print("  OPTIMIZATION RESULTS")
    print("=" * 70)
    print(f"  Systemic EROI:           {prob.get_val('eroi')[0]:.2f}")
    print(f"  EROI Gate (> 3.5):       {'✅ PASS' if prob.get_val('eroi')[0] > 3.5 else '❌ FAIL'}")
    print(f"  ---")
    print(f"  Optimal Membrane Area:   {prob.get_val('membrane_area')[0]:.2f} m²")
    print(f"  Optimal LED Frequency:   {prob.get_val('led_frequency')[0]:.1f} Hz")
    print(f"  Optimal HTL Temp:        {prob.get_val('htl_temp')[0] - 273.15:.1f} °C")
    print(f"  Optimal Pyrolysis Temp:  {prob.get_val('pyrolysis_temp')[0] - 273.15:.1f} °C")
    print(f"  ---")
    print(f"  Freshwater Rate:         {prob.get_val('freshwater_rate')[0]*3600:.2f} kg/hr")
    print(f"  Biomass Rate:            {prob.get_val('biomass_rate')[0]*3600:.4f} kg/hr")
    print(f"  Bio-Crude Rate:          {prob.get_val('biocrude_rate')[0]*3600:.4f} kg/hr")
    print(f"  Bio-Crude HHV:           {prob.get_val('biocrude_hhv')[0]/1e6:.1f} MJ/kg")
    print(f"  Ethanol Rate:            {prob.get_val('ethanol_rate')[0]*3600:.4f} kg/hr")
    print(f"  Biochar Rate:            {prob.get_val('biochar_rate')[0]*3600:.4f} kg/hr")
    print(f"  Biochar O:C Ratio:       {prob.get_val('oc_ratio')[0]:.3f}")
    print(f"  CO₂ Absorbed:            {prob.get_val('co2_absorbed')[0]*3600:.4f} kg/hr")
    print("=" * 70)

    return prob


if __name__ == '__main__':
    build_and_run()
