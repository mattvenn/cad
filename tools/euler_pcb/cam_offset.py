#!/usr/bin/python
import argparse
import os

#camera offsets
x=+52.77
y=-1.26

#hole 1 in file
#G00 X9.7488 Y5.7394 
x1=9.7488 
y1=5.7394 

#hole 2 in file
#G00 X68.0000 Y13.0800 
x2=68
y2=13.08

#what they were with cam over holes
a1=5.25
b1=-11.85
a2=61.98
b2=2.72

parser = argparse.ArgumentParser(description="use grecode to generate rotated/offset drill files")

parser.add_argument('--gcode', default="drill.ngc", help='gcode file to read')
args = parser.parse_args()

print("%f %f %f %f %f %f %f %f" % (x1,y1,x2,y2,a1-x,b1-y,a2-x,b2-y))
os.system("cat %s | ./grecode/grecode -overlay %f %f %f %f %f %f %f %f -o adjust.ngc " % (args.gcode,x1,y1,x2,y2,a1-x,b1-y,a2-x,b2-y))


