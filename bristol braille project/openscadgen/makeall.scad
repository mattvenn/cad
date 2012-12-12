include <globals.scad>;
include <stepper.scad>;
include <sliders.scad>;
include <solenoids.scad>;
include <base.scad>;
include <rotors.scad>;
include <pins.scad>;


//sliders and slider rods
slider_z=solenoid_width/2+slider_height/2+slider_solenoid_z_spacing;
translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z])
  sliders();
made_slider_rods();
module made_slider_rods()
{
  translate([-solenoid_width/2-edge_margin-0.5*edge_margin,0,slider_z])
    slider_rods();
}

//rotors and rod
rotor_rod_z=slider_z+slider_height+slider_move_height;
rotor_rod_y=slider_move_length+solenoid_total_y/2-solenoid_min_y_spacing;
translate([0,rotor_rod_y,rotor_rod_z])
{
  rotors();
  
  translate([-solenoid_width/2-edge_margin-0.5*edge_margin,0,0])
    rotor_rod();
}

//pins
made_pins();
module made_pins()
{
  translate([0,rotor_rod_y,rotor_rod_z+rotor_diameter/2+pin_length/2])
    pins();
}

//solenoids
solenoids()solenoid();

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
    slider_holders();
  }
}

made_lid();

module made_lid()
{
  difference()
  {
    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z+base_height-thickness])
      base();
    slider_holders();
    made_side();
    made_pins();
  }

}
*made_side();
module made_side()
{

  difference()
  {
    translate([base_x,base_y,base_z+base_height/2-thickness/2])
      side();
    made_pin_slider(); 
    //allow for movement of the pin slider
      translate([0,0,pin_slider_move_height])
        made_pin_slider();
    slider_holders();
    made_slider_rods();
  }
  difference()
  {
    translate([base_x+base_width-thickness,base_y,base_z+base_height/2-thickness/2])
      side();
    made_pin_slider(); 
    //allow for movement of the pin slider
      translate([0,0,pin_slider_move_height])
        made_pin_slider();
    slider_holders();
    made_slider_rods();
  }
}

made_pin_slider();
module made_pin_slider()
{
  color("gray")
  difference()
  {
    translate([base_x+pin_slider_width/2-thickness/2-thickness,rotor_rod_y,rotor_rod_z+pin_length/2])
      pin_slider();
      made_pins();
  }
}

made_comb();
module made_comb()
{
  color("blue")
    translate([comb_width/2-min_spacing-rotor_thickness,rotor_rod_y,rotor_rod_z+spindle_radius*2])
      comb();
}
//slider holders
slider_holders();
module slider_holders()
{
 difference()
  {
    union()
    {
    //most +ve y slider_holder
    translate([-solenoid_width/2-edge_margin+base_width/2,rotor_rod_y+comb_length/2-thickness/2,base_z+base_height/2-thickness/2])
      rotate([90,0,0])
        slider_holder();
    //close to origin slider_holder
    translate([-solenoid_width/2-edge_margin+base_width/2,rotor_rod_y-comb_length/2+thickness/2,base_z+base_height/2-thickness/2])
      rotate([90,0,0])
        slider_holder();
    }
    solenoids()solenoid_hole();
    made_comb();
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
