include <stepper.scad>;
include <globals.scad>;

//how we'll export DXFs
*projection(cut = true) stepper_mount();

rotate([90,0,0])
{
    stepper();
    translate([0,0,stepper_length/2+thickness/2])
        stepper_mount();
}
