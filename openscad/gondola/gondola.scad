$fs=0.5;
include </home/mattvenn/cad/MCAD/servos.scad>
outer_r = 60;
pen_hole_r = 12;

thickness = 3;
drill_r = 1;
pcb_dist=42;
bolt_r = 1.5;
clearance=0.2;

servo_w = 12;
servo_r = 2;

//calculated
hanger_r = pen_hole_r + 5;

//made up
servo_x = 6;

gondola();
*translate([0,0,thickness*2]) rotate([0,0,-45])hanger();
*translate([0,0,thickness*3]) rotate([0,0,-135])hanger();
translate([servo_x,-25,thickness/2+servo_w/2]) rotate([90,0,0]) cam();
color("gray") alignds420(position=[servo_x,-outer_r+8,thickness/2+6],rotation=[0,90,90]);

module plate()
{
  difference()
  {
    cylinder(r=outer_r,h=thickness,center=true);
    cylinder(r=pen_hole_r,h=2*thickness,center=true);
  }
}

module pcb_holes()
{
  translate([-pcb_dist/2,0,0])
    cylinder(r=bolt_r,h=thickness*2,center=true);
  translate([+pcb_dist/2,0,0])
  cylinder(r=bolt_r,h=thickness*2,center=true);
}
module slot(l,w)
{
  
  t=thickness*2;
  slot_w =drill_r*2;
      translate([0,-l/2,0])
        cube([w,slot_w,t],center=true);

      translate([-w/2,-l/2,0])
        cylinder(r=slot_w/2,h=t,center=true);
      translate([w/2,-l/2,0])
        cylinder(r=slot_w/2,h=t,center=true);
      translate([-w/2,0,0])
        rotate([0,0,90])
          cube([l,slot_w,t],center=true);
      translate([+w/2,0,0])
        rotate([0,0,90])
          cube([l,slot_w,t],center=true);
}

module gondola()
{
  difference()
  {
    plate();
    slot(outer_r,outer_r);
    slot(40,40);
    translate([0,+outer_r*0.6,0])
      pcb_holes();
  }
}

module hanger()
{
  color("blue")
  difference()
    {
      hull()
      {
        translate([outer_r/2,0,0])
          cylinder(r=hanger_r/3,h=thickness,center=true);
        cylinder(r=hanger_r,h=thickness,center=true);
      }
      cylinder(r=pen_hole_r+clearance,h=thickness*2,center=true);
        translate([outer_r/2,0,0])
          cylinder(r=bolt_r+clearance,h=thickness*2,center=true);
    }
}

module cam()
{
  difference()
  {
    cylinder(r=servo_w-thickness,h=thickness,center=true);
    cylinder(r=servo_r,h=thickness*2.0,center=true);
  }
}

