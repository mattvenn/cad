include <globals.scad>;

module base()
{
  color("orange")
  {
   difference()
   {
     cube([base_width,base_length,thickness],center=true);
     bolt_holes();
   }
  }
}

module bolt_holes()
{
  smooth=20;
  translate([-base_width/2+edge_margin/2,-base_length/2+edge_margin/2,0])
    cylinder(r=bolt_radius,h=2*base_height,center=true,$fn=smooth);
  translate([+base_width/2-edge_margin/2,-base_length/2+edge_margin/2,0])
    cylinder(r=bolt_radius,h=2*base_height,center=true,$fn=smooth);

  translate([-base_width/2+edge_margin/2,+base_length/2-edge_margin/2,0])
    cylinder(r=bolt_radius,h=2*base_height,center=true,$fn=smooth);
  translate([+base_width/2-edge_margin/2,+base_length/2-edge_margin/2,0])
    cylinder(r=bolt_radius,h=2*base_height,center=true,$fn=smooth);
}
module side()
{
 difference()
 {
 cube([thickness,base_length,base_height+0.1],center=true);
 /*
  translate([0,-base_length/2-0.1+thickness/2,0])
    cube([base_width-edge_margin,thickness,thickness*2],center=true);
  translate([0,+base_length/2+0.1-thickness/2,0])
    cube([base_width-edge_margin,thickness,thickness*2],center=true);
    */
  translate([0,0,-base_height/2-0.1+thickness/2])
    cube([thickness*2,base_length-edge_margin,thickness],center=true);
  translate([0,0,+base_height/2+0.1-thickness/2])
    cube([thickness*2,base_length-edge_margin,thickness],center=true);
  }
}

module comb()
{
  
 difference()
 {
 cube([base_width,base_height+0.1,thickness],center=true);
  //base locators
  translate([0,-base_height/2-0.1+thickness/2,0])
    cube([base_width-edge_margin,thickness,thickness*2],center=true);
  translate([0,+base_height/2+0.1-thickness/2,0])
    cube([base_width-edge_margin,thickness,thickness*2],center=true);

  //side locators
  translate([-base_width/2-0.1+thickness/2,0,0])
    cube([thickness,edge_margin,thickness*2],center=true);
  translate([+base_width/2+0.1-thickness/2,0,0])
    cube([thickness,edge_margin,thickness*2],center=true);
  }
}
