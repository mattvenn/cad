include <globals.scad>;
include </home/mattvenn/cad/MCAD/shapes.scad>;
module mount_plate()
{
          side_s = makerbeam_w/2;
          difference()
          {

            roundedBox(stepper_width,base_height+0.1,thickness,round_radius);
          translate([stepper_width/2-side_s,base_height/2-makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([-stepper_width/2+side_s,base_height/2-makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([stepper_width/2-side_s,-base_height/2+makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([-stepper_width/2+side_s,-base_height/2+makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
        }            
}
