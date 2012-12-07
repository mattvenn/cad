#!/usr/bin/python
"""
another good font?
http://www.fontsaddict.com/download/silexstencil-basic.otf
program to make laser cutterable labels for bristol hackspace storage boxes.
needs digital-7 font installed: http://www.dafont.com/digital-7.font
relies on inkscape to make the svg into an eps, and then pstoedit to turn the file into a dxf. The magic argument to include is -mm, which gets the scale right.

"""
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

def write_label(svg):
    (textWidth,textHeight)=get_font_size(fontsize)
    if textWidth > width or textHeight > height:
      print "text too big"
      exit(1)
    x=(width-textWidth)/2
    y=height/2+textHeight/2
    y=y+args.y_offset
    t=text(args.text,x+margin,y+margin)
    t.set_style(get_style())
    svg.addElement(t)

    r=rect(x+margin,y+margin-textHeight,textWidth,textHeight)
    r.set_style(get_style)
    svg.addElement(r)


#takes a font size and returns mm it is
def get_font_size(fontsize):
  fonts = registry.matchName( args.font)
  if len(fonts)>1:
    print "more than 1 font by that name, aborting"
    exit(1)

  font_file =registry.fontFile(fonts[0])
  print "font found at", font_file
  font = describe.openFont(font_file)

  width = 0
  for char in args.text:
    if char == ' ':
      char = "space"
    width += glyphquery.width(font,char)

  scaling=200 #no idea what this is
  return(width/scaling,glyphquery.lineHeight(font)/scaling)

def square(svg):
  x=margin
  y=margin

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
      action='store', dest='file', default="label.dxf",
      help="dxf file to create")
  argparser.add_argument('--text',
      action='store', dest='text', default="no label",
      help="text to print")
  argparser.add_argument('--font',
      action='store', dest='font', default="Stencil Gothic JL",
      help="font name")
  argparser.add_argument('--y_offset',
      action='store', dest='y_offset', type=int, default=0,
      help="move y about")
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size, 0=small box, 1=big box")
  argparser.add_argument('--fontsize',
      action='store', type=int, dest='fontsize', default=None,
      help="override font")
  argparser.add_argument('--noremove',
      action='store_const', const=False, dest='remove', default=True,
      help="don't remove temporary files")

  args = argparser.parse_args()

  if args.size == 0:
    height=23
    width=75
    fontsize=10 
  elif args.size == 1:
    height=35
    width=104
    fontsize=15

  if args.fontsize:
    fontsize = args.fontsize

  args.text = str.upper(args.text)
  margin = 5
  pagewidth=width+2*margin
  pageheight=height+2*margin
  
  dwg = setup()
  square(dwg)
  write_label(dwg)
  dwg.save("label.svg")

  import os
  #magic!
  os.system("inkscape -E label.eps label.svg") 
  os.system("pstoedit -dt -f dxf:'-polyaslines -mm' label.eps " + args.file)
  #get rid of old temp files
  if args.remove:
    os.system("rm label.svg")
    os.system("rm label.eps")

  print "laser cutter settings. power at 1 turn, 50mm per second"
