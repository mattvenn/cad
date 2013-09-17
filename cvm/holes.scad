//radius should be 1.36 but something is going wrong.

for ( i = [0 : 24] )
{
	translate([i*3.96,0,0])
	circle(1.60 / 2 , $fn = 20);
}