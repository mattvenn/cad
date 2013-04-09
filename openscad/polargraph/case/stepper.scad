include <globals.scad>;

bolt_radius=1.55;
stepper_shaft_radius=5/2;
stepper_bush_radius=22.1/2;
stepper_bush_length=4;
bolt_distance=31.0/2;

module stepper()
{
    color("blue")
    {
        union()
        {
        cube([stepper_width,stepper_length,stepper_height],center=true);
        translate([0,0,stepper_length/2+stepper_shaft_length/2])
            cylinder(r=stepper_shaft_radius,h=stepper_shaft_length,center=true);
        translate([0,0,stepper_length/2+stepper_bush_length/2])
            cylinder(r=stepper_bush_radius,h=stepper_bush_length,center=true);
        translate([bolt_distance,bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([bolt_distance,-bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([-bolt_distance,bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([-bolt_distance,-bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        }
    }
}

module stepper_mount()
{
          side_s = makerbeam_w/2;
          difference()
          {
          cube([stepper_width,base_height+0.1,thickness],center=true);    
          translate([stepper_width/2-side_s,base_height/2-makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([-stepper_width/2+side_s,base_height/2-makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([stepper_width/2-side_s,-base_height/2+makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          translate([-stepper_width/2+side_s,-base_height/2+makerbeam_w/2,0])
            cylinder(r=bolt_r,h=thickness*2,center=true);
          }
}
