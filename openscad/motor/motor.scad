wall_thickness=3;
num_blades=3;
blade_rake=20;
open_top=true;
bearing_diameter=20;
shaft_diameter=10;
magnet_length=30;
magnet_width=10;
magnet_height=2;
magnet_holder_height=0;
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
        //2 end bearings
        rotate([0,90,0])
            cylinder(h=length*2,r=bearing_diameter/2,center=true);
        //1 bottom bearing
        cylinder(h=length*2,r=bearing_diameter/2,center=true);

        //holes for the winding post
        rotate([90,0,0])
            translate([0,0,-width/2+wall_thickness/2])
                winding_base(width/2,magnet_length,wall_thickness*2);
        rotate([-90,0,0])
            translate([0,0,-width/2+wall_thickness/2])
                winding_base(width/2,magnet_length,wall_thickness*2);
        
    }
}

//TODO: needs holes for the wires to come out
//height refers to the total height of the winding post
module winding(width,length,height)
{
    difference()
    {
        //the base
        translate([0,0,wall_thickness/2])
            winding_base(width,length,wall_thickness);
        union()
        {
        //the two slots to make the clip connection
        translate([length/2-0.75*wall_thickness,width/2,0])
            cube([wall_thickness/2,width,wall_thickness*2],center=true);
        translate([-length/2+0.75*wall_thickness,-width/2,0])
            cube([wall_thickness/2,width,wall_thickness*2],center=true);
        }
    }
    //the coils go round this
    translate([0,0,height/2])
        cube([length*0.7,wall_thickness,height],center=true);
    //and don't fall off because of this
    top_height=wall_thickness/2;
    translate([0,0,height-wall_thickness/4])
        cube([length*0.9,wall_thickness,wall_thickness/2],center=true);

}
//height in this case refers to the height of the base block, so we can use it also for boolean removal of a hole that fits the winding
module winding_base(width,length,height)
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
//watch out, this may catch the winding posts
module magnet_mount()
{
    difference()
    {
        union()
        {
            rotate([0,90,0])
                magnet_holder();
            cylinder(r=shaft_diameter/2+wall_thickness/2,h=length-wall_thickness*2,center=true);
        }
        cylinder(r=shaft_diameter/2,h=length+wall_thickness+1,center=true);
    }
    echo("mag holder");
    echo(magnet_holder_height);
}
//TODO: needs to be made printable by removing overhangs
module magnet_holder()
{
    height=shaft_diameter+wall_thickness+2*magnet_height;
    difference()
    {
        cube([magnet_length+wall_thickness,magnet_width+wall_thickness,height],center=true);
        cube([magnet_length,magnet_width,height+1],center=true);

    }
    //possible to measure this rathr than calculate it?
    echo(height);
}

module blade_holder()
{
    difference()
    {
        union()
        {
            cylinder(r=shaft_diameter/2+wall_thickness,h=10);
            for(i=[0:num_blades-1])
            {
                rotate([0,0,i*360/num_blades])
                    translate([0,0,0])
                        blade_mount();
            }
        }
        translate([0,0,-2])
            cylinder(r=shaft_diameter/2,h=10);
    }
        
}

module blade_mount()
{
    base_thickness=2;
    blade_holder_length=40;
    blade_holder_width=10;
    holder_height=tan(blade_rake)*blade_holder_width;
    //echo(holder_height);
            difference()
            {
            translate([-blade_holder_width/2,0,0])
            rotate([90,0,0])
            {
                linear_extrude(height=blade_holder_length)
                polygon([[0,0],[blade_holder_width,0],[blade_holder_width,holder_height+base_thickness],[0,base_thickness]]);
                }
        
        //bolt holes
        for(i=[0:1])
        {
            translate([0,-20-i*10,0])
                rotate([0,-blade_rake,0])
                    cylinder(r=1.5,h=50,center=true,$fn=12);
        }
    }


}

echo($t*360);
rotate([$t*360,0,0])
{
color("blue")
    translate([length/2+10,0,0])
        rotate([0,90,0])
            blade_holder();

//show the ally tube
color("red")
    rotate([0,90,0])
        cylinder(r=shaft_diameter/2,h=length*1.5,center=true);

//translate([-100,0,0])
color("green")
    rotate([90,0,90])
        magnet_mount();
}
//FIXME!
magnet_holder_height=17;
winding_clearance=6;
winding_height=(width - magnet_holder_height - winding_clearance )/ 2;
echo("winding height:");
echo(winding_height);

//static stuff
motorbase(width,length);

color("grey"){
    rotate([90,0,0])
        translate([0,0,-width/2])
            winding(width/2,magnet_length,winding_height);
    rotate([-90,0,0])
        translate([0,0,-width/2])
            winding(width/2,magnet_length,winding_height);
            }

