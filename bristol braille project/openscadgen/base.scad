include <globals.scad>;
include <solenoids.scad>;

//calculated
//base_width=2*edge_margin+solenoid_total_x;
//base_width=2*edge_margin+solenoid_total_x;
base_width=solenoid_total_x+2*edge_margin;
base_length=solenoid_total_y+2*edge_margin;

module base()
{
  color("orange")
  {
   cube([base_width,base_length,thickness],center=true);
  }
}
