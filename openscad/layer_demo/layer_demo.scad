//define some variables
//can vars
can_radius = 6;
can_wall_thickness=1;
can_height = 30;
top_cone_h = 2;
//nozzle vars
nozzle_h=3;
nozzle_r = 2;

//calculated variable
total_can_height=can_height+top_cone_h+nozzle_h;
echo(str("can height:", total_can_height));

//global vars
smooth=20; //circular shapes are drawn with this number of edges
slice_thickness=1;

//so we can choose what to do from the command line
make_can=true;
//slice_can=true;
import_slices=true;
//get_single_slice=true;
//cut_level=20;

//make a simple 3d model of a can
module make_can()
{
  //the body
  color("grey")
  //the 0.1 is to make sure the objects merge together
  difference()
  {
    cylinder(r=can_radius,h=can_height+0.1,$fn=smooth);
    translate([0,0,can_wall_thickness])
      cylinder(r=can_radius-can_wall_thickness,h=can_height-can_wall_thickness*2,$fn=smooth);
  }

  //the top cone
  color("grey")
  translate([0,0,can_height-0.1])
    cylinder(r2=nozzle_r,r1=can_radius*0.8,h=top_cone_h+0.1,$fn=smooth);
  //the nozzle
  color("white")
  translate([0,0,can_height+top_cone_h])
    cylinder(r=nozzle_r,h=nozzle_h,$fn=smooth);
}


//slice the can up into sections
module slice_can()
{
  for(cut_level=[0:slice_thickness:total_can_height])
  {
    projection(cut=true)
      translate([cut_level/slice_thickness*3*can_radius,10,-cut_level])
        make_can();
  }
}

module get_single_slice()
{
  echo(str("cut level:", cut_level));
  projection(cut=true)
    translate([0,0,-cut_level])
      make_can();
}

module import_slices()
{
  translate([can_radius*3,0,0])
  for(cut_level=[0:slice_thickness:total_can_height-1])
  {
    echo(str("layer", cut_level, ".dxf"));
    translate([0,0,cut_level*2]) //*2 to explode it
      color("gray")
        linear_extrude(height=slice_thickness) import(str("layer", cut_level, ".dxf"));
  }

}
//do it
if(make_can)
  make_can();

if(slice_can)
  slice_can();

if(get_single_slice)
  get_single_slice();

if(import_slices)
  import_slices();
