// make holes nice
$fa=10;
$fs=0.8;

w = 162;
l = 111;
h= 3;

projection()
difference()
{
//cube([w,l,h]);
translate([5,8,0])
	pi();
}

module pi()
{
	w = 56;
	l = 85;
	h = 10;
//	color("blue") cube([w,l,h]);

	bw = 49;
	bl = 58;
	bd = 3;
    //fixings
    translate([(w-bw)/2 + bw/2,(l-bl) +bl/2 - 3.5,0])
{
    translate([-bw/2,-bl/2,10/2])
        cylinder(r=bd/2, h=10*2, center=true);
    translate([+bw/2,-bl/2,10/2])
        cylinder(r=bd/2, h=10*2, center=true);
    translate([+bw/2,+bl/2,10/2])
        cylinder(r=bd/2, h=10*2, center=true);
    translate([-bw/2,+bl/2,10/2])
        cylinder(r=bd/2, h=10*2, center=true);
}
}
