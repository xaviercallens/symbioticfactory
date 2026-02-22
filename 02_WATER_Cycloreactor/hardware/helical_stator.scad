/*
  Symbiotic Factory - Module II (WATER)
  Hardware: Parametric Helical Cyclonic Stator
  License: CERN-OHL-S
  
  Description:
  This static baffle sits inside the vertical algal photobioreactor tubes. 
  When the fluid is pumped from below, the helical fins induce a cyclonic vortex. 
  This physically forces the microalgae into rapid light/dark (L/D) cycles 
  between the illuminated transparent edges and the dark central core. 
  By matching the rotational frequency to the Plastoquinone pool turnover rate (~10-50Hz), 
  we mathematically bypass photoinhibition.
*/

// --- Core Parameters (Customize for your transparent Acrylic/PC tube) ---
$fn = 100;

reactor_inner_diameter = 90.0; // The inner diameter of your main reactor tube (mm)
tolerance = 1.0;               // Clearance to easily slide the stator inside (mm)

shaft_diameter = 15.0;         // Central support rod diameter (mm)
stator_length = 200.0;         // Height of a single printable stator segment (mm)

blade_thickness = 2.5;         // Thickness of the helical fins (mm)
num_blades = 3;                // Number of twisting fins (3 provides excellent shear)
twist_angle = 360;             // Total degrees the blades twist over the length. Higher = tighter vortex.

// Calculate active working bounds
working_diameter = reactor_inner_diameter - tolerance;

// --- Generated Helical Baffle ---
module helical_stator() {
    union() {
        // Central Shaft
        cylinder(h=stator_length, d=shaft_diameter, center=false);
        
        // Generate twisting blades
        linear_extrude(height=stator_length, twist=-twist_angle, slices=stator_length/2, convexity=10) {
            for(i = [0 : num_blades-1]) {
                rotate([0, 0, (360/num_blades) * i]) {
                    // Profile to extrude into a blade
                    polygon(points=[
                        [-(blade_thickness/2), (shaft_diameter/2) - 1],
                        [(blade_thickness/2), (shaft_diameter/2) - 1],
                        [(blade_thickness/4), (working_diameter/2)],
                        [-(blade_thickness/4), (working_diameter/2)]
                    ]);
                }
            }
        }
    }
}

// --- Interlocking mechanism for stacking multiple segments ---
// Adding a male peg to the top
module stacking_peg() {
    translate([0, 0, stator_length])
    cylinder(h=15.0, d=shaft_diameter - 2.0);
}

// Adding a female socket to the bottom
module stacking_socket() {
    translate([0, 0, -0.1])
    cylinder(h=15.2, d=shaft_diameter - 1.5);
}

module printable_segment() {
    difference() {
        union() {
            helical_stator();
            stacking_peg();
        }
        stacking_socket();
    }
}

// Render the module
printable_segment();
