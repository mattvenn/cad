bolt_r = 2.5;
sbolt_r = 1.6;
wheel_r = 50;
beam_w = 15;
module wheel()
{
difference()
{
    circle(r=wheel_r);
    circle(r=bolt_r);
    for ( i = [ 10 : 10 : wheel_r ])
    translate([i,0,0])
        circle(r=sbolt_r);
}
}

module beam(length=120)
{
    difference()
    {
    square([length,beam_w]);
    for ( i = [ 10 : 20 : length ])
    translate([i,beam_w/2,0])
        circle(r=sbolt_r);
    }
}
wheel();
translate([wheel_r*2+5,0,0])
    wheel();
translate([0,wheel_r*2,0])
    beam();
translate([130,wheel_r*2,0])
    beam();
translate([0,wheel_r*2+beam_w*2,0])
    beam();
translate([130,wheel_r*2+beam_w*2,0])
    beam();
translate([0,wheel_r*2+beam_w*4,0])
    beam(240);
translate([0,wheel_r*2+beam_w*6,0])
    beam(240);
