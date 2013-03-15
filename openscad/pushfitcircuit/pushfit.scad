/*
needs a different, easier, more reliable push()
*/
//$fa=15;
$fs=0.6;

tape_reel_r = 77 / 2;
tape_reel_h = 30;
thickness=3;
clearance = 0.1; //laser clearance

//push fit dimensions
push_width=10;
push_top_height=5;
push_clip_height=5;
push_top_space=thickness-0.3; //how close the ends of the clip are to the top of the plug
slope = 0.12; //this is half the offset between top and bottom of the slope

//wire dimensions
thin_wire_r = 1.1/2;
double_wire_r = 1.6/2;
mobile_wire_r = 3/2;


include </home/matthew/work/cad/MCAD/boxes.scad>;

resistor_space = 20;
double_wire_space = 5;

module push_buttons()
{
    translate([tape_reel_r-push_width,20,0])
    push();
    translate([-tape_reel_r+push_width,20,0])
    push();
}
*projection()
{
    translate([0,0,0]) push();
    translate([push_width*2,0,0]) push();
    *translate([push_width*5,0,0]) push();
    *translate([push_width*7,0,0]) push();
}
*projection() translate([0,20,0]) test_board();

//projection()
//projection()
{
    push_buttons();
    led_board();
}

module test_board()
{
    for(i=[0:1])
    {
        translate([i*15,0,0])
        difference()
        {
            cube([20,20,thickness],center=true);
            push_hole();
        }
    }
}
module double_wire(wire_r=thin_wire_r,space=double_wire_space)
{
    translate([0,space/2,0])
        wire_hole(wire_r);
    translate([0,-space/2,0])
        wire_hole(wire_r);
}

module led_board()
{
    color("grey")
    difference()
    {
        board();
        push_hole();
        translate([0,resistor_space,0])
            push_hole();
        translate([push_width,resistor_space,0])
            double_wire();
        translate([-push_width,resistor_space,0])
            double_wire();
        for(i=[0:2])
        {
            translate([i*mobile_wire_r*4+push_width*1.5,-tape_reel_h/4,0])
                wire_hole(mobile_wire_r);
        }
    }
}
module wire_hole(wire_r)
{
    color("yellow")
    cylinder(r=wire_r,h=thickness*2,center=true);
}
    
module board()
{
    union()
    {
        translate([0,resistor_space/2,0])
        roundedBox([push_width*3,resistor_space*2,thickness],4,true);
        roundedBox([tape_reel_r*2,tape_reel_h,thickness],4,true);
    }
}
module push(bump_width=1.15)
{
    slot_offset=0.5;
    difference()
    {
    union()
    {
    //top
    roundedBox([push_width*1.5,push_top_height,thickness],1,true);

    //middle
    translate([0,push_top_height/2+thickness/2,0])
        cube([push_width,thickness,thickness],center=true);

    //clip
    translate([0,push_top_height/2+push_top_space,0])
    hull()
        {
            cube([push_width+bump_width,0.1,thickness],center=true);
            translate([0,push_clip_height,0])
            cube([push_width*0.9,0.1,thickness],center=true);
        }
    }

    //the slot
    translate([0,push_top_height/2+slot_offset,0])
        hull()
        {
            wire_hole(thin_wire_r);
            translate([0,push_top_space+push_clip_height,0])
            wire_hole(double_wire_r);
        }
    }
}

module push_hole()
{
    cube([push_width-clearance,thickness-clearance,thickness*2],center=true);
    hull()
    {
        translate([0,thickness/2+thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
        translate([0,-thickness/2-thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
    }
}
