#!/usr/bin/python
import svg_stack as ss
import os

doc = ss.Document()
layout1 = ss.HBoxLayout()

path = './history/'
print "looking in %s for svg files" % path
listing = os.listdir(path)
num = 0
for infile in sorted(listing):
  num += 1
  svgfile = path + infile
  layout1.addSVG(svgfile)

layout1.setSpacing(-707.7)
doc.setLayout(layout1)

doc.save('concat.svg')
print "concat %d files" % num
