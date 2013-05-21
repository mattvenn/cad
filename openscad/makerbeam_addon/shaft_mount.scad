include <globals.scad>;
include <utils.scad>;

top_plate_r = 15;

//top_plate();
//shaft_mount();
module top_plate(center_radius=stepper_shaft_radius)
{
    difference()
    {
        cylinder(r=top_plate_r,h=thickness,center=true);
        holes(center_radius);
    }
}
module middle_holes(center_radius=stepper_shaft_radius)
{
    difference()
    {
        child();

        //screw hole
        translate([top_plate_r/2,0,0])
            cube([top_plate_r,bolt_r*2,thickness*2],center=true);

        //all the rest of the holes
        holes(center_radius);
    }

}

module shaft_mount(center_radius=stepper_shaft_radius)
{
    middle_holes(center_radius) mount_plate();
}

module holes(center_radius=stepper_shaft_radius)
{
    //securing holes
    translate([0,top_plate_r/2,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    translate([0,-top_plate_r/2,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);

    //shaft hole
    cylinder(r=center_radius,h=thickness*2,center=true);

    //nut hole
    translate([top_plate_r/2,0,0])
        cube([m3_nut_depth,m3_nut_flats,thickness*2],center=true);
}
