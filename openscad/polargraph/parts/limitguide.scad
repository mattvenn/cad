include <../case/stepper.scad>
include <../case/globals.scad>
include </home/mattvenn/cad/MCAD/shapes.scad>

edge_clearance = 3;
//m3 plastic pcb spacer
sleeve_r = 5/2;
//switch datasheet: http://www.newark.com/pdfs/datasheets/Honeywell_Sensing/V15.pdf
switch_hole_x = 10.3; //distance between holes
switch_hole_y = 22.2; //distance between holes
switch_offset_x = 20.6 + sleeve_r; //opearating position - distance between top left hole and when the switch turns on, from website: http://sensing.honeywell.com/product%20page?pr_id=45588
switch_offset_y = switch_hole_y - 20.6; //y distance from edge of roller to left hole , this from datasheet
switch_length = 29;

//calculated
width = switch_offset_x + edge_clearance * 2;
height = switch_length;

projection()
mount_plate();

module mount_plate()
{
    difference()
    {
    roundedBox(width,height,thickness,round_radius);
    //hole for mounting the roller
    translate([width/2-edge_clearance,height/2-edge_clearance-m3_bolt_r,0])
    {
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
        //switch mount holes
        translate([-switch_offset_x,switch_offset_y,0])
            switch_holes();
    }
    translate([5,-height/2-edge_clearance*2-m3_bolt_r*2,-thickness])
        cube([width,height,thickness*2]);
    }
}
//draws from top left hole
module switch_holes()
{
    cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    translate([switch_hole_x,-switch_hole_y,0])
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
}
