include <../case/stepper.scad>
include <../case/globals.scad>
include </home/mattvenn/cad/MCAD/shapes.scad>
include <../tab_creator.scad>

//pinch height is distance between where the wire is pinched for limits, and the shaft of the motor
pinch_height = 60;
guide_hole_r = 0.5;
pinch_x = 1; //x offset for the pinch
pillar_height = 8; //standard spacers
hole_clearance = 5; //min distance a hole will be made from an edge
//switch datasheet: http://www.newark.com/pdfs/datasheets/Honeywell_Sensing/V15.pdf
    switch_hole_x = 10.3; //distance between holes
    switch_hole_y = 22.2; //distance between holes
    switch_offset_x = 16; //20.6; //opearating position - distance between top left hole and when the switch turns on, from website: http://sensing.honeywell.com/product%20page?pr_id=45588
    switch_offset_y = switch_hole_y - 20.6; //y distance from edge of roller to left hole , this from datasheet
    switch_hole_offset_x = 2.8; //x distance from the edge of the switch to the center of the mounting hole
    switch_thickness = 10.3; //thickkness of switch
    switch_offset_z = pillar_height; //height above the surface we want the switch
    

//middle part of the guide height
guide_height = switch_offset_z+hole_clearance;
//top of the guide width
guide_width = stepper_width/2 + switch_offset_x - (pinch_x+switch_hole_x+switch_hole_offset_x);
mount_length = stepper_height / 2 + pinch_height + hole_clearance;
pinch_y = -mount_length/2+stepper_width/2+pinch_height;
guide_y = pinch_y + switch_offset_y - switch_hole_y /2;

//made_guide_plate();
//projection()guide_plate();
projection()made_plate();


//mount plate
module made_guide_plate()
{
translate([0,mount_length/2-stepper_width/2+guide_y,guide_height/2+thickness/2])
    rotate([90,0,0])
        guide_plate(true);
}

module made_plate()
{
//mount plate
difference()
{
translate([0,mount_length/2-stepper_width/2,0])
    mount_plate();

translate([0,0,-stepper_height/2-thickness/2])
    stepper();
    made_guide_plate();
}
}
module mount_plate()
{
    difference()
    {
    roundedBox(stepper_width,mount_length,thickness,round_radius);
    //hole for mounting the roller
    translate([pinch_x+m3_bolt_r,pinch_y,0])
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    translate([pinch_x-m3_bolt_r-switch_offset_x,pinch_y+switch_offset_y,0])
        switch_holes();
    }
}
module guide_plate(boolean)
{
    difference()
    {
    union()
    {
    //main part
    cube([stepper_width,guide_height,thickness],center=true);

    //extra bit that has the hole
    translate([(stepper_width-guide_width)/2,guide_height,0])
    cube([guide_width,guide_height,thickness],center=true);

    //the slot
    translate([0,-guide_height/2-thickness/2,0])
    if( boolean )
        cube([stepper_width*0.8,2*thickness,thickness],center=true);
    else
        cube([stepper_width*0.8,thickness,thickness],center=true);
    }
    //guide hole
    //shuld be switch_offset_z + switch_thickness above the 0
    translate([0,switch_offset_z+switch_thickness/2,0])
    cylinder(r=guide_hole_r,h=thickness*2,center=true);
    }

}
//draws from top left hole
module switch_holes()
{
    cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    translate([switch_hole_x,-switch_hole_y,0])
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
}
