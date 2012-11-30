
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
		cylinder(10,1.5,1.5);
	}
}
module slot()
{
	m = (60 - 42) / 2;
	translate([m,0,0])
		cube(size=[42,7,25],center=true);


}
module locate()
{
	translate([-60/2,0,0])
		cylinder(10,1.5,1.5);
}
module base()
{
	cylinder(3.8, 60/2,60/2 );
	translate([0,0,3.8])
	difference() {
		cylinder(10-3.8,50/2,50/2);
		cylinder(10-3.8,40/2,43/2);		
}
}
example001();

