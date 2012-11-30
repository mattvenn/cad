#!/usr/bin/python
"""
another good font?
http://www.fontsaddict.com/download/silexstencil-basic.otf
program to make laser cutterable labels for bristol hackspace storage boxes.
needs digital-7 font installed: http://www.dafont.com/digital-7.font
relies on inkscape to make the svg into an eps, and then pstoedit to turn the file into a dxf. The magic argument to include is -mm, which gets the scale right.

"""
import argparse
from PIL import Image, ImageDraw, ImageFont
from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

def get_style():
    style=StyleBuilder()
    style.setFontFamily(fontfamily="Digital-7")
#    style.setFontFamily(fontfamily="FreeSans")
    style.setFontSize(args.fontsize/3.39) 
    style.setFilling("black")
    return style.getStyle()

def write_label(svg):
    (textWidth,textHeight)=get_font_size(fontsize)
    print textWidth,textHeight
    if textWidth > width:
      print "text too long"
      exit(1)
    x=0 #(width-textWidth)/2
    y=height #10 #height #(height-textHeight)/2+textHeight
    margin = 0
    t=text(args.text,x+margin,y+margin)
    t.set_style(get_style())
    svg.addElement(t)

#takes a font size and returns mm it is
def get_font_size(fontsize):
  font = ImageFont.truetype(args.font,args.fontsize) #fontsize)
  im = Image.new('RGBA', (400,200),"yellow")
  draw = ImageDraw.Draw(im)
  w, h = font.getsize(args.text)
  draw.text(((400-w)/2,(200-h)/2), args.text, fill="black",font=font)
  im.save("hello.png", "PNG")
  print w,h
  print w/3.8,h/3.8
  return(w/3.8, h/3.8)

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
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size, 0=small box, 1=big box")
  argparser.add_argument('--fontsize',
      action='store', type=int, dest='fontsize', default=None,
      help="override font")
  argparser.add_argument('--font',
      action='store', dest='font', default=None,
      help="specify where the font is installed")
  argparser.add_argument('--noremove',
      action='store_const', const=False, dest='remove', default=True,
      help="don't remove temporary files")

  args = argparser.parse_args()

  if args.size == 0:
    height=50 #23
    width=100 #75
    fontsize=10 #results in text char size 5x7mm
  elif args.size == 1:
    height=35
    width=104
    fontsize=15 #results in text char size 5x7mm

  margin = 5
  pagewidth=width+2*margin
  pageheight=height+2*margin
  
  dwg = setup()
  square(dwg)
  write_label(dwg)
  dwg.save("label.svg")

  import os
  #magic!
  #os.system("inkscape -E label.eps label.svg") 
  #os.system("pstoedit -dt -f dxf:'-polyaslines -mm' label.eps " + args.file)
  #get rid of old temp files
  if args.remove:
    os.system("rm label.svg")
    os.system("rm label.eps")

  print "laser cutter settings. power at 1 turn, 50mm per second"
