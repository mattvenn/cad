/*
needs a different, easier, more reliable plug()
*/
//$fa=15;
$fs=0.6;

tape_reel_r = 77 / 2;
tape_reel_h = 30;
thickness=3;
clearance = 0.1; //laser clearance

//plug fit dimensions
plug_width=10;
plug_clip_width=plug_width+2;
plug_top_height=5;
plug_clip_height=5;
plug_slot_offset=0.5; //moves the end of the slot away from the top
plug_spacing=thickness-0.2; //how close the ends of the clip are to the top of the plug
plug_articulation=2; //how big the articulation point is

//wire dimensions
thin_wire_r = 1.1/2;
double_wire_r = 1.6/2;
mobile_wire_r = 3/2;


include </home/matthew/work/cad/MCAD/boxes.scad>;

resistor_space = 20;
double_wire_space = 5;

module plugs()
{
    translate([tape_reel_r-plug_width,20,0])
    plug();
    translate([-tape_reel_r+plug_width,20,0])
    plug();
}
*projection()
{
    translate([0,0,0]) plug();
    translate([plug_width*2,0,0]) plug();
    *translate([plug_width*5,0,0]) plug();
    *translate([plug_width*7,0,0]) plug();
}
*projection() translate([0,20,0]) test_board();

//projection()
//projection()
{
    plugs();
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
            plug_hole();
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
        plug_hole();
        translate([0,resistor_space,0])
            plug_hole();
        translate([plug_width,resistor_space,0])
            double_wire();
        translate([-plug_width,resistor_space,0])
            double_wire();
        for(i=[0:2])
        {
            translate([i*mobile_wire_r*4+plug_width*1.5,-tape_reel_h/4,0])
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
        roundedBox([plug_width*3,resistor_space*2,thickness],4,true);
        roundedBox([tape_reel_r*2,tape_reel_h,thickness],4,true);
    }
}
module plug()
{
    difference()
    {
        union()
        {
        //top
        roundedBox([plug_width*1.5,plug_top_height,thickness],1,true);

        //middle
        translate([0,plug_top_height/2+thickness/2,0])
            cube([plug_width,thickness,thickness],center=true);

        //clip
        translate([0,plug_top_height/2+plug_spacing,0])
        hull()
            {
                cube([plug_clip_width,0.1,thickness],center=true);
                translate([0,plug_clip_height,0])
                cube([plug_width-clearance,0.1,thickness],center=true);
            }
        }

    //the bottom slot
    translate([0,plug_top_height/2+plug_slot_offset+thin_wire_r,0])
        hull()
        {
            wire_hole(thin_wire_r);
            translate([0,plug_spacing+plug_clip_height,0])
            wire_hole(double_wire_r);
        }
    //the top slot
    translate([0,plug_top_height/2+plug_slot_offset-plug_articulation-thin_wire_r,0])
        hull()
        {
            wire_hole(thin_wire_r);
            translate([0,-plug_top_height,0])
            wire_hole(double_wire_r);
        }
    }
}

module plug_hole()
{
    cube([plug_width-clearance,thickness-clearance,thickness*2],center=true);
    hull()
    {
        translate([0,thickness/2+thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
        translate([0,-thickness/2-thin_wire_r,0])
            cylinder(r=thin_wire_r,h=thickness*2,center=true);
    }
}
