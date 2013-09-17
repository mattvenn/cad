//radius should be 1.36 but something is going wrong.
pitch = 4.785;
pins = 73;
pogo_r = 1.7 / 2;
thickness = 5;
length = 351.5;
pogo_offset_y = 14;
pogo_offset_x = 3.5;
width = pogo_offset_y + pogo_r * 2 + 5;
mount_r = 5/2;
mount_hole_space = 50;
mount_holes = 6;
mount_hole_offset_x = (length - mount_hole_space * mount_holes ) /2;

module mount()
{
    difference()
    {
        cube([length,width,thickness]);
*        translate([mount_hole_offset_x,5,-thickness/2])
            mount_holes();
    }
}

module mount_holes()
{
    for(i=[0: mount_holes])
    {
        translate([i*mount_hole_space,0,0])
        cylinder(r=mount_r,h=thickness*2);
    }
}

module pogos()
{
    for ( i = [0 : pins-1] )
    {
//        translate([i*pitch,0,0])
//        cylinder(r=pogo_r,h=20  , $fn = 20);
        polygon(points=[[i*pitch,0]]);
    }
}
*translate([pogo_offset_x,pogo_offset_y,0])
    pogos();
projection()mount();

