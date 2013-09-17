#!/usr/bin/python

import argparse

"""
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


 
parser = argparse.ArgumentParser(description='make drill gcodes.')
parser.add_argument('safez', type=int, help='safe z distance (mm)')
parser.add_argument('holebottom', type=int, help='bottom of hole (mm)')
parser.add_argument('-peck', type=int, help='peck amount (mm)')
parser.add_argument('feedspeed', type=int, help='feed speed (mm/min)')
parser.add_argument('-gcode', default="drill.ngc", help='gcode file to write', type=argparse.FileType('w'))


args = parser.parse_args()

peck = args.peck
if peck == None:
    peck = args.safez - args.holebottom

ptList = []
pitch = 4.785
x_offset = 3.5
y_offset = 14
m_holes = 6
m_hole_space = 50
length = 351.5
mx_offset = (length - m_hole_space*m_holes)/2
print mx_offset
my_offset = 6
print my_offset
for i in range(0,73):
    ptList.append({'x':i*pitch+x_offset,'y':y_offset})
for i in range(m_holes+1):
    ptList.append({'x':i*m_hole_space+mx_offset,'y':my_offset})
    
print "found %d points" % len(ptList)

print "generating gcodes"
#preamble
gcode = []
gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
gcode.append( 'G0 Z%.4f F%s' %(float(args.safez), float(args.feedspeed)) )

firstHole = True
for hole in ptList:
    x = float(hole['x'])
    y = float(hole['y'])
    if firstHole:
        #first hole
        gcode.append( 'G83 X%.4f Y%.4f Z%.4f Q%.4f R%.4f' %( x, y,
            float(args.holebottom),
            float(peck),
            float(args.safez)))
        firstHole = False
    else:
        #subsequent
        gcode.append( 'G83 X%.4f Y%.4f' %( x , y ) )

#postamble
gcode.append( 'M5 M9 M2' )

#write the file
for item in gcode:
  args.gcode.write("%s\n" % item)
