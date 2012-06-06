#!/usr/bin/python

import sys
import re
drillfilename = ""
if (len(sys.argv) > 1):
    drillfilename = sys.argv[1]
else:
    print "no file given"
    exit(1)

newdrillfilename = drillfilename + ".minimal.ngc" 

try:
    drillfile = open(drillfilename)
    gcode = drillfile.readlines()
    #better way to do this?
    drillfile = open(drillfilename)
    allgcode = drillfile.read()
except IOError as e:
    print "couldn't read file %s : %s" % ( drillfilename, e )
    exit(1)

#find all the tools used
tools = []
for line in gcode:
    matchObj = re.match( r'^\( (T\d\d) \| (\d+\.\d+)mm', line )
    if matchObj:
        if len(matchObj.groups()) == 2:
            tools.append( matchObj.group(2) )
            print matchObj.group(1), matchObj.group(2)

print tools
currentToolNum = 1
#get user input
while currentToolNum <= len(tools):
    #could just ask for the number of tools to replace up to
    toolNumbers = raw_input( "how many for %d?\n" % currentToolNum )
    #could do some error checking on the input
    replace = re.findall( r'(\d)', toolNumbers )
    replaceStr =  "T%02d" %  currentToolNum
    if replace:
        print "replacing tools:"
        for replaceTool in replace:
            findStr =  "T%02d" %  int(replaceTool)
            print findStr , " with " , replaceStr
            #do the replacing
            allgcode = re.sub(findStr, replaceStr, allgcode)
        currentToolNum = int( replace[len(replace)-1] ) + 1
    else:
        currentToolNum += 1

#write the file
print "writing file to %s" % newdrillfilename
newgcodefile = open( newdrillfilename, "w" )
newgcodefile.write(allgcode)
newgcodefile.close()
