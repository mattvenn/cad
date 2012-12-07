include <stepper.scad>;
include <sliders.scad>;
include <globals.scad>;
include <solenoids.scad>;
include <base.scad>;

 translate([0,solenoid_total_y/2-solenoid_min_y_spacing,solenoid_width/2+slider_height/2+slider_solenoid_z_spacing])
  sliders();
solenoids()solenoid();

difference()
{
  translate([base_width/2-solenoid_width/2-edge_margin,base_length/2-edge_margin-solenoid_height,0]) //-solenoid_length/2+thickness/2])
    base();
  solenoids()solenoid_hole();
}

//how we'll export DXFs
*projection(cut = true) stepper_mount();
*rotate([90,0,0])
{
    stepper();
    translate([0,0,stepper_length/2+thickness/2])
        stepper_mount();
}
