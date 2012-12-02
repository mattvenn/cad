#!/usr/bin/python
from pysvg.structure import svg
import argparse
from Base import base
"""
  p = path("M%d,%d" % (x,y))
  p.appendLineToPath(x,y+height,False)
  p.appendLineToPath(x+width,y+height,False)
  p.appendLineToPath(x+width,y,False)
  p.appendLineToPath(x,y,False)
  p.set_style(style)
  dwg.addElement(p)
"""

def setup():
  widthmm = "%fmm" % defaults["width"] #pagewidth
  heightmm = "%fmm" % defaults["height"] #pageheight

  dwg = svg(width=widthmm,height=heightmm)
  dwg.set_viewBox("0 0 %s %s" % (defaults["width"], defaults["height"]))
  return dwg

if __name__ == '__main__':
  argparser = argparse.ArgumentParser(
      description="generates square based energy drawings")
  argparser.add_argument('--file',
      action='store', dest='file', default="label.dxf",
      help="dxf file to create")
  argparser.add_argument('--text',
      action='store', dest='text', default="no label",
      help="text to print")
  argparser.add_argument('--size',
      action='store', dest='size', type=int, default=0,
      help="size, 0=small box, 1=big box")

  args = argparser.parse_args()

  defaults = {}
  defaults["width"]=250
  defaults["height"]=200
  defaults["fontsize"]=10
  defaults["stroke"]=0.5
  """
    margin = 5
    pagewidth=width+2*margin
    pageheight=height+2*margin
  """
  
  #stepper
  defaults["stepper"]={}
  defaults["stepper"]["width"]=40
  defaults["stepper"]["margin"]=40 #distance between stepper and solenoids
  #solenoid stuff
  defaults["solenoid"]={}
  defaults["solenoid"]["length"] = 20.4
  defaults["solenoid"]["t_length"] = 8 #trough length
  defaults["solenoid"]["width"] = 10.6
  defaults["solenoid"]["number"] = 8
  defaults["solenoid"]["x_shift"] = 3.25 #distance between centres
  defaults["solenoid"]["y_shift"] = defaults["solenoid"]["length"]+defaults["solenoid"]["t_length"]+4

  dwg = setup()
  base(defaults,dwg) #draw the base that the solenoids fit on
  dwg.save("label.svg")
"""
  import os
  #magic!
  os.system("inkscape -E label.eps label.svg") 
  os.system("pstoedit -dt -f dxf:'-polyaslines -mm' label.eps " + args.file)
  #get rid of old temp files
  os.system("rm label.svg")
  os.system("rm label.eps")
"""
