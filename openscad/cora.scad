$fa = 0.5;
$fs = 0.5;
base_width = 77;
top_width = 60;
base_height = 97;
total_height = 115;
top_height = total_height - base_height;
num_slots = 12;
lower_slot_height=23.5;
lower_slot_width = 1.5;
slot_length = 6;
top_slot_width = 2.5;
drill_d = 2;
top_hole_d = 2.5;
top_hole_offset = 4 + top_hole_d / 2;
thickness = 5;

points = [ [0,0], [base_width/2,0], [top_width/2,base_height], [0,total_height]];

module slots()
{
    slot_w_increase = ( top_slot_width - lower_slot_width ) / (num_slots - 1);
    slot_y_increase = ( base_height - lower_slot_height ) / (num_slots -1 );
    lower_slot_base_width = base_width+((top_width-base_width)/base_height)*lower_slot_height;
    echo(lower_slot_base_width);
    slot_x_increase = ( lower_slot_base_width - top_width ) / 2 / (num_slots );
    for( i = [0:num_slots-1] )
    {
        translate([base_width/2-slot_length/2-slot_x_increase*i,lower_slot_height+i*slot_y_increase-lower_slot_width,thickness/2])
        assign(slot_width = lower_slot_width+i*slot_w_increase)
            cube([slot_length*2,slot_width,thickness*2],center=true);
    }
}

difference()
{
    bridge();
    slots();
    mirror([1,0,0])
        slots();
    translate([0,total_height-top_hole_offset,thickness/2])
        cylinder(r=top_hole_d/2,h=thickness*2,center=true);
}
module bridge()
linear_extrude(height=thickness)
{
    mirror([1,0,0])
        polygon(points);
    polygon(points);
}

