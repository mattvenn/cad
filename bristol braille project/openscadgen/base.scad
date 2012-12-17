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

//holds the rotors in place and provides homing
module comb()
{
  union()
  {
    //main part
    difference()
    {
      cube([comb_width,comb_length,thickness],center=true); 
      //holes for the rotors
      for(x=[0:num_solenoids-1])
      {
        translate([-comb_width/2+min_spacing+rotor_thickness+x*pitch,0,0])
          cube([rotor_thickness,rotor_diameter+min_spacing,thickness*2],center=true);
      }
      //locators 1.1 for good boolean
      translate([0,-comb_length/2+thickness/2,0])
          cube([comb_width/3,thickness*1.1,thickness*2],center=true);
      translate([0,+comb_length/2-thickness/2,0])
          cube([comb_width/3,thickness*1.1,thickness*2],center=true);

    }
    //stop blocks for the rotors
    for(x=[0:num_solenoids-1])
    {
      translate([-comb_width/2+min_spacing+rotor_thickness+x*pitch+rotor_thickness/4,rotor_diameter/2+rotor_thickness/4,0])
        cube([rotor_thickness/2,rotor_thickness/2,thickness],center=true);
    }
  }
}


module pin_slider()
{
    //main part
    difference()
    {
      cube([pin_slider_width,comb_length-2*thickness,thickness],center=true); 

      //locators 1.1 for good boolean
      translate([-pin_slider_width/2+thickness,0])
          cube([thickness*2,comb_length/3,thickness*2],center=true);
      translate([+pin_slider_width/2-thickness,0])
          cube([thickness*2,comb_length/3,thickness*2],center=true);

    }
}

//holds the sliders
module slider_holder()
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
