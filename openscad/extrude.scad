//see the tutorial on how to make inkscape render to dxf properly
difference()
{
	linear_extrude( height=100) import("drawing.dxf");
	cylinder(200,10,10);

}