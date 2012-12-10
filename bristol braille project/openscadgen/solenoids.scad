include <globals.scad>;

module solenoid()
{
  color("lightblue")
  {
  cube([solenoid_width,solenoid_length,solenoid_height],center=true);
  translate([0,0,solenoid_height/2+solenoid_plunger_length/2])
    cylinder(r=solenoid_plunger_radius,h=solenoid_plunger_length,center=true);
  }
}
module solenoid_hole()
{
  trough_width=2*solenoid_plunger_radius+min_spacing;
  trough_length=solenoid_plunger_length+min_spacing;
  color("darkblue")
  {
    //*1.1 to get a clean boolean
    cube([solenoid_width,solenoid_length*1.1,solenoid_height],center=true);
    translate([0,0,solenoid_height/2+(trough_length)/2])
      cube([trough_width,solenoid_length*1.1,trough_length],center=true);
  }
}

module solenoids()
{
    max_x = 0;
    max_y = 0;
    for(x=[0:solenoid_columns-1])
    {
      for(y=[0:solenoid_rows-1])
      {
        assign(xp=x*solenoid_rows*pitch+y*pitch)
        {
          translate([xp,y*solenoid_min_y_spacing,0])
            rotate([90,0,0])
            {
              child();
            }
        }
      }
    }
}
