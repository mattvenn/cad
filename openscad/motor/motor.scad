wall_thickness=5;
open_top=true;
bearing_diameter=25;
shaft_diameter=10;
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
            winding_hole(30,50,wall_thickness*2);
        
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
motorbase(width,length);
rotate([0,90,0])
    cylinder(r=shaft_diameter/2,h=100,center=true);
translate([100,0,-width/2])
    winding(30,50,width/2-shaft_diameter);
