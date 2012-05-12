#!/usr/bin/python

import sys
import re
drillfilename = ""
newdrillfilename = "./newdrill.gcode"
if (len(sys.argv) > 1):
    drillfilename = sys.argv[1]
else:
    print "no file given"
    exit()

drillfile = open(drillfilename)
gcode = drillfile.readlines()
drillfile = open(drillfilename)
allgcode = drillfile.read()

tools = []
for line in gcode:
    matchObj = re.match( r'^\( (T\d\d) \| (\d+\.\d+)mm', line )
    if matchObj:
        if len(matchObj.groups()) == 2:
            tools.append( matchObj.group(2) )
            print matchObj.group(1), matchObj.group(2)

print tools
currentToolNum = 1
while currentToolNum <= len(tools):
    toolNumbers = raw_input( "how many for %d?\n" % currentToolNum )
    replace = re.findall( r'(\d)', toolNumbers )
    replaceStr =  "T%02d" %  currentToolNum
    if replace:
        print "replacing tools:"
        for replaceTool in replace:
            findStr =  "T%02d" %  int(replaceTool)
            print findStr , " with " , replaceStr
            allgcode = re.sub(findStr, replaceStr, allgcode)
        currentToolNum = int( replace[len(replace)-1] ) + 1
    else:
        currentToolNum += 1

newgcodefile = open( newdrillfilename, "w" )
newgcodefile.write(allgcode)
newgcodefile.close()
