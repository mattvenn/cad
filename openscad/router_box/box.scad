mot_soc_d = 15.5;
mot_soc_flat = 0.5;
th = 2;
mains_d = 16;
$fs = 0.5;

module mot_soc()
{
    difference()
    {
    cylinder(r=mot_soc_d/2,h = th * 2,center = true);
    translate([0,mot_soc_d/2 + 5 - mot_soc_flat])
        cube([10,10,10],center=true);
    }
}

module mains()
{
    cylinder(r=mains_d/2,h=th*2,center=true);
}
module dsub(pins)
{
    //measured
    db_h = 10;
    //13 = 40, 5 = 18
    db_w = (pins + 1) * 2.77 + 1.4;
    db_w_diff = 2.0;
    echo(db_w);

    //calculated
    db_w_min = db_w - db_w_diff / 2;
    db_w_max = db_w + db_w_diff / 2;
    db_w_h = db_w + 7;
    echo(db_w_h);

    translate([-db_w_h/2,0,0])
        cylinder(r=1.5,h=th*2,center=true);
    translate([+db_w_h/2,0,0])
        cylinder(r=1.5,h=th*2,center=true);

    linear_extrude(height=th*2,center=true)
       polygon([[-db_w_min/2,-db_h/2],[-db_w_max/2,db_h/2],[db_w_max/2,db_h/2],[db_w_min/2,-db_h/2]]);

}

projection()
    mains();
//13 = 40, 5 = 18
//13 = 47, 5 = 25
* projection()
    dsub(5);
* projection()
    mot_soc();
