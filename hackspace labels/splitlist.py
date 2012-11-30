#!/usr/bin/python
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

