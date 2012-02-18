BOX-O-TRON-SVG version 0.1

This is a python script that is derived from Simon Kirkby's box-o-tron.

It outputs in SVG instead of DXF because I've found DXF a pain to deal with.

It also adds a --radius option for the radius of a cnc miller cutter. This expands the slot holes a little to accomodate from the rounded edges you get with cnc milling.

Notes from the original README:

If you specify a config file "./boxotron box.cfg" it will create if it does not exist, and populate it with defaults.

Edit the file and rerun the script and you will get a new shiney box.

One gotcha for using the config file , it will override the command line args,
So if you wat to specify on the command line , take it out of the config file
It has no sanity checking so you can make impossible boxes , check the output 
