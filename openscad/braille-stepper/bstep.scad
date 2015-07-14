$fn=20;
th = 2;
motor_d = 6;
slot_z = 6; //height above base of the slot
base_l = 100;
sup_h = 20;
slider_h = sup_h/2;
motor_l = 30;
w = 50;
//projection()base();
//projection() rotate([90,0,0])support();
//made_supports();
projection() rotate([0,90,0])made_slider();
//made_motor();
module base()
{
	difference()
	{
	cube([w,base_l,th],center=true);
	made_supports();
	made_motor();
	}
}


module made_motor()
{
	translate([0,-base_l/2+motor_d/2+5,th/2+motor_d/2])
	rotate([-90,0,0])
	{
	motor();
	translate([0,motor_d,0])
	cube(motor_d+1,center=true);
	}
}
module made_slider()
{
	difference()
	{
	translate([0,15,slider_h/2+slot_z+th/2])
	slider();
	made_motor();
	}
}
module made_supports()
{
	translate([0,base_l/2 - 10,sup_h/2-th/2])
		support();
	translate([0,-base_l/2+motor_l,sup_h/2-th/2])
		support();
}
module motor()
{
	cylinder(r=motor_d/2,h=motor_d,center=true);
	translate([0,0,22/2-motor_d/2])
	cylinder(r=1.4/2,h=22,center=true);
	translate([0,0,9.5])
	cube([3.5,3.5,1.5],center=true);
	translate([0,5,-motor_d/2+10])
	rotate([90,0,0])cylinder(r=0.5,h=th*2,center=true);
	translate([0,5,-motor_d/2+14])
	rotate([90,0,0])cylinder(r=0.5,h=th*2,center=true);

}
module slider()
{
	cube([th,base_l,slider_h],center=true);
	slider_nub = 5;
	translate([0,-base_l/2+slider_nub/2,-2])
	cube([th,slider_nub,slider_h],center=true);
}
module support()
{
	difference()
	{
		cube([w,th,sup_h],center=true);
		//locating
		translate([0,0,-sup_h/2])
		cube([w/3,th*2,th*2],center=true);
		//slot
		translate([-th/2,-th/2,-sup_h/2+th+slot_z])
		cube([th,th*2,sup_h]);
	}

}
	
