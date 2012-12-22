thickness=3;
clearance=1.1;
bolt_radius=1.5;
bolt_length=15;
nut_width=5;
nut_height=2.5;
size=[40,40,thickness];

//assume internal size is the most important one, so we'll add material
module make_tab_slots(size,tab_edge,thickness,bolt_radius)
{
    if(tab_edge[0]) // x
    difference()
    {
        child();
        //the slots
        translate([size[0]/2-thickness,size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([size[0]/2-thickness,-size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([-size[0]/2+thickness,size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([-size[0]/2+thickness,-size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        //the holes
        translate([-size[0]/2+thickness,0,0])
            scale(clearance)
                cylinder(h=thickness*2,r=bolt_radius,center=true,$fn=20);
        translate([+size[0]/2-thickness,0,0])
            scale(clearance)
                cylinder(h=thickness*2,r=bolt_radius,center=true,$fn=20);
    }
    if(tab_edge[1]) // x
    difference()
    {
        child();
        //the slots
        translate([size[0]/2-thickness,size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([size[0]/2-thickness,-size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([-size[0]/2+thickness,size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        translate([-size[0]/2+thickness,-size[1]/4,0])
            scale(clearance)
                cube([thickness,size[1]/4,size[2]*2],center=true);
        //the holes
        translate([-size[0]/2+thickness,0,0])
            scale(clearance)
                cylinder(h=thickness*2,r=bolt_radius,center=true,$fn=20);
        translate([+size[0]/2-thickness,0,0])
            scale(clearance)
                cylinder(h=thickness*2,r=bolt_radius,center=true,$fn=20);
    }
}

module make_tabs(size,tab_edge,thickness,bolt_radius,bolt_length,nut_width,nut_height)
{
    if(tab_edge[0]) // x
    assign(bolt_slot_length=bolt_length-thickness)
    difference()
    {
        child();
        //the slots for the bolt 
        echo(bolt_slot_length);
        translate([size[0]/2-bolt_slot_length/2+0.1,0,0])
            cube([bolt_slot_length,bolt_radius*2,thickness*2],center=true);
        translate([-size[0]/2+bolt_slot_length/2-0.1,0,0])
            cube([bolt_slot_length,bolt_radius*2,thickness*2],center=true);
        //the slots for the captive nuts
        translate([size[0]/2-bolt_slot_length/2+0.1,0,0])
            cube([nut_height,nut_width,thickness*2],center=true);
        translate([-size[0]/2+bolt_slot_length/2-0.1,0,0])
            cube([nut_height,nut_width,thickness*2],center=true);
    }
    //the tabs
    translate([size[0]/2+thickness/2,size[1]/4,0])
        cube([thickness,size[1]/4,size[2]],center=true);
    translate([size[0]/2+thickness/2,-size[1]/4,0])
        cube([thickness,size[1]/4,size[2]],center=true);
    translate([-size[0]/2-thickness/2,size[1]/4,0])
        cube([thickness,size[1]/4,size[2]],center=true);
    translate([-size[0]/2-thickness/2,-size[1]/4,0])
        cube([thickness,size[1]/4,size[2]],center=true);
}
/*
translate([50,0,0])
    make_tab_slots(size,[1,0,0],thickness,bolt_radius)
        cube(size,center=true);

make_tabs(size,[1,0,0],thickness,bolt_radius,bolt_length,nut_width,nut_height)
    cube(size,center=true);
    */
