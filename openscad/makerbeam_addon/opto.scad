include <globals.scad>;
include <shaft_mount.scad>;

shaft_r = 3/2;

fin_length = 8;
fin_width = 3;
num_fins = 20;
top_plate_r = 10;
opto_mount_space = 25;

projection() opto_mount_holes() mount_plate();
module opto_mount_holes()
{
    difference()
    {
        child();
        translate([opto_mount_space/2,0,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([-opto_mount_space/2,0,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
    }
}

//top
*projection()
{
top_plate(shaft_r);

//middle
*translate([top_plate_r*2+5,0,0])
    middle_holes(shaft_r) cylinder(r=top_plate_r,h=thickness,center=true);

translate([top_plate_r*4+10,0,0])
    top_plate(shaft_r);

translate([top_plate_r*6+15+fin_length,0,0])
{
    fin_plate();
    top_plate(shaft_r);
}

}
module fin_plate()
{
    for(i=[1:360/num_fins:360])
    {
        rotate([0,0,i])
        translate([top_plate_r+fin_length/2-b_clearance,0,0])
            cube([fin_length,fin_width,thickness],center=true);
    }
}

