include <globals.scad>;
include <utils.scad>;
include </home/mattvenn/cad/MCAD/shapes.scad>;

projection()servo_mount();
module servo_mount()
{
    mount_w=4*makerbeam_w;
    difference()
    {
    roundedBox(mount_w,mount_w,thickness,round_radius);
    //mount holes
    translate([-mount_w/2,-mount_w/2+makerbeam_w/2,0])
    {
        translate([makerbeam_w/2,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);

        translate([makerbeam_w/2+3*makerbeam_w,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    }

    translate([-mount_w/2,+mount_w/2-makerbeam_w/2,0])
    {
        translate([makerbeam_w/2,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);

        translate([makerbeam_w/2+3*makerbeam_w,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    }
    //servo cutout
    cube([servo_length,servo_width,thickness*2],center=true);

    //wire hole
    translate([servo_length/2,0,0])
        cube([2,3,thickness*2],center=true);

    //mount holes
    translate([servo_hole_space/2,0,0])
        cylinder(r=servo_bolt_r,h=thickness*2,center=true);
    translate([-servo_hole_space/2,0,0])
        cylinder(r=servo_bolt_r,h=thickness*2,center=true);

    }
}
