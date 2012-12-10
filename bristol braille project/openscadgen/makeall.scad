include <globals.scad>;
include <stepper.scad>;
include <sliders.scad>;
include <solenoids.scad>;
include <base.scad>;

slider_z=solenoid_width/2+slider_height/2+slider_solenoid_z_spacing;
translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z])
  sliders();
made_slider_rods();
module made_slider_rods()
{
  translate([-solenoid_width/2-edge_margin-0.5*edge_margin,0,slider_z])
    slider_rods();
}
*solenoids()solenoid();

//base
base_z=-solenoid_length/2+thickness/2;
base_y=base_length/2-edge_margin-solenoid_height;
base_x=-solenoid_width/2-edge_margin+thickness/2;
made_base();
*projection(cut = false) made_base();
module made_base()
{
  difference()
  {
    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z])
      base();
    solenoids()solenoid_hole();
    combs();
  }
}
made_side();
* made_lid();
module made_lid()
{
  difference()
  {
    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z+base_height-thickness])
      base();
    combs();
    made_side();
  }

}
module made_side()
{

  difference()
  {
    union()
    {
    translate([base_x,base_y,base_z+base_height/2-thickness/2])
      side();
    translate([base_x+base_width-thickness,base_y,base_z+base_height/2-thickness/2])
      side();
    }
  combs();
  made_slider_rods();
  }
}
combs();
module combs()
{
 difference()
  {
    union()
    {
    //most +ve y comb
    translate([-solenoid_width/2-edge_margin+base_width/2,base_y+base_length/2-solenoid_height-edge_margin,base_z+base_height/2-thickness/2])
      rotate([90,0,0])
        comb();
    //close to origin comb
    translate([-solenoid_width/2-edge_margin+base_width/2,base_y,base_z+base_height/2-thickness/2])
      rotate([90,0,0])
        comb();
    }
    solenoids()solenoid();
union()
{
    translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z])
      sliders_boolean();
    translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z+slider_move_height])
      sliders_boolean();
      }
    }
  
}

//how we'll export DXFs
*projection(cut = true) stepper_mount();
*rotate([90,0,0])
{
    stepper();
    translate([0,0,stepper_length/2+thickness/2])
        stepper_mount();
}
