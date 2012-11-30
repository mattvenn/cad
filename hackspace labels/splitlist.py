#!/usr/bin/python
#./makeLabel.py --fontname 'Stencil Gothic JL' --font ~/.fonts/Stencil\ Gothic\ JL.ttf --noremove --text  SPEAKERS --y_offset -3 --file speakergoth.dxf
import os
list=open("list")
count=0
for line in list:
	if count!=0:
		(label,file,size) = line.split(",")
		print label,file,size,
		output="./dxfs/" + file + ".dxf"
		os.system("./makeLabel.py --text '%s' --file %s --size %s" % (label,output,size))
 	count+=1

