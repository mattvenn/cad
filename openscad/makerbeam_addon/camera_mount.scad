include <globals.scad>;
include <utils.scad>;
include </home/mattvenn/cad/MCAD/shapes.scad>;
camera_mount();
tripod_screw_r = 6.25/2;
module camera_mount()
{
    mount_w=4*makerbeam_w;
    difference()
    {
    roundedBox(mount_w,mount_w,thickness,round_radius);
    translate([-mount_w/2,-mount_w/2+makerbeam_w/2,0])
    {
        translate([makerbeam_w/2,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([makerbeam_w/2+makerbeam_w,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
        translate([makerbeam_w/2+3*makerbeam_w,0,0])
        cylinder(r=bolt_r,h=thickness*2,center=true);
    }
    //tripod
    translate([0,makerbeam_w,0])
        cylinder(r=tripod_screw_r,h=thickness*2,center=true);
    }


}
