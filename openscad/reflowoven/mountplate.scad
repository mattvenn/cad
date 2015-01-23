base_w = 202.0;
base_h = 98.0;
screw_r = 1.5;
w = 216;
h = 113;
th = 3;

ssr_r = 5/2;
ssr_w = 57;

projection()
difference()
{
    base();
    translate([-base_w/2 + 25,0,0])
        ssr();
    translate([-base_w/2 + 25 + 50,0,0])
        ac_dc();
    translate([-base_w/2 + 25 + 50 + 60,0,0])
        arduino();
    translate([-base_w/2 + 25 + 50 + 60 + 50,0,0])
        temp();
}
//arduino();
//temp();

module temp()
{
    temp_w = 20;
    temp_h = 30;
    translate([0,temp_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([-temp_w/2,-temp_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([temp_w/2,-temp_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    
}

module ac_dc()
{
    ac_dc_w = 17.5;
    ac_dc_h = 58;
    translate([ac_dc_w/2,ac_dc_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([-ac_dc_w/2,ac_dc_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([ac_dc_w/2,-ac_dc_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([-ac_dc_w/2,-ac_dc_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
}
module arduino()
{
    translate([-25,-25,0])
    {
    cylinder(r=screw_r,h=th*2,center=true);
    translate([15.2,50.8,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([15.2+27.9+5.1,-1.3,0])
        cylinder(r=screw_r,h=th*2,center=true);
   } 

}

module ssr()
{
    translate([0,ssr_w/2,0])
        cylinder(r=ssr_r,h=th*2,center=true);
    translate([0,-ssr_w/2,0])
        cylinder(r=ssr_r,h=th*2,center=true);
    
}
module base()
{
    difference()
    {
    cube([w,h,th],center=true);
    translate([base_w/2,base_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([-base_w/2,base_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([base_w/2,-base_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    translate([-base_w/2,-base_h/2,0])
        cylinder(r=screw_r,h=th*2,center=true);
    }
}
