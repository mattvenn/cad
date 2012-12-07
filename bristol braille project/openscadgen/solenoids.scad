include <globals.scad>;
solenoid_length = 12.6;
solenoid_width= 10.6;
solenoid_height=20.6;
solenoid_plunger_radius=1.5;
solenoid_plunger_length=8;
solenoid_min_x_spacing=min_spacing; //minimum gap we can have between adjacent solenoids
solenoid_min_y_spacing=solenoid_height+solenoid_plunger_length+2*min_spacing; //minimum gap we can have between adjacent solenoids

//calulated
num_solenoids = 2 * letters;
solenoid_rows = round((solenoid_width+solenoid_min_x_spacing) / pitch);
solenoid_columns = round(num_solenoids/solenoid_rows);
solenoid_total_y = solenoid_rows*(solenoid_min_y_spacing);
//solenoid_total_x = pitch*(solenoid_rows-1); // +solenoid_columns*(solenoid_length+pitch);
solenoid_x_spacing = solenoid_rows*pitch-solenoid_width;
solenoid_total_x = solenoid_columns*(solenoid_x_spacing+solenoid_width)-solenoid_x_spacing+(solenoid_rows-1)*pitch; //num_solenoids*pitch;


echo(solenoid_total_y);
echo(solenoid_total_x);
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
    cube([solenoid_width,solenoid_length,solenoid_height],center=true);
    translate([0,0,solenoid_height/2+(trough_length)/2])
      cube([trough_width,trough_length,solenoid_length,],center=true);
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
