include <stepper.scad>
include <globals.scad>
use <../gondola/gondola.scad>
width  = 500;
height = 500;
depth = 60;
side_thickness = 10;
back_thickness = 5;
stepper_sep = 200;

back_angle = atan(height/depth);
echo("angle=",back_angle);

//left side
translate([-width/2,0,0]) rotate([0,90,0]) wood() side();
//right side
translate([+width/2,0,0]) rotate([0,90,0]) wood() side();
//top
translate([0,-depth/2+side_thickness/2,height/2-depth/2]) rotate([90,0,0]) wood() side();
//bottom
translate([0,+depth/2-side_thickness/2,,-height/2+depth/2]) rotate([90,0,0]) wood() side();
wood() rotate([back_angle,0,0]) back();

translate([stepper_sep/2,0,-height/2+stepper_width/2])rotate([0,90,0])stepper();
translate([-stepper_sep/2,0,-height/2+stepper_width/2])rotate([0,-90,0])stepper();
translate([0,-thickness,0])rotate([back_angle,0,0]) made_gondola();
module wood()
{
    color("brown")
        child();
}

module back()
{
    cube([width,height,back_thickness],center=true);
}
module side()
{
    cube([height,depth,side_thickness],center=true);
}
