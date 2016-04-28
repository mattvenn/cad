#!/usr/bin/python

import re

def get_gcode_xy(num,ngc):
    # linuxcnc is 1 indexed
    hole = int(raw_input("what line in gcode for hole %d: " % num)) - 1
    #hole = 23

    with open(ngc) as fh:
        gcodes = fh.readlines()

    m = re.search('X(-?\d+.\d+) Y(-?\d+.\d+)', gcodes[hole])
    if m:
        print(gcodes[hole])
        return(float(m.group(1)), float(m.group(2)))
    else:
        raise Exception("couldn't get XY in [%s]" % gcodes[hole]) 

def get_cam_xy(num):
    x = float(raw_input("x%d: " % num))
    y = float(raw_input("y%d: " % num))
    return(x,y)
