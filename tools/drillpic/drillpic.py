#!/usr/bin/python
"""
todo:
* image is flipped both x & y
- done: the png demo image should draw circles
* allow define a tool radius instead of xdiv


Gcode for peck drilling:
G83 Z Q P R I K J F X* Y*
Z= Bottom of hole
Q= Peck amount 
P= Pause at bottom of hole
R= Position of the R &lt; clearance &gt; plane
I= Start peck amount
K= Amount to reduce each successive peck
J= Minimum peck amount
X and Y= Optional locations for successive holes.

"""
import argparse
from PIL import Image, ImageDraw

def get_main_color(img):
    colors = img.getcolors(img.size[0]*img.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

def get_region_box(img,x,y):
    
    cell_width = img.size[0]/args.xdiv
    cell_height = img.size[1]/args.ydiv
    box = (
        x*cell_width,
        y*cell_height,
        x*cell_width+cell_width,
        y*cell_height+cell_height)
    return box

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="make a gcode file from a pic")

    parser.add_argument('--gcode', default="drill.ngc", help='gcode file to write', type=argparse.FileType('w'))
    parser.add_argument('--image', action='store', dest='image_file', help="image", required = True)
    parser.add_argument('--width', action='store', dest='width', type=int, default=100, help="width in mm")
    parser.add_argument('--xdiv', action='store', dest='xdiv', type=int, default=5, help="xdiv")
    parser.add_argument('--ydiv', action='store', dest='ydiv', type=int, default=5, help="ydiv")
    parser.add_argument('--safez', action='store', dest='safez', type=float, default=1, help="z safety")
    parser.add_argument('--peck', action='store', dest='peck', type=float, default=0, help="peck")
    parser.add_argument('--feedspeed', action='store', dest='feedspeed', type=float, default=200, help="feedspeed mm/min")
    parser.add_argument('--depth', action='store', dest='z', type=float, default=5, help="z depth")
    parser.add_argument('--offset', action='store', dest='offset', type=float, default=0, help="offset z by this much")
    parser.add_argument('--invert', action='store_const', dest='invert', const=True, default=False, help="invert the image, making black white and vice versa")
    parser.add_argument('--square', action='store_const', dest='square', const=True, default=False, help="make the drilling happen on a square grid, disregard y")
    parser.add_argument('--openscad', action='store_const', dest='openscad', const=True, default=False, help="make an openscad that represents the drawing")
    args = parser.parse_args()

    print "generating gcodes"

    #preamble
    openscad = []
    gcode = []
    gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
    gcode.append( 'G0 Z%.4f F%s' %(float(args.safez), float(args.feedspeed)) )


    src = Image.open(args.image_file)
    src = src.convert('L')
    resize = float(args.width) / src.size[0]
    if args.invert:
        circle_colour = 0
        bg_colour = 255
    else:
        circle_colour = 255
        bg_colour = 0
    drill = Image.new('L',src.size,bg_colour)
    draw = ImageDraw.Draw(drill)

    skip_count = 0
#    im.show()
    (x,y) = src.size
    if args.openscad:
        cube_height = args.z + args.offset 
        openscad.append("rad_1 = 1; rad_2 = 20;")
        openscad.append("difference(){")
        openscad.append("translate([-10,-10,0])")
        openscad.append("cube([%d,%d,%d]);" % ( x+20,y+20,cube_height))

    if args.square:
       args.ydiv = y / (x / args.xdiv ) 
    cell_width = x/args.xdiv
    cell_height = y/args.ydiv

    for i in range(args.xdiv):
        for j in range(args.ydiv):
            box = get_region_box(src,i,j)
            region = src.crop(box)
            main_color = get_main_color(region)
            z = float(args.z / 255.0) * main_color
            if args.invert:
                z = args.z - z
            if args.offset:
                z = z + args.offset


            if z <= 0:
                skip_count += 1
                continue

            #draw a representative image
            circle_r = (cell_width/2)/255.0 * main_color
            draw.ellipse((i*cell_width+circle_r,j*cell_height+circle_r,i*cell_width+cell_width-circle_r,j*cell_height+cell_width-circle_r), fill=circle_colour)

            if args.openscad:
                openscad.append("translate([%d,%d,%d])" % (box[0],box[1],cube_height-z))
                openscad.append("cylinder(r1=rad_1,r2=rad_2,h=%f);" % (cube_height+ 5 ))
            #if peck
            if args.peck:
                gcode.append( 'G83 X%.4f Y%.4f Z%.4f Q%.4f R%.4f' %( 
                    box[0] * resize,
                    box[1] * resize,
                    -z,
                    float(peck),
                    float(args.safez)))
            else:
                gcode.append( 'G81 X%.4f Y%.4f Z%.4f R%.4f' %( 
                    box[0] * resize,
                    box[1] * resize,
                    -z,
                    float(args.safez)))

    drill.save("drill.png")
    gcode.append( 'M5 M9 M2' )
    for item in gcode:
      args.gcode.write("%s\n" % item)

    if args.openscad:
        openscad.append("}\n")
        f = open("drill.scad",'w')
        for item in openscad:
            f.write("%s\n" % item)
        f.close()

    print "didn't appending %d gcodes as drill didn't go below surface" % skip_count
    print "made %d drill codes" % len(gcode)
