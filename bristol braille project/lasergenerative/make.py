#!/usr/bin/python
from pysvg.structure import svg
import argparse
from Base import base
import Stepper

"""
  p = path("M%d,%d" % (x,y))
  p.appendLineToPath(x,y+height,False)
  p.appendLineToPath(x+width,y+height,False)
  p.appendLineToPath(x+width,y,False)
  p.appendLineToPath(x,y,False)
  p.set_style(style)
  dwg.addElement(p)
"""

def setup(width,length):
  widthmm = "%fmm" % width
  lengthmm = "%fmm" % length
  print width,length
  dwg = svg(width=widthmm,height=lengthmm)
  dwg.set_viewBox("0 0 %s %s" % (width, length))
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

  conf = {}
  conf["pitch"] = 3.25 #distance between centres
  conf["thickness"]=3
  conf["margin"]=10 #10mm margin all round
  conf["spindle_y"]=50 #the spindle for the rotors
  conf["letters"]=4 #the spindle for the rotors

  conf["fontsize"]=10
  conf["stroke"]=0.5
  """
    margin = 5
    pagewidth=width+2*margin
    pageheight=height+2*margin
  """
 
  #base
  conf["base"]={}
  #stepper
  conf["stepper"]={}
  conf["stepper"]["bush_radius"]=10
  conf["stepper"]["hole_radius"]=1.5
  conf["stepper"]["mount_hole_distance"]=20
  conf["stepper"]["length"]=40
  conf["stepper"]["width"]=float(40)
  conf["stepper"]["height"]=40
  conf["stepper"]["margin"]=40 #distance between stepper and solenoids
  #solenoid stuff
  conf["solenoid"]={}
  conf["solenoid"]["solenoids_per_column"] = 4
  conf["solenoid"]["length"] = 20.4
  conf["solenoid"]["width"] = 10.6
  conf["solenoid"]["number"] = conf["letters"]*2
  conf["solenoid"]["x_shift"] = conf["pitch"]
  conf["solenoid"]["y_shift"] = 4

  bases=base(conf) #draw the base that the solenoids fit on
  #now we should have the base size, so can setup
  dwg = setup(conf["base"]["width"],conf["base"]["length"])
  dwg.addElement(bases)
  #Stepper.stepper_mount_holes(conf,dwg)
  dwg.save("base.svg")
#  stepper(conf) #draw the base that the solenoids fit on
  """
  dwg = setup()
  support=Stepper.stepper_support(conf)
  dwg.addElement(support)
  dwg.save("stepper_support.svg")
  """

  import os
  #magic!
  os.system("inkscape -E base.eps base.svg") 
  os.system("pstoedit -dt -f dxf:'-polyaslines -mm' base.eps base.dxf")
  #get rid of old temp files
#  os.system("rm label.svg")
#  os.system("rm label.eps")
