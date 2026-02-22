/*
  Symbiotic Factory - Module I (SUN)
  Hardware: Parametric Interfacial Solar Steam Generator (ISSG) Housing
  License: CERN-OHL-S
  
  Description:
  This OpenSCAD script generates a customizable housing for the Plasmonic Biochar Sponge.
  It is designed to float on top of saltwater/wastewater.
  - The central "Sponge Tray" allows capillary wicking of water from below.
  - The angled "Condensation Roof" lets sunlight/UV in to power the LSPR evaporation,
    catches the rising steam, and channels the pure condensate into...
  - The "Distillate Gutters", which route the freshwater out to the WATER module.
*/

// --- Core Parameters (Customize to match your local saltwater tank dimensions) ---
$fn = 60; // Curve resolution

// Base Dimensions
tank_inner_width = 300.0;   // Inner width of your main saltwater reservoir (mm)
tank_inner_length = 400.0;  // Inner length of your main saltwater reservoir (mm)
tolerance_gap = 10.0;       // Gap around the housing so it floats freely (mm)

// Housing Dimensions
housing_w = tank_inner_width - (tolerance_gap * 2);
housing_l = tank_inner_length - (tolerance_gap * 2);
housing_wall_thickness = 4.0;
housing_base_height = 40.0; // Deep enough to act as a boat

// Sponge Tray (The central hole for the biochar)
// We leave a lip around the edge so the sponge doesn't fall through
tray_lip_width = 20.0;
sponge_w = housing_w - (tray_lip_width * 2) - (housing_wall_thickness * 2);
sponge_l = housing_l - (tray_lip_width * 2) - (housing_wall_thickness * 2);

// Condensation Gutter (Interior perimeter)
gutter_width = 15.0;
gutter_depth = 10.0;

// Roof Angles (Standard is 30-45 degrees to ensure drop roll-off before falling back in)
roof_angle = 35.0;
roof_overhang = 5.0;

// Output Port (To attach tubing to the algae cycloreactors)
output_pipe_outer_dia = 8.0;
output_pipe_inner_dia = 5.0;

// --- Module Generation ---

module floating_base() {
    difference() {
        // Main buoyant hull
        cube([housing_w, housing_l, housing_base_height]);
        
        // Hollow out the interior (leaving structural walls and the bottom lip)
        translate([housing_wall_thickness, housing_wall_thickness, housing_wall_thickness])
            cube([housing_w - (housing_wall_thickness*2), 
                  housing_l - (housing_wall_thickness*2), 
                  housing_base_height]);
                  
        // Cut out the central hole for the capillary sponge to touch the water
        translate([tray_lip_width + housing_wall_thickness, 
                   tray_lip_width + housing_wall_thickness, 
                   -1])
            cube([sponge_w, sponge_l, housing_wall_thickness + 2]);
    }
}

module condensation_gutters() {
    // Generate the internal trough that catches water rolling off the roof
    translate([housing_wall_thickness, housing_wall_thickness, housing_base_height - gutter_depth])
    difference() {
        // Solid rim
        cube([housing_w - (housing_wall_thickness*2), 
              housing_l - (housing_wall_thickness*2), 
              gutter_depth]);
              
        // Hollowed trough
        translate([gutter_width, gutter_width, 0])
             cube([housing_w - (housing_wall_thickness*2) - (gutter_width*2), 
                   housing_l - (housing_wall_thickness*2) - (gutter_width*2), 
                   gutter_depth + 1]);
    }
}

module output_spigot() {
    // Connects to the gutter to drain the freshwater
    translate([housing_w - housing_wall_thickness, 
               housing_l / 2, 
               housing_base_height - (gutter_depth / 2)])
    rotate([0, 90, 0])
    difference() {
        cylinder(h=20, d=output_pipe_outer_dia);
        translate([0,0,-1]) cylinder(h=22, d=output_pipe_inner_dia);
    }
    
    // Pierce the hull wall into the gutter
    translate([housing_w - housing_wall_thickness - gutter_width - 1, 
               (housing_l / 2) - (output_pipe_inner_dia / 2), 
               housing_base_height - (gutter_depth / 2) - (output_pipe_inner_dia / 2)])
        cube([gutter_width + 2, output_pipe_inner_dia, output_pipe_inner_dia]);
}

// NOTE: The transparent roof is usually cut from a flat sheet of Polycarbonate or Acrylic,
// not 3D printed (since FDM printing is never truly optically clear).
// We provide a solid 3D model here just as a cutting template or assembly reference.
module acrylic_roof_template() {
    roof_height = tan(roof_angle) * (housing_w / 2);
    
    // Render as a translucent blue body to indicate glass/acrylic
    color([0.2, 0.5, 0.9, 0.4]) 
    translate([-roof_overhang, 0, housing_base_height])
    rotate([0, 0, 0])
    // Generate a prism (A-frame roof)
    polyhedron(
        points=[
            [0, -roof_overhang, 0], [housing_w + (roof_overhang*2), -roof_overhang, 0], 
            [housing_w + (roof_overhang*2), housing_l + (roof_overhang*2), 0], [0, housing_l + (roof_overhang*2), 0], // Base corners
            [(housing_w/2) + roof_overhang, -roof_overhang, roof_height], [(housing_w/2) + roof_overhang, housing_l + (roof_overhang*2), roof_height]  // Peak line
        ],
        faces=[
            [0,3,2,1], // Bottom
            [0,1,4],   // Front Triangle
            [3,0,4,5], // Left slope
            [1,2,5,4], // Right slope
            [2,3,5]    // Back Triangle
        ]
    );
}

// Assemble the printable parts
module export_printable_housing() {
    union() {
        difference() {
            floating_base();
            output_spigot(); // Cut hole for spigot
        }
        condensation_gutters();
        output_spigot();
    }
}

// Choose what to render (Uncomment for export)
export_printable_housing();

// Display the transparent roof for assembly context (Do not export this for 3D printing)
acrylic_roof_template();
