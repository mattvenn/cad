$fa = 5;
$fs = 1;
kerf = 0.3;
hub_r = 11 /2 - kerf;
sprockets = 6;
sprocket_w = 2.3 - kerf;
sprocket_h = 2.3 - kerf;
wheel_r = 50;
thickness = 5;

projection() wheel();

module wheel()
{
    difference()
    {
        //wheel
        cylinder(r=wheel_r,h=thickness,center=true);
        //hub
        cylinder(r=hub_r,h=thickness*2,center=true);
        //sprockets
        for(i = [0:360/sprockets:360])
        {
            rotate([0,0,i])
            translate([hub_r,0,0])
            cube([sprocket_h*2,sprocket_w,thickness*2],center=true);
        }
    }

}
