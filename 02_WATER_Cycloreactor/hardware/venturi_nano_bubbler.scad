/*
  Symbiotic Factory - Module II (WATER)
  Hardware: Parametric Venturi Nano-Bubbler
  License: CERN-OHL-S
  
  Description:
  This nozzle utilizes continuity and Bernoulli principles to drop fluid pressure 
  at the throat, drawing in CO2 enriched air. The extreme velocity shear forces 
  the air into nanoscale bubbles, increasing Laplace pressure (\Delta P = 2\gamma/r) 
  to bypass the low aqueous solubility limit of CO2 for hyper-dense algal growth.
*/

// --- Core Parameters (Customize for your local pump & PVC sizing) ---
$fn = 100; // Curve resolution (higher = smoother prints)

inlet_outer_dia = 25.0;  // Outer diameter of the inlet pipe connection (mm)
inlet_inner_dia = 20.0;  // Inner diameter of the incoming fluid flow (mm)
throat_dia = 6.0;        // Diameter of the Venturi constriction (mm). Smaller = higher shear.
diffuser_outer_dia = 25.0; // Outer diameter of the outlet
diffuser_inner_dia = 20.0; // Inner diameter of the diffusing fluid

inlet_length = 25.0;
converging_length = 20.0; 
throat_length = 15.0;
diffusing_length = 35.0;   // Gradual slope prevents flow separation
outlet_length = 25.0;

gas_port_inner_dia = 4.0;  // Standard silicone airline tubing
gas_port_outer_dia = 7.0;
gas_port_length = 15.0;

wall_thickness = 3.0; // Structural integrity for PETG/PC prints under pressure

// --- Generated Venturi Body ---
module venturi_nozzle() {
    difference() {
        // --- 1. Solid Outer Body ---
        union() {
            // Inlet tube
            cylinder(h=inlet_length, d=inlet_outer_dia);
            
            // Converging Conus
            translate([0, 0, inlet_length])
                cylinder(h=converging_length, d1=inlet_outer_dia, d2=throat_dia + (wall_thickness*2));
                
            // Throat 
            translate([0, 0, inlet_length + converging_length])
                cylinder(h=throat_length, d=throat_dia + (wall_thickness*2));
                
            // Diffusing Conus (diverging)
            translate([0, 0, inlet_length + converging_length + throat_length])
                cylinder(h=diffusing_length, d1=throat_dia + (wall_thickness*2), d2=diffuser_outer_dia);
                
            // Outlet tube
            translate([0, 0, inlet_length + converging_length + throat_length + diffusing_length])
                cylinder(h=outlet_length, d=diffuser_outer_dia);
                
            // Gas Injection Port (Placed at the throat where pressure drops)
            translate([0, (throat_dia/2) + wall_thickness - 1, inlet_length + converging_length + (throat_length/2)])
            rotate([-90, 0, 0])
                cylinder(h=gas_port_length, d=gas_port_outer_dia);
        }
        
        // --- 2. Subtracted Inner Void (The fluid path) ---
        union() {
            // Inlet void
            translate([0, 0, -1]) 
                cylinder(h=inlet_length + 1.1, d=inlet_inner_dia);
                
            // Converging Void
            translate([0, 0, inlet_length])
                cylinder(h=converging_length, d1=inlet_inner_dia, d2=throat_dia);
                
            // Throat Void
            translate([0, 0, inlet_length + converging_length - 0.1])
                cylinder(h=throat_length + 0.2, d=throat_dia);
                
            // Diffusing Void
            translate([0, 0, inlet_length + converging_length + throat_length])
                cylinder(h=diffusing_length, d1=throat_dia, d2=diffuser_inner_dia);
                
            // Outlet Void
            translate([0, 0, inlet_length + converging_length + throat_length + diffusing_length - 0.1])
                cylinder(h=outlet_length + 1.1, d=diffuser_inner_dia);
                
            // Gas Injection Void
            translate([0, 0, inlet_length + converging_length + (throat_length/2)])
            rotate([-90, 0, 0])
                cylinder(h=gas_port_length + (throat_dia/2) + wall_thickness + 1, d=gas_port_inner_dia);
        }
    }
}

// Render the module
venturi_nozzle();
