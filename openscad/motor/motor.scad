wall_thickness=3;
num_blades=3;
blade_rake=20;
open_top=true;
bearing_diameter=22;
shaft_diameter=8;
magnet_length=25.2;
magnet_width=10;
magnet_height=3;
magnet_holder_height=shaft_diameter+wall_thickness+2*magnet_height;
width=50;
length=50;

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

//TODO: needs holes for the wires to come out, and for a motor shaft to assist winding
//needs sloped edges
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
	bottom_length=length*0.7;
	top_length=length*0.9;
	rise=4;
	translate([0,wall_thickness/2,height-rise])
	  rotate([90,0,0])
	    linear_extrude(height=wall_thickness)
		polygon([[0,0],[bottom_length/2,0],[top_length/2,rise],[-top_length/2,rise],[-bottom_length/2,0],[0,0]]);
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
//TODO remove overhangs
module magnet_mount()
{
	mount_length=length-wall_thickness*2;
	cone_height=mount_length-magnet_holder_height;
	start_radius=shaft_diameter/2+wall_thickness;
	end_radius=shaft_diameter/2+2*wall_thickness;
    difference()
    {
        union()
        {
            rotate([0,90,0])
                magnet_holder();
			  translate([0,0,cone_height/2]) //+magnet_holder_height])	
			  cylinder(end_radius,start_radius,cone_height,center=true);
//            cylinder(r=shaft_diameter/2+wall_thickness,h=length-wall_thickness*2,center=true);
        }
        cylinder(r=shaft_diameter/2,h=length+wall_thickness+1,center=true);
    }
}
//TODO: needs to be made printable by removing overhangs
module magnet_holder()
{
    difference()
    {
        cube([magnet_length+wall_thickness,magnet_width+wall_thickness,magnet_holder_height],center=true);
        cube([magnet_length,magnet_width,magnet_holder_height+1],center=true);

    }
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

//FIXME!
magnet_holder_height=17;
winding_clearance=6;
winding_height=(width - magnet_holder_height - winding_clearance )/ 2;
color("green")
    rotate([90,0,90])
        magnet_mount();
/*
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

//static stuff
* motorbase(width,length);
* color("grey"){
    rotate([90,0,0])
        translate([0,0,-width/2])
            winding(width/2,magnet_length,winding_height);
    rotate([-90,0,0])
        translate([0,0,-width/2])
            winding(width/2,magnet_length,winding_height);
            }
*/
//winding mount
* winding(width/2,magnet_length,winding_height);
/*
//test hole for the spring fitting
difference()
{
cube([40,40,wall_thickness],center=true);
winding_base(width/2,magnet_length,wall_thickness*2);
}
*/
