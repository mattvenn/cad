///////////////////////////////////////////////
//simple case to show boolean method of creating parts for laser/cnc cutting
//Matt Venn 2013, releases under an open source license.
//mattvenn.net

//smooth curves
$fs=0.5;

//fundamental measurements, these are things we can't change
button_r = 7;
bolt_r = 3;

//how big we want the case
width=100;
height=40;
length=80;

//some adjustable parameters
thickness = 5; //material thickness
spacing = 15;

///////////////////////////////////////////////
//show where the bits of the case are
build_front();
build_back();
build_side_l();
build_side_r();
//build_buttons();
//build_bolts();

//to make dxfs, uncomment these
//projection() build_front();
//projection() build_back();
//projection() rotate([0,90,0]) build_side_l();

///////////////////////////////////////////////
//the models: these are built at the 0,0,0 point and are all centered

module short_side()
{
   slot_length = length / 5;
   cube([height-2*thickness,length,thickness],center=true); 
   translate([0,length/2-slot_length/2,0])
       cube([height+0.1,slot_length,thickness],center=true);
   translate([0,-length/2+slot_length/2,0])
       cube([height+0.1,slot_length,thickness],center=true);
}

module front_or_back()
{
    mink_r = thickness/2;
    minkowski()
    {
        //have to take into account the radius of the cylinder, so subtract from width and length
        cube([width-mink_r*2,length-mink_r*2,thickness],center=true);
        cylinder(r=thickness/2,h=0.01);
    }
}

///////////////////////////////////////////////
//the models moved to the correct position, and with intersecting parts cut out of them using difference()
module build_front()
{
    difference()
    {
        translate([0,0,height/2-thickness/2])
            front_or_back();
        build_side_r();
        build_side_l();
        build_buttons();
        build_bolts();
    }
}
module build_back()
{
    difference()
    {
        translate([0,0,-height/2+thickness/2])
            front_or_back();
        build_side_r();
        build_side_l();
        build_bolts();
    }
}

module build_side_r()
{
    color("grey")
        translate([+width/2-spacing,0,0])
            rotate([0,90,0])
                short_side();
}

module build_side_l()
{
    color("grey")
        translate([-width/2+spacing,0,0])
            rotate([0,90,0])
                short_side();
}

///////////////////////////////////////////////
//so simple and we're never going to cut these parts, that we combine the build and model in one module
module build_buttons()
{
    color("blue")
    {
        translate([-width/6,0,height/2])
            cylinder(r=10,h=20,center=true);
        translate([+width/6,0,height/2])
            cylinder(r=10,h=20,center=true);
    }
}

module build_bolts()
{
    translate([-width/2+spacing/2,-length/2+spacing/2,0])
        cylinder(r=bolt_r,h=height*1.5,center=true);
    translate([+width/2-spacing/2,-length/2+spacing/2,0])
        cylinder(r=bolt_r,h=height*1.5,center=true);
    translate([-width/2+spacing/2,+length/2-spacing/2,0])
        cylinder(r=bolt_r,h=height*1.5,center=true);
    translate([+width/2-spacing/2,+length/2-spacing/2,0])
        cylinder(r=bolt_r,h=height*1.5,center=true);
}
