include <globals.scad>;


module slider()
{
  color("red")
  difference()
  {
    union()
    {
    cube([slider_width,slider_length,slider_height],center=true);
    translate([+slider_width/2,0,slider_height/2])
      rotate([0,0,180])
      rotate([90,0,0])
      rotate([0,90,0])
        linear_extrude(height=slider_width) import("nod.dxf");
    }
    translate([0,-slider_length/4,min_spacing])
      rotate([0,90,0])
        slot();
    translate([0,+slider_length/4,min_spacing])
      rotate([0,90,0])
        slot();
  }
} 
//for cutting out of the slider holder
module slider_boolean()
{
  color("red")
    cube([slider_width,slider_length,slider_height],center=true);
} 
module slot()
{
  smooth=20;
  hull()
  {
  cylinder(r=spindle_radius,h=slider_width*2,center=true,$fn=smooth);
  translate([slider_move_height,-slider_move_length,0])
    cylinder(r=spindle_radius,h=slider_width*2,center=true,$fn=smooth);
  }
}

module sliders_boolean()
{
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,0,0])
      slider_boolean();
  }
}
module sliders()
{
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,0,0])
      slider();
  }
}

module slider_rods()
{
  smooth=20;
  translate([0,slider_length/4,0])
  {
  translate([0,-slider_length/4,min_spacing])
    rotate([0,90,0])
      cylinder(r=spindle_radius,h=base_width+edge_margin,$fn=smooth);
  translate([0,+slider_length/4,min_spacing])
    rotate([0,90,0])
      cylinder(r=spindle_radius,h=base_width+edge_margin,$fn=smooth);
  }
}
