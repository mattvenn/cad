$fs = 0.5;
$fa = 0.5;
radius= 5;
flat_length =4;
rat = 1.0;
bradius= 7;
length=30;

projection()bell();

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
