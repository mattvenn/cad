button_d = 27.8;
iec_w = 26.6;
iec_h = 19;
iec_hole_w = 40;

mains_w = 65;
mains_h = 65;
mains_hole_w = 60;
mains_hole_sur = 10;
mains_screw_r = 3.5/2;
th = 5;

lcd_w = 27;
lcd_h = 70;
lcd_hole_w = 75;
lcd_hole_h = 31;
lcd_hole_r = 1.5;

lid_w=210;
lid_h=105;

//lid();
projection()
{
translate([-50,0,0])
mains();
translate([20,25,0])
    iec();
translate([70,25,0])
    button();
translate([45,-15,0])
    lcd();
}
module lid()
{
    color("gray")
    cube([lid_w,lid_h,th/2],center=true);
}
module lcd()
{
    cube([lcd_h,lcd_w,th],center=true);
    translate([lcd_hole_w/2,lcd_hole_h/2,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
    translate([-lcd_hole_w/2,lcd_hole_h/2,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
    translate([lcd_hole_w/2,-lcd_hole_h/2,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
    translate([-lcd_hole_w/2,-lcd_hole_h/2,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);

}
module button()
{
    cylinder(r=button_d/2,h=th,center=true);
}
module iec()
{

    cube([iec_w,iec_h,th],center=true);
    translate([iec_hole_w/2,0,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
    translate([-iec_hole_w/2,0,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
}

module mains()
{
    difference()
    {
    cube([mains_w,mains_h,th],center=true);
    translate([mains_hole_w/2,0,0])
        cylinder(r=mains_hole_sur/2,h=th*2,center=true);
    translate([-mains_hole_w/2,0,0])
        cylinder(r=mains_hole_sur/2,h=th*2,center=true);
    }
    translate([mains_hole_w/2,0,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
    translate([-mains_hole_w/2,0,0])
        cylinder(r=mains_screw_r,h=th*2,center=true);
}

