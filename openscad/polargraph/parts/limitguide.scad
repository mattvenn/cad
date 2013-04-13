include <../case/stepper.scad>
include <../case/globals.scad>
include </home/mattvenn/cad/MCAD/shapes.scad>
include <../tab_creator.scad>

//pinch height is distance between where the wire is pinched for limits, and the shaft of the motor
pinch_height = 60;
pillar_height = 6; //standard spacers
hole_clearance = 5; //min distance a hole will be made from an edge
//measure all these
    switch_hole_x = 6;
    switch_hole_y = -25;
    switch_offset_x = -15;
    switch_offset_y = -10;
    switch_thickness = 8; //thickkness of switch
    switch_spring_x = 6; //distance from tip of spring to body of switch
    switch_offset_z = pillar_height; //height above the surface we want the switch
    switch_spring_y = -15; //from top hole to where the spring comes out

guide_height = switch_offset_z+hole_clearance;
//just top width
guide_width = stepper_width/2 + switch_spring_x;
mount_length = stepper_height / 2 + pinch_height + hole_clearance;
pinch_y = -mount_length/2+stepper_width/2+pinch_height;
guide_y = pinch_y + switch_offset_y + switch_spring_y;

//mount plate
module made_guide_plate()
{
translate([0,mount_length/2-stepper_width/2+guide_y,guide_height/2+thickness/2])
    rotate([90,0,0])
        guide_plate();
}

//mount plate
difference()
{
translate([0,mount_length/2-stepper_width/2,0])
    mount_plate();

translate([0,0,-stepper_height/2-thickness/2])
    stepper();
    made_guide_plate();
}
module mount_plate()
{
    difference()
    {
    roundedBox(stepper_width,mount_length,thickness,round_radius);
    translate([m3_bolt_r,pinch_y,0])
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    translate([-m3_bolt_r+switch_offset_x,pinch_y+switch_offset_y,0])
        switch_holes();
    }
}
module guide_plate()
{
    difference()
    {
    union()
    {
    //main part
    cube([stepper_width,guide_height,thickness],center=true);

    //extra bit that has the hole
    translate([(stepper_width-guide_width)/2,switch_offset_z+switch_thickness/2,0])
    cube([guide_width,guide_height,thickness],center=true);

    translate([0,-guide_height/2-thickness/2,0])
    cube([stepper_width*0.8,thickness,thickness],center=true);
    }
    //guide hole
    //shuld be switch_offset_z + switch_thickness above the 0
    translate([0,switch_offset_z+switch_thickness/2,0])
    cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    }

}
//draws from top left hole
module switch_holes()
{
    cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    translate([switch_hole_x,switch_hole_y,0])
        cylinder(r=m3_bolt_r,h=thickness*2,center=true);
    cylinder(r=m3_bolt_r,h=thickness*2,center=true);
}
