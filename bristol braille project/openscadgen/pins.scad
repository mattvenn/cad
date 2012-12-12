include <globals.scad>;

module pin()
{
  cylinder(r=pin_radius,h=pin_length,center=true,$fn=smooth);
  cylinder(r=pin_radius*1.5,h=pin_radius,center=true,$fn=smooth);
}
module pins()
{
  color("green")
  {
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,0,0])
      pin();
  }
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,pitch,0])
      pin();
  }
  for(x=[0:num_solenoids-1])
  {
    translate([x*pitch,-pitch,0])
      pin();
  }
  }
}


