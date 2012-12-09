#!/usr/bin/python
"""
another good font?
program to make laser cutterable labels for bristol hackspace storage boxes.

for font width/height uses
* http://sourceforge.net/projects/fonttools/?source=dlp and 
* http://ttfquery.sourceforge.net/ttfquery.html#module-ttfquery.findsystem

for svg -> DXF uses:
* inkscape to make the svg into an eps,
* pstoedit to turn the file into a dxf. The magic argument to include is -mm, which gets the scale right.

"""
import os
from ttfquery import ttfmetadata
import argparse
from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

from ttfquery import describe, glyphquery
from ttfquery._scriptregistry import registry

pix_to_mm = 3.77

def get_style():
    style=StyleBuilder()
    style.setFontFamily(fontfamily=args.font)
    style.setFontSize(fontsize) 
    style.setFilling("black")
    return style.getStyle()

def write_label(svg,labeltext,x=0,y=0):
    (textWidth,textHeight)=get_font_size(fontsize,labeltext)
    if textWidth > width or textHeight > height:
      print "text too big"
      exit(1)
    x+=(width-textWidth)/2
    y+=height/2+textHeight/2
    y=y+args.y_offset
    t=text(labeltext,x+margin,y+margin)
    t.set_style(get_style())
    svg.addElement(t)

#    r=rect(x+margin,y+margin-textHeight,textWidth,textHeight)
#    r.set_style(get_style)
#    svg.addElement(r)


#takes a font size and returns mm it is
def get_font_size(fontsize,text):
  fonts = registry.matchName( args.font)
  if len(fonts)>1:
    print "more than 1 font by that name, aborting"
    for font in fonts:
        print font
    exit(1)

  font_file =registry.fontFile(fonts[0])
  if args.debug:
    print "font found at", font_file
  font = describe.openFont(font_file)
  #import pdb; pdb.set_trace()
  width = 0
  for char in text:
    width += glyphquery.width(font,glyphquery.glyphName(font,char))

  scaling=2000/fontsize #no idea what this is
  if args.debug:
    print "label width x height calculated to be %dx%d" % (width/scaling,glyphquery.charHeight(font)/scaling)
  return(width/scaling,glyphquery.charHeight(font)/scaling)

def square(svg,x=0,y=0):

  x+=margin
  y+=margin
  points = []
  #inkscape needs this to be able to export to dxf properly. Crap.
  style="stroke:#000000;stroke-opacity:1;fill:none;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none"

  p = path("M%d,%d" % (x,y))
  p.appendLineToPath(x,y+height,False)
  p.appendLineToPath(x+width,y+height,False)
  p.appendLineToPath(x+width,y,False)
  p.appendLineToPath(x,y,False)
  p.set_style(style)
  dwg.addElement(p)

    
def setup():
  widthmm = "%fmm" % pagewidth
  heightmm = "%fmm" % pageheight

  dwg = svg(width=widthmm,height=heightmm)
  dwg.set_viewBox("0 0 %s %s" % (pagewidth, pageheight))
  return dwg


if __name__ == '__main__':
  argparser = argparse.ArgumentParser(
      description="generates a laser cutterable label")
  argparser.add_argument('--file',
      action='store', dest='file', default="list.csv",
      help="file to generate labels from")
  argparser.add_argument('--text',
      action='store', dest='text', default=None,
      help="text to print")
  argparser.add_argument('--font',
      action='store', dest='font', default="Stencil Gothic JL",
      help="font name")
  argparser.add_argument('--columns',
      action='store', dest='columns', type=int, default=3,
      help="for sheet printing, number of columns")
  argparser.add_argument('--y_offset',
      action='store', dest='y_offset', type=int, default=0,
      help="positive numbers move text down")
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size, 0=small box, 1=big box")
  argparser.add_argument('--fontsize',
      action='store', type=int, dest='fontsize', default=None,
      help="override font")
  argparser.add_argument('--debug',
      action='store_const', const=True, dest='debug', default=False,
      help="print debugging info")
  argparser.add_argument('--noremove',
      action='store_const', const=False, dest='remove', default=True,
      help="don't remove temporary files")

  args = argparser.parse_args()

  #defaults
  if args.size == 0:
    height=23
    width=75
    fontsize=10 
  elif args.size == 1:
    height=35
    width=104
    fontsize=15

  margin = 5

  #allow override of fontsize
  if args.fontsize:
    fontsize = args.fontsize


  #if only one label:
  if args.text:    
    filename = args.text.replace(" ","")
    args.text = str.upper(args.text)
    pagewidth=width+2*margin
    pageheight=height+2*margin
    dwg = setup()
    square(dwg)
    write_label(dwg,args.text,)
    dwg.save(filename + ".svg")
  #make a sheet
  elif args.file:
    filename="sheet"
    labels=[]
    count=0
    list=open(args.file)
    labels=list.read().splitlines()

    import math
    rows = int(math.ceil(float(len(labels))/args.columns))
    print "printing %d labels as a %dx%d sheet" % (len(labels),args.columns,rows)

    pagewidth=args.columns*(width+2*margin)
    pageheight=rows*(height+2*margin)
    dwg = setup()

    count=0
    for i in range(0,args.columns):
        for j in range(0,rows):
            if count>=len(labels):
                break;
            x=i*(width+2*margin)
            y=j*(height+2*margin)
            square(dwg,x,y)
            write_label(dwg,labels[count],x,y)
            count+=1

  dwg.save(filename + ".svg")
  exit(1) 
  
  #export magic!
  os.system("inkscape -E %s.eps %s.svg" % (filename,filename)) 
  os.system("pstoedit -dt -f dxf:'-polyaslines -mm' %s.eps %s.dxf" % (filename,filename))
  #get rid of old temp files
  if args.remove:
    os.system("rm label.svg")
    os.system("rm label.eps")

  print "laser cutter settings. power at 1 turn, 50mm per second"
