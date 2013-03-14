$fa=1;
$fs=0.3;

tape_reel_r = 76 / 2;
tape_reel_h = 30;
thickness=3;

//push fit dimensions
push_width=10;
push_top_height=5;
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
projection()
{
translate([push_width,0,0]) push(0.1);
translate([push_width*3,0,0]) push(0.2);
translate([push_width*5,0,0]) push(0.3);
translate([push_width*7,0,0]) push(0.4);
}
//projection()
//push_buttons();
//projection()
//led_board();

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
module push(bump_offset=0.2)
{

    push_top_clip_h = 2;
    slot_width = 1;
    bump_r = 1.0;
    difference()
    {
    union()
    {
    roundedBox([push_width*1.5,push_top_height,thickness],1,true);
    translate([0,push_top_height/2+thickness/2,0])
        cube([push_width,thickness*1.5,thickness],center=true);
    translate([0,push_top_height/2+thickness-bump_offset+push_top_clip_h/2,0])
    //blip on the end
    roundedBox([push_width*1.1,push_top_clip_h,thickness],bump_r,true);
    }
    translate([0,thickness/2+thickness/2+bump_offset,0])
        hull()
        {
            wire_hole(thin_wire_r);
            translate([0,thickness*2,0])
            wire_hole(double_wire_r);
        }
    }

}

module opush(slope=slope)
{
    difference()
    {
        union()
        {
            roundedBox([push_width*1.5,push_top_height,thickness],1,true);
            hull()
            {
                cube([push_width*(1+slope),push_top_height,thickness],center=true);
                translate([0,thickness*2,0])
                cube([push_width*(1-slope),5,thickness],center=true);
            }
        }
        translate([0,push_top_height/2+thickness,0])
        cylinder(r=double_wire_r,h=thickness*2,center=true);
    }
}

module push_hole()
{
    cube([push_width,thickness,thickness*2],center=true);
    hull()
    {
        translate([0,thickness/2+thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
        translate([0,-thickness/2-thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
    }
}
