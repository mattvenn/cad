include <globals.scad>;

module slider()
{
  difference()
  {
    union()
    {
      //the main slider body
     translate([0,slider_y_offset,0])
      cube([slider_width,slider_length,slider_height],center=true);
      //the lock
      translate([0,-slider_move_length/2,-slider_move_height/2]) //eyeballed
      translate([+slider_width/2,0,slider_height/2-0.4+2.1]) //eyeballed
        rotate([0,0,180])
        rotate([90,0,0])
        rotate([0,90,0])
          linear_extrude(height=slider_width) import("depdxf/lock_pattern_dxf_lines.dxf");

    }
    translate([0,-slider_length/4,min_spacing])
      rotate([0,90,0])
        slot();
    translate([0,+slider_length/4,min_spacing])
      rotate([0,90,0])
        slot();
  }
} 

solenoid_pin_base_length=5;
solenoid_pin_base_width=5;
solenoid_pin_top_width=1;
solenoid_pin_shoulder_height=2;
solenoid_pin_length=4.5;
solenoid_pin_shoulder_width=(solenoid_pin_base_width-solenoid_pin_top_width)/2;
module solenoid_pin()
{
  union()
  {
  //the top pin
  translate([0,solenoid_pin_shoulder_height/2+solenoid_pin_length/2,0])
    cube([solenoid_pin_top_width,solenoid_pin_length,slider_width],center=true);
  //the shoulder
  translate([-solenoid_pin_base_width/2,-solenoid_pin_shoulder_height/2,-slider_width/2])
  linear_extrude(height=slider_width)
    polygon([
      [0,0],
      [solenoid_pin_base_width,0],
      [solenoid_pin_base_width-solenoid_pin_shoulder_width,solenoid_pin_shoulder_height],
      [solenoid_pin_shoulder_width,solenoid_pin_shoulder_height],
      [0,0]]);
  //the base
  translate([0,-solenoid_pin_shoulder_height/2-solenoid_pin_base_length/2,0])
    cube([solenoid_pin_base_width,solenoid_pin_base_length,slider_width],center=true);
  }
}
//for cutting out of the slider holder
module slider_boolean()
{
  color("red")
    translate([0,slider_y_offset,0])
    cube([slider_width,slider_length,slider_height],center=true);
} 
module slot()
{
  smooth=20;
  hull()
  {
  cylinder(r=spindle_radius,h=slider_width*1.5,center=true,$fn=smooth);
  translate([slider_move_height,-slider_move_length,0])
    cylinder(r=spindle_radius,h=slider_width*1.5,center=true,$fn=smooth);
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
module sliders(project)
{
  color("red")
  {
    for(x=[0:num_solenoids-1])
    {
      if(project)
      {
        rotate([0,90,0])
        translate([0,0,x*slider_height*2])
        {
          slider();
          translate([0,-slider_y-solenoid_height/2-slider_pin_offset+(x % solenoid_rows)*solenoid_min_y_spacing ,-9]) //eyeballed
            rotate([0,0,180])
            rotate([-90,0,0])
            rotate([0,90,0])
              solenoid_pin();
        }
      }
      else
      {
        translate([x*pitch,0,0])
        {
          slider();
          translate([0,-slider_y-solenoid_height/2-slider_pin_offset+(x % solenoid_rows)*solenoid_min_y_spacing ,-slider_solenoid_pin_z_offset]) //eyeballed
            rotate([0,0,180])
            rotate([-90,0,0])
            rotate([0,90,0])
              solenoid_pin();
        }
      }
    }
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
