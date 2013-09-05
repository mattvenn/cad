$fs = 0.5;
$fa = 0.5;
cube_h = 6;
top_clearance = 2;
feature_w = 3.5;
base_w = cube_h * 15;
base_h = 2*top_clearance+cube_h+5;
void_w = cube_h * 3;
void_w2 = cube_h * 4;

module all()
{
color("yellow")
    mould();
color("red")
    object();
}

all();

*difference()
{
all();
translate([100,0,0])
cube(200,center=true);
}

module object()
{
    translate([0,0,-cube_h/2-top_clearance])
    {
            sphere(cube_h/2); //cube(cube_h,center=true);
            translate([0,0,-cube_h/2])
            cylinder(r=cube_h/2,h=2*cube_h/2,center=true);
    }
}
module mould()
{
    translate([0,0,-base_h/2])
    difference()
    {
        cube([base_w,base_w,base_h],center=true);
        translate([0,0,base_h/2+void_w/2-cube_h-top_clearance]) //+cube_h+top_clearance])
       cube(void_w,center=true);
        translate([0,0,base_h/2+void_w2/2-(cube_h+top_clearance)/2]) //+cube_h+top_clearance])
        cube(void_w2,center=true);
    }
}
