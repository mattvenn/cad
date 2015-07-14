#!/usr/bin/python
import argparse
import os
import drill_extract as de
import pickle

inch = 25.4

parser = argparse.ArgumentParser(description="use grecode to generate rotated/offset drill files")

parser.add_argument('--gcode', default="input.ngc", help='gcode file to read')
parser.add_argument('--defaults', action='store_const', const=True, help='load last used')
parser.add_argument('--inch', action='store_const', const=True, help='use if drill file in inches')
args = parser.parse_args()

# load old defaults
if args.defaults:
    with open('offsets') as fh:
        [x,y,x1,y1,x2,y2,a1,b1,a2,b2] = pickle.load(fh)
else:
    # holes in gcode
    x1, y1 = de.get_gcode_xy(1, args.gcode)
    x2, y2 = de.get_gcode_xy(2, args.gcode)


    # what they were with cam over holes
    print("locate drill at first hole, touch off 0,0")
    print("set z to safe then move till camera cross hair over first hole")
    x, y = de.get_cam_xy(1)
    a1, b1 = x, y 

    print("move to second hole")
    a2, b2 = de.get_cam_xy(2)

    if args.inch:
        print("converting inches")
        a1 = a1 / inch
        b1 = b1 / inch
        a2 = a2 / inch
        b2 = b2 / inch
        x = x / inch
        y = y / inch

    # save them
    with open('offsets','w') as fh:
        pickle.dump([x,y,x1,y1,x2,y2,a1,b1,a2,b2], fh)

print("%f %f %f %f %f %f %f %f" % (x1,y1,x2,y2,a1-x,b1-y,a2-x,b2-y))
os.system("cat %s | ./grecode/grecode -overlay %f %f %f %f %f %f %f %f -o adjust.ngc " % (args.gcode,x1,y1,x2,y2,a1-x,b1-y,a2-x,b2-y))


