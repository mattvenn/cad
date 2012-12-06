include <globals.scad>;
stepper_width=40;
stepper_height=40;
stepper_length=40;
stepper_shaft_radius=3;
stepper_shaft_length=15;
stepper_bush_radius=7;
stepper_bush_length=3;

module stepper()
{
    color("blue")
    {
        cube([stepper_width,stepper_length,stepper_height],center=true);
        translate([0,0,stepper_length/2+stepper_shaft_length/2])
            cylinder(r=stepper_shaft_radius,h=stepper_shaft_length,center=true);
        translate([0,0,stepper_length/2+stepper_bush_length/2])
            cylinder(r=stepper_bush_radius,h=stepper_bush_length,center=true);
    }
}

module stepper_mount()
{
    difference()
    {
        cube([stepper_length,stepper_width+2*thickness,thickness],center=true);    
        translate([0,stepper_width/2+thickness/2,0])
            cube([stepper_width/3,thickness,thickness],center=true);    
        translate([0,-stepper_width/2-thickness/2,0])
            cube([stepper_width/3,thickness,thickness],center=true);    
        cylinder(r=stepper_bush_radius,h=thickness,center=true);

    }

}
