wall_thickness=5;
open_top=true;
bearing_diameter=25;
shaft_diameter=10;
magnet_length=30;
magnet_width=10;
magnet_height=2;
width=50;
length=70;

module motorbase(width,length)
{
    difference()
    {
        cube([length,width,width],center=true);
        cube([length-wall_thickness*2,width-wall_thickness*2,width-wall_thickness*2],center=true);

        if(open_top)
        {
            translate([0,0,width/2])
                cube([length-wall_thickness*2,width-wall_thickness*2,width-wall_thickness*2],center=true);
        }

        //bearings
        rotate([0,90,0])
            cylinder(h=length*2,r=bearing_diameter/2,center=true);
            
        translate([0,0,-width/2+wall_thickness/2])
            winding_hole(width/2,magnet_length,wall_thickness*2);
        
    }
}

//TODO: needs holes for the wires to come out
//height refers to the total height of the winding post
module winding(width,length,height)
{
    difference()
    {
        winding_hole(width,length,wall_thickness);
        union()
        {
        translate([length/2-0.75*wall_thickness,width/2,0])
            cube([wall_thickness/2,width,wall_thickness*2],center=true);
        translate([-length/2+0.75*wall_thickness,-width/2,0])
            cube([wall_thickness/2,width,wall_thickness*2],center=true);
        }
    }
    translate([0,0,height/2])
        cube([length*0.7,wall_thickness,height],center=true);
    translate([0,0,height])
        cube([length*0.9,wall_thickness,wall_thickness/2],center=true);

}
//height in this case refers to the height of the base block, so we can use it also for boolean removal of a hole that fits the winding
module winding_hole(width,length,height)
{
        union()
        {
            //bumps for clippage
            translate([length/2,width/2-wall_thickness/2,0])
                sphere(wall_thickness/2,$fn=12);
            translate([-length/2,-width/2+wall_thickness/2,0])
                sphere(wall_thickness/2,$fn=12);
            cube([length,width,height],center=true);
        }
}
module magnet_mount()
{
    difference()
    {
        cylinder(r=shaft_diameter/2+wall_thickness/2,h=length-wall_thickness*2,center=true);
        cylinder(r=shaft_diameter/2,h=length+wall_thickness+1,center=true);
    }
    translate([shaft_diameter,0,0])
        rotate([0,90,0])
            magnet_holder();
    translate([-shaft_diameter,0,0])
        rotate([0,90,180])
            magnet_holder();
}
//TODO: needs to be made printable by removing overhangs
module magnet_holder()
{
    difference()
    {
        cube([magnet_length+wall_thickness,magnet_width+wall_thickness,magnet_height+wall_thickness],center=true);
        translate([0,0,wall_thickness/2])
            cube([magnet_length,magnet_width,magnet_height*2],center=true);

    }
}
rotate([0,90,0])
    magnet_mount();
motorbase(width,length);
/*
rotate([0,90,0])
    cylinder(r=shaft_diameter/2,h=100,center=true);
translate([100,0,-width/2])
    winding(width/2,magnet_length,width/2-shaft_diameter);
*/
