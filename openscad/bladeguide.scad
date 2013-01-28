//make nice  circles
$fa = 1;
$fs = 1;
locater_r=3;
height = 10;
vent_r=1.7;
base_height = 3.8;
radius=30;

//make the whole thing
module bladeguide()
{
	difference()
	{
		base();
		slot();
		locate();
		vents();
	}	
}

module vents()
{
	for( y = [ - 10 : 5 : 10 ] )
	{
	translate([y,10,0])
		cylinder(h=height*2,r=vent_r,center=true);
	}
}

module slot()
{
	slot_center_offset=12; 
	slot_l=slot_center_offset+radius+5; //bit more to be safe
	m = slot_l/2-slot_center_offset;
	translate([m,0,0])
		cube(size=[slot_l,7,25],center=true);


}

module locate()
{
	translate([-radius,0,0])
		cylinder(height*2,locater_r,center=true);
}

module base()
{
	cylinder(h=base_height, r=radius );
	translate([0,0,base_height])
	difference() 
	{
		cylinder(height-3.8,50/2,50/2);
		cylinder(height*2,40/2,40/2,center=true);		
	}
}

bladeguide();

