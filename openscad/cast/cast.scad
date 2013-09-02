/*
y = 6.01 - micro
x = 6.00 - micro
z = 5.53 - micro
f_w = 3.5 - vernier
f_d = 2.7 - vernier

but something has gone wrong, because void_w is 24 not 18.
And cube height from the bottom of the void is not 6, it's more like 5.3.
And the feature on the top is 2.7 not 3.5/2=1.75
*/
cube_h = 6;
top_clearance = 2;
feature_w = 3.5;
base_w = cube_h * 10;
base_h = 2*top_clearance+cube_h;
void_w = cube_h * 3;

*color("blue")
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
            #cube([feature_w,cube_h*2,feature_w],center=true);
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
