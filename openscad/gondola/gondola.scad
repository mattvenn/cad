/*todo

  servo measurements a bit small, increased by 0.2. not tested
  servo wire hole too small
  servo mount slot too small - check cnc - esp drill diameter
  how mount pcb without screws in back?

*/
$fa = 4; //min angle: make large circles smoother
$fs=0.5; //min fragment size, make small circles smoother
include <servos.scad>

//measured
thickness = 2.73;
pcb_dist=42;
bolt_r = 1.6;
pen_holder_r = 30/2;
clearance=0.2;
drill_r = 1+clearance;

servo_dim = [12.5, 25,19.5];
servo_w = servo_dim[0];
servo_h = servo_dim[1];
servo_r = 4.8/2; //axle of the motor
servo_cam_to_holder = 11.2; //distance between one face of the cam and the back shoulder of the servo


//made up
leaf_width = 20; //width of the leaf spring
servo_x = 5.5;
slot_shift = 5;
cam_y = 25 + slot_shift;
pen_holder_height = 100;
outer_r = 60;

//calculated
hanger_r = pen_holder_r + 5;
servo_y = servo_h+cam_y; 
pen_hole_r = 25/2; //acrylic pipe is 30mm D, which I'll turn down to get a nice fit

//the bits
/*
acrylic() gondola();
acrylic() translate([0,0,thickness*2]) rotate([0,0,45])hanger();
acrylic() translate([0,0,thickness*3]) rotate([0,0,-180-45])hanger();
acrylic() pen_holder();
cam_angle = $t * -90;
acrylic() translate([servo_x,cam_y,thickness/2+servo_w/2]) rotate([90,cam_angle,0]) cam();
acrylic() servo_mount();
color("blue") servo();
*/

 projection() gondola();
* projection() rotate([90,0,0]) servo_mount();
* projection() hanger();
module acrylic()
{
    color("grey",0.8)
        child();
}
module servo_mount_diff()
{
    h = servo_w+2*thickness;
    translate([0,cam_y+thickness+servo_cam_to_holder,h/2-thickness/2])
        rotate([90,0,0])
            minkowski()
            {
                cube([servo_dim[2]+8*thickness-drill_r*2,h-drill_r*2,thickness],center=true);
                cylinder(r=drill_r,h=0.1);
            }

}

module servo_mount()
{
    difference()
    {
        servo_mount_diff();
        servo();
    }
}

module servo()
{
    alignds420(position=[servo_x,servo_y,thickness/2+6],rotation=[0,-90,90]);
    translate([servo_w-drill_r,servo_y-servo_dim[0]/2,thickness/2+6])rotate([0,-90,90])cylinder(r=drill_r+clearance,h=20,center=true);
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

      //bottom left corner stress hole
      translate([-w/2,-l/2,0])
        cylinder(r=slot_w*.8,h=t,center=true);

      //bottom right corner stress hole
      translate([w/2,-l/2,0])
        cylinder(r=slot_w*.8,h=t,center=true);

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
    translate([0,0,-1])
        servo_mount_diff();
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
      cylinder(r=pen_holder_r+clearance,h=thickness*2,center=true);
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

