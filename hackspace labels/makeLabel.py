#!/usr/bin/python
import argparse
from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

def get_style():
    style=StyleBuilder()
    style.setFontFamily(fontfamily="Digital-7")
    style.setFontSize(fontsize) 
    style.setFilling("black")
    return style.getStyle()

def write_label(svg):
    textWidth=len(args.text)*charWidth
    if textWidth > width:
      print "text too long"
      exit(1)
    x=(width-textWidth)/2
    y=(height-charHeight)/2+charHeight
    t=text(args.text,x+margin,y+margin)
    t.set_style(get_style())
    svg.addElement(t)


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
      description="generates square based energy drawings")
  argparser.add_argument('--text',
      action='store', dest='text', default="no label",
      help="text to print")
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size, 0=small box, 1=big box")

  args = argparser.parse_args()

  if args.size == 0:
    height=23
    width=75
    charWidth=4.5
    charHeight=7
    fontsize=10 #results in text char size 5x7mm
  elif args.size == 1:
    height=35
    width=104
    charWidth=6.8
    charHeight=9.7
    fontsize=15 #results in text char size 5x7mm

  margin = 5
  pagewidth=width+2*margin
  pageheight=height+2*margin
  
  dwg = setup()
  square(dwg)
  #write_label(dwg)
  dwg.save("label.svg")
  print "now open label.svg with inkscape. Then select all, object to path, save as a desktop cutting plotter (r13) .dxf file"
  print "laser cutter settings. power at 1 turn, 50mm per second"
