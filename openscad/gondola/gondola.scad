$fs=0.5;
include </home/matthew/work/cad/MCAD/servos.scad>
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
leaf_width = 20; //width of the leaf spring
servo_x = 6;
slot_shift = 5;
cam_y = 25 + slot_shift;
servo_h = 25;
servo_y = servo_h+cam_y; 
pen_holder_height = 100;


acrylic() gondola();
acrylic() translate([0,0,thickness*2]) rotate([0,0,45])hanger();
acrylic() translate([0,0,thickness*3]) rotate([0,0,-180-45])hanger();
acrylic() pen_holder();
cam_angle = $t * -90;
acrylic() translate([servo_x,cam_y,thickness/2+servo_w/2]) rotate([90,cam_angle,0]) cam();
color("blue") alignds420(position=[servo_x,servo_y,thickness/2+6],rotation=[0,-90,90]);

module acrylic()
{
    color("grey",0.8)
        child();
}

module pen_holder()
{
    translate([0,0,pen_holder_height/2])
        difference()
        {
            cylinder(r=pen_hole_r,h=pen_holder_height,center=true);
            cylinder(r=pen_hole_r-thickness,h=pen_holder_height*1.5,center=true);
        }
    
}
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
      //top
      translate([0,l/2,0])
        cube([w,slot_w,t],center=true);

      //top left corner
      translate([-w/2,l/2,0])
        cylinder(r=slot_w/2,h=t,center=true);

      //top right corner
      translate([w/2,+l/2,0])
        cylinder(r=slot_w/2,h=t,center=true);

      //left side
      translate([-w/2,0,0])
        rotate([0,0,90])
          cube([l,slot_w,t],center=true);

      //right side
      translate([+w/2,0,0])
        rotate([0,0,90])
          cube([l,slot_w,t],center=true);
}

module gondola()
{
  difference()
  {
    plate();
    translate([0,slot_shift+leaf_width/4,0])
        slot(outer_r-leaf_width/2,outer_r);
    translate([0,slot_shift,0])
        slot(outer_r-leaf_width,outer_r-leaf_width);
    translate([0,-outer_r*0.6,0])
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
  radius = servo_w/2+thickness;
  difference()
  {
    translate([0,thickness,0])
    cylinder(r=radius,h=thickness,center=true);
    cylinder(r=servo_r,h=thickness*2.0,center=true);
  }
}

