#!/usr/bin/python
"""
todo:

"""
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="make a gcode file from a pic")

    parser.add_argument('--gcode', default="drill.ngc", help='gcode file to write', type=argparse.FileType('w'))
    parser.add_argument('--x', action='store', type=int, dest='x', help="number of x holes", required = True)
    parser.add_argument('--y', action='store', type=int, dest='y', required = True, help="number of y holes")
    parser.add_argument('--xspace', action='store', dest='xspace', type=int, default=5, help="xdiv")
    parser.add_argument('--yspace', action='store', dest='yspace', type=int, default=5, help="ydiv")
    parser.add_argument('--safez', action='store', dest='safez', type=float, default=1, help="z safety")
    parser.add_argument('--feedspeed', action='store', dest='feedspeed', type=float, default=200, help="feedspeed mm/min")
    parser.add_argument('--depth', action='store', dest='z', type=float, default=3, help="z depth")
    args = parser.parse_args()

    print "generating gcodes"

    #preamble
    gcode = []
    gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
    gcode.append( 'G0 Z%.4f F%s' %(float(args.safez), float(args.feedspeed)) )
    for i in range(args.x):
        for j in range(args.y):
            z=args.z
            """
            #if peck
            if args.peck:
                gcode.append( 'G83 X%.4f Y%.4f Z%.4f Q%.4f R%.4f' %( 
                    i*args.xspace,j*args.yspace,-z,
                    float(peck),
                    float(args.safez)))
            else:
            """
            gcode.append( 'G81 X%.4f Y%.4f Z%.4f R%.4f' %( 
                i*args.xspace,j*args.yspace,-z,
                args.safez))

    gcode.append( 'M5 M9 M2' )

    for item in gcode:
        args.gcode.write("%s\n" % item)

    print "made %d drill codes" % ( args.x * args.y )
