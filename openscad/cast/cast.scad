cube_h = 6;
top_clearance = 2;
feature_w = 3.5;
base_w = cube_h * 10;
base_h = 2*top_clearance+cube_h;
void_w = cube_h * 3;

color("blue")
    mould();
color("red")
    object();

module object()
{
    translate([0,0,-cube_h/2-top_clearance])
    {
        difference()
        {
            cube(cube_h,center=true);
            translate([0,0,cube_h/2])
            cube([feature_w,cube_h*2,feature_w],center=true);
        }
    }
}
module mould()
{
    translate([0,0,-base_h/2])
    difference()
    {
        cube([base_w,base_w,base_h],center=true);
        translate([0,0,-base_h/2+void_w/2+top_clearance])
        cube(void_w,center=true);
    }
}
