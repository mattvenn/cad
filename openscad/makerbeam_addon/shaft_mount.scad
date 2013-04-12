include <globals.scad>;
include <utils.scad>;

top_plate_r = 15;

*projection() top_plate();
projection() shaft_mount();
module top_plate()
{
    difference()
    {
        cylinder(r=top_plate_r,h=thickness,center=true);
        holes();
    }
}
module shaft_mount()
{
    difference()
    {
        mount_plate();

        //screw hole
        translate([stepper_width/2,0,0])
            cube([stepper_width,bolt_r*2,thickness*2],center=true);

        //all the rest of the holes
        holes();
    }
}
module holes()
{
    //securing holes
    translate([0,top_plate_r/2,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    translate([0,-top_plate_r/2,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    //shaft hole
    cylinder(r=stepper_shaft_radius,h=thickness*2,center=true);
    //nut hole
    translate([stepper_width/4,0,0])
        cube([m3_nut_depth,m3_nut_flats,thickness*2],center=true);
}
