$fs = 0.5;
$fa = 0.5;
radius= 5;
flat_length =2;
rat = 1.0;
bradius= 7;
length=30;
top_clearance = 2;
base_w = 100;
base_h = top_clearance+bradius+flat_length;
void_w = bradius*6;
void_l = length + 5* bradius;

mould();
translate([0,bradius/2,0])flat_bell();
//projection(cut=true)bell();

module mould()
{
     difference()
    {
        cube([base_w,base_w,2*base_h],center=true);
        translate([0,0,+void_w/2])
        union()
        {
        translate([0,0,6])
        cube([void_w+6,void_l+6,void_w],center=true);
        cube([void_w,void_l,void_w],center=true);
        }
    }
}

module flat_bell()
{
translate([0,0,flat_length])
{
difference()
{
bell();
translate([0,0,-100/2])
cube([100,100,100],center=true);
}
}
linear_extrude( height=flat_length) import("bellend.dxf");
}

module bell()
{
rotate([90,0,0])
    cylinder(r=radius,h=length,center=true);
//bell
translate([0,length/2,0])
    sphere(r=radius);
translate([0,-length/2,0])
    sphere(r=radius);
//balls
translate([rat*bradius,-length/2-bradius/2,0])
    sphere(r=bradius);
translate([rat*-bradius,-length/2-bradius/2,0])
{
difference()
{
    sphere(r=bradius);
    cylinder(r=3,h=100,center=true);
}
}
}
