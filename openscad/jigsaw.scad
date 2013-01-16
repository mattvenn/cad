$fa = 1;
$fs = 1;
height = 10;
base_height = 3.8;
radius=30;
module example001()
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
		cylinder(height*2,1.5,1.5,center=true);
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
		cylinder(15,1.5,1.5,center=true);
}
module base()
{
	cylinder(h=base_height, r=radius );
	translate([0,0,base_height])
	difference() {
		cylinder(height-3.8,50/2,50/2);
		cylinder(height*2,40/2,40/2,center=true);		
}
}
example001();

