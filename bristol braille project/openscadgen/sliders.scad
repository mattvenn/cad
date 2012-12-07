include <globals.scad>;
include <solenoids.scad>;

slider_width=2;
slider_length=solenoid_total_y;
slider_height=10;
module slider()
{
  color("red")
    cube([slider_width,slider_length,slider_height],center=true);
} 
module sliders()
{
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,0,0])
      slider();
  }
}
