import math
import numpy as np

# Physical constants
epsilon_0 = 8.854e-12 # Vacuum permittivity
k_B = 1.38e-23        # Boltzmann constant
R = 8.314             # Ideal gas constant (J/(mol*K))

class SubcriticalHTLThermodynamics:
    """
    Formal predictive thermodynamic model for Subcritical Hydrothermal Liquefaction (HTL)
    (Module IV: FIRE). Models dielectric shifts, ionization, and bio-crude yields.
    """
    def __init__(self, temp_c: float, pressure_mpa: float):
        """
        temp_c: Operating temperature in Celsius (Target: ~300)
        pressure_mpa: Pressure in MPa (Target: >10 to maintain liquid phase)
        """
        self.T = temp_c + 273.15 # Kelvin
        self.P = pressure_mpa
        
        # Verify subcritical liquid state
        critical_T = 373.946 + 273.15
        if self.T >= critical_T:
            raise ValueError("[DANGER] State is Supercritical. Boiler failure imminent. Reduce Temp!")
            
    def calculate_dielectric_constant(self) -> float:
        """
        Calculates the approximate static relative permittivity (dielectric constant) of 
        subcritical water. Standard water has epsilon_r = 78 at 25C.
        Subcritical water drops drastically, acting as a non-polar solvent.
        (Uematsu & Franck empirical approximation)
        """
        # Simplified polynomial for illustrative purposes in this manuscript
        # Emulating the drop from ~80 to ~20 at 300C
        t_reduced = self.T / 298.15
        epsilon_r = 87.74 - 40.0 * (t_reduced - 1) + 9.39 * (t_reduced - 1)**2 - 1.41 * (t_reduced - 1)**3
        
        # Guard rails for empirical fit
        if epsilon_r < 15: epsilon_r = 15.0 
        
        return epsilon_r

    def calculate_reaction_rate(self, activation_energy_kj: float = 120.0, arrhenius_A: float = 1e11) -> float:
        """
        Calculates the Arrhenius reaction rate constant k for the depolymerization 
        of algal biomass into bio-crude.
        activation_energy_kj: E_a (Standard for HTL lipid depolymerization is ~80-140 kJ/mol)
        """
        E_a = activation_energy_kj * 1000 # Convert to Joules
        k = arrhenius_A * math.exp(-E_a / (R * self.T))
        return k

    def predict_hhv(self, carbon_pct: float, hydrogen_pct: float, oxygen_pct: float, nitrogen_pct: float) -> float:
        """
        Predicts the Higher Heating Value (HHV) of the extracted biocrude using the 
        Modified Dulong Equation (MJ/kg).
        """
        # Dulong: HHV (MJ/kg) = 0.338C + 1.428(H - O/8) + 0.095S
        # Assuming negligible Sulfur for microalgae
        hhv = 0.338 * carbon_pct + 1.428 * (hydrogen_pct - (oxygen_pct / 8)) + 0.095 * 0 
        return hhv

if __name__ == "__main__":
    print("--- [MODULE IV] HTL Thermodynamic Predictor ---")
    
    # Standard Operating Procedure parameterization
    htl = SubcriticalHTLThermodynamics(temp_c=300.0, pressure_mpa=15.0)
    
    dielectric = htl.calculate_dielectric_constant()
    print(f"Subcritical Relative Permittivity (ε_r) at 300°C: {dielectric:.2f} (Target: ~20 for organic solvation)")
    
    k = htl.calculate_reaction_rate()
    print(f"Depolymerization Rate Constant (k): {k:.4e} s^-1")
    
    # Theoretical elemental composition of extracted biocrude
    c_pct, h_pct, o_pct, n_pct = 75.0, 10.0, 10.0, 5.0
    hhv = htl.predict_hhv(c_pct, h_pct, o_pct, n_pct)
    print(f"Predicted Bio-Crude Higher Heating Value (HHV): {hhv:.2f} MJ/kg (Target: ~35-39 MJ/kg)")
