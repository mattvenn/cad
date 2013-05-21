include </home/mattvenn/cad/MCAD/shapes.scad>;
$fa=0.5;
$fs=0.5;
//measured vars
sled_hole_r = 1.5;
p_width= 85.60;
p_length =56;
p_height =21;
//for setting the height of the boolean bits
case_height = 20;

sd_stick_out = 17;

b_width = 82;
b_length = 53;
b_height = 10;
spacing = sd_stick_out;

//material thickness
thickness = 3;

//calculated vars
s_width = p_width+spacing*2;
s_length = b_length+p_length+spacing*3;
s_height = thickness;
echo(b_width,p_width,s_width);
/*
translate([0,-p_length/2-spacing/2,0])
    pi();
translate([0,b_length/2+spacing/2,0])
    breadboard();
*/

projection() color("blue") sled();

module sled()
{
    difference()
    {
    translate([0,0,-thickness/2-0.1])
        roundedBox(s_width,s_length,s_height,spacing);
    translate([0,-p_length/2-spacing/2,0])
        pi();
    translate([0,b_length/2+spacing/2,-b_height/2])
        breadboard();
    sled_holes();
    }
}
module sled_holes()
{
    hole_offset = spacing*0.7;
    translate([s_width/2-hole_offset,s_length/2-hole_offset,0])
        cylinder(r=sled_hole_r,h=thickness*4,center=true);
    translate([-s_width/2+hole_offset,s_length/2-hole_offset,0])
        cylinder(r=sled_hole_r,h=thickness*4,center=true);
    translate([s_width/2-hole_offset,-s_length/2+hole_offset,0])
        cylinder(r=sled_hole_r,h=thickness*4,center=true);
    translate([-s_width/2+hole_offset,-s_length/2+hole_offset,0])
        cylinder(r=sled_hole_r,h=thickness*4,center=true);
}

module breadboard()
{
    translate([0,0,b_height/2])
        cube([b_width,b_length,b_height],center=true);
}
module pi()
{
  hole_r=2.9/2;
  sd_slot=10;

  //not centering the cuboids because the dimensions of the holes are relative to 0,0
  translate([-p_width/2,-p_length/2,0])
  {
    cube([p_width,p_length,p_height]);

    //gpio
    translate([0,p_length-5,p_height])
      cube([30,5,5]);

    //sdcard hole
    translate([-sd_stick_out/2,p_length/2,0]) //-p_width/2,-p_length/2,0])
      hull()
      {
          cylinder(r=sd_slot,h=case_height,center=true);
          translate([-spacing,0,0])
          cylinder(r=sd_slot,h=case_height,center=true);
      }

    /*
    Corner: 0.0mm,0.0mm
    First Mount: 25.5mm,18.0mm
    Second Mount: 80.1mm, 43.6mm
    */
    translate([25.5,18,-case_height/2])
      cylinder(r=hole_r,h=case_height,center=true);
    translate([80.1,43.6,-case_height/2])
      cylinder(r=hole_r,h=case_height,center=true);

  }
}
