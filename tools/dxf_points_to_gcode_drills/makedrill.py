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


"""
this code derived from http://bytes.com/topic/python/answers/644857-parse-dxf-file-lines-circles-arcs
"""
def parseDXFpts(f):
 
    # skip to entities section
    s = f.next()
    while s.strip() != 'ENTITIES':
        s = f.next()
 
    inPoint = False
 
    ptList = []
 
    for line in f:
        line = line.strip()
        # In ENTITIES section, iteration can cease when ENDSEC is reached
        if line == 'ENDSEC':
            break
 
        elif inPoint == True:
            dd = dict.fromkeys(['10','20'], 0.0)
            while line != '0':
                if line in dd:
                    dd[line] = f.next().strip()
                line = f.next().strip()
            ptList.append([[dd['10'], dd['20']]])
            inLine = False
 
        else:
            if line == 'POINT':
                inPoint = True
 
    f.close()
    return ptList
 
parser = argparse.ArgumentParser(description='make drill gcodes.')
parser.add_argument('safez', type=int, help='safe z distance (mm)')
parser.add_argument('holebottom', type=int, help='bottom of hole (mm)')
parser.add_argument('-peck', type=int, help='peck amount (mm)')
parser.add_argument('feedspeed', type=int, help='feed speed (mm/min)')
parser.add_argument('dxf', type=file, help='dxf file to parse')
parser.add_argument('-gcode', default="drill.ngc", help='gcode file to write', type=argparse.FileType('w'))


args = parser.parse_args()

peck = args.peck
if peck == None:
    peck = args.safez - args.holebottom

print "parsing DXF:",
ptList = parseDXFpts(args.dxf)
print "found %d points" % len(ptList)

print "generating gcodes"
#preamble
gcode = []
gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
gcode.append( 'G0 Z%.4f F%s' %(float(args.safez), float(args.feedspeed)) )

firstHole = True
for hole in ptList:
    x = float(hole[0][0])
    y = float(hole[0][1])
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
