mot_soc_d = 15.5;
mot_soc_flat = 0.5;
th = 2;

module mot_soc()
{
    difference()
    {
    cylinder(r=mot_soc_d/2,h = th * 2,center = true);
    translate([0,mot_soc_d/2 + 5 - mot_soc_flat])
        cube([10,10,10],center=true);
    }
}

projection()
mot_soc();
