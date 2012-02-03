module drill(r)
{
scaling = 10;
scale([1/scaling,1/scaling,1/scaling]) circle(r = r * scaling);
}
dSize = 1.36/2;
for ( i = [0 : 10] )
{
	translate([i*4.251,0,0]) drill(dSize);
}