#!/usr/bin/python

import os
import math
import argparse

#font stuff
from ttfquery import ttfmetadata
from ttfquery import describe, glyphquery
from ttfquery._scriptregistry import registry

#svg stuff
from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

def get_style():
    style=StyleBuilder()
    style.setFontFamily(fontfamily=args.font)
    style.setFontSize(fontsize) 
    style.setFilling("black")
    return style.getStyle()

def write_label(svg,labeltext,x=0,y=0):

    if args.toupper:
        labeltext = str.upper(labeltext)

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


def find_font():
  #load fonts
  registry.scan()
  fonts = registry.matchName(args.font)
  if len(fonts)>1:
    print "more than 1 font by that name, aborting"
    for font in fonts:
        print font
    exit(1)

  font_file =registry.fontFile(fonts[0])
  if args.debug:
    print "font found at", font_file

  font = describe.openFont(font_file)
  return font

#takes a font size and returns mm it is
def get_font_size(fontsize,text):

  width = 0
  for char in text:
    width += glyphquery.width(font,glyphquery.glyphName(font,char))

  scaling=2000/fontsize #no idea what this is
  if args.debug:
    print "label '%s' calculated to be %dx%d" % (text,width/scaling,glyphquery.charHeight(font)/scaling)
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
  print "page size %dmm x %dmm" % (pagewidth,pageheight)

  dwg = svg(width=widthmm,height=heightmm)
  dwg.set_viewBox("0 0 %s %s" % (pagewidth, pageheight))
  return dwg


if __name__ == '__main__':
  argparser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description='''program to make laser cuterable labels for bristol hackspace storage boxes.

    defaults sizes are for louvred plastic boxes, override with the --width and --height arguments

    process a newline separated file in one go with --file argument

    requirements
    ------------

    * a good laser cutable font. I recommend this one 'Stencil Gothic JL'
    * an old version of pysvg: http://code.google.com/p/pysvg/downloads/detail?name=pysvg-0.2.1.zip&can=2&q=
    * some python modules that can query ttf fonts:
        * http://pypi.python.org/pypi/TTFQuery
        * http://sourceforge.net/projects/fonttools/?source=dlp
    * an up to date version of pstoedit http://www.pstoedit.net/
    * inkscape''')

  group = argparser.add_mutually_exclusive_group(required=True)
  group.add_argument('--text',
      action='store', dest='text', default=None,
      help="text to print")
  group.add_argument('--file',
      action='store', dest='file',
      help="file to generate labels from")
  argparser.add_argument('--font',
      action='store', dest='font', default="Stencil Gothic JL",
      help="font to use")
  argparser.add_argument('--columns',
      action='store', dest='columns', type=int, default=3,
      help="for sheet printing, number of columns")
  argparser.add_argument('--y_offset',
      action='store', dest='y_offset', type=int, default=0,
      help="positive numbers move text down")
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size of label, 0=small box, 1=big box. Override with --width and --height")
  argparser.add_argument('--width',
      action='store', dest='width', type=int,
      help="override width of label")
  argparser.add_argument('--height',
      action='store', dest='height', type=int,
      help="override height of label")
  argparser.add_argument('--fontsize',
      action='store', type=int, dest='fontsize', default=None,
      help="override default fontsize")
  argparser.add_argument('--toupper',
      action='store_const', const=True, dest='toupper', default=False,
      help="convert labels to upper case")
  argparser.add_argument('--debug',
      action='store_const', const=True, dest='debug', default=False,
      help="print debugging info")
  argparser.add_argument('--noremove',
      action='store_const', const=False, dest='remove', default=True,
      help="don't remove temporary svg and eps files")

  args = argparser.parse_args()

  #defaults
  if args.size == 0:
    height=23
    width=75
    fontsize=10 
  elif args.size == 1:
    height=35
    width=104
    fontsize=14

  #allow override of defaults
  if args.fontsize:
    fontsize = args.fontsize
  if args.width:
    width = args.width
  if args.height:
    width = args.height

  margin = 5

  if args.debug:
    print "label size %dx%dmm, fontsize %d" % (height,width,fontsize)


  font=find_font()

  #if only one label:
  if args.text:    
    filename = args.text.replace(" ","")
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

    rows = int(math.ceil(float(len(labels))/args.columns))
    print "printing %d labels as a %dx%d sheet" % (len(labels),args.columns,rows)

    pagewidth=args.columns*(width+2*margin)
    pageheight=rows*(height+2*margin)
    dwg = setup()

    count=0
    for j in range(0,rows):
        for i in range(0,args.columns):
            if count>=len(labels):
                break;
            x=i*(width+2*margin)
            y=j*(height+2*margin)
            square(dwg,x,y)
            write_label(dwg,labels[count],x,y)
            count+=1

    dwg.save(filename + ".svg")

  #export magic!
  os.system("inkscape -E %s.eps %s.svg" % (filename,filename)) 
  os.system("pstoedit -dt -f dxf:'-polyaslines -mm' %s.eps %s.dxf" % (filename,filename))
  print "written label to %s.dxf" % filename
  #get rid of old temp files
  if args.remove:
    os.system("rm %s.svg" % filename)
    os.system("rm %s.eps" % filename)

  if args.debug:
    print "laser cutter settings. power at 1 turn, 50mm per second"
