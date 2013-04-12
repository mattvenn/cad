include <globals.scad>;
include <utils.scad>;
stepper_mount();

module stepper_mount()
{
          difference()
          {
          mount_plate();  
          //bush
          cylinder(r=stepper_bush_radius,h=thickness*2,center=true);
            //mounting holes
        translate([bolt_distance,bolt_distance,0])
          cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([bolt_distance,-bolt_distance,0])
          cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([-bolt_distance,bolt_distance,0])
          cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([-bolt_distance,-bolt_distance,0])
          cylinder(r=bolt_r,h=thickness*2,center=true);
          }
}
