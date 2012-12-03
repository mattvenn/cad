from pprint import pprint
from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *
import Styles

def base(d):
  group=g();
  conf=d["base"]
  conf["width"]=d["margin"]
  conf["length"]=d["margin"]
  #starting from the left
  group.addElement(motor_mount(d))
  group.addElement(solenoid_holes(d))

#    group.addElement(edge_holes(d))
  group.addElement(base_outline(d))
  pprint(d)
  return group

def base_outline(d):
  conf=d["base"]
  #how much is this going to add to the width and length
  conf["width"]+=d["margin"]
  conf["length"]+=d["margin"]

  r=rect(0,0,conf["width"],conf["length"],5,5) #rounded corners
  r.set_style(Styles.get_cut_style(d))
  return r;

def solenoid_holes(d):
    conf=d["base"]
    #draw the solenoids
    group=g();
    x=0
    y=0
    ymax=0
    sol_num=0
    for i in range(d["solenoid"]["number"]):
      th=TransformBuilder()
      th.setTranslation("%f,%f" % (x,y))
      print "sol_num:", sol_num
      solenoid=solenoid_hole(d)
      solenoid.set_transform(th.getTransform())
      group.addElement(solenoid)
      sol_num+=1
      x=x+d["pitch"]
      y=y+d["solenoid"]["total_length"]+d["solenoid"]["y_shift"]
      if sol_num == d["solenoid"]["solenoids_per_column"]:
        ymax=y
        y=0
    
    th=TransformBuilder()
    conf["solenoid_start_x"]=conf["width"]
    conf["solenoid_start_y"]=d["margin"]
    th.setTranslation('%f,%f' % (conf["solenoid_start_x"],conf["solenoid_start_y"]))
    group.set_transform(th.getTransform())

    #sol's total width,length calculated by solenoid_hole()
    total_length=ymax #+d["solenoid"]["total_length"] 
    conf["length"]+=total_length-d["solenoid"]["y_shift"]
    total_width=x+d["solenoid"]["total_width"]
    conf["width"]+=total_width-d["pitch"]

    return group

def solenoid_hole(d):
  conf=d["solenoid"]
  x=0
  y=0
  trough_width = 8
  trough_length= 8
  s_width=conf["width"]
  s_length=conf["length"]
  lip = (conf["width"]-trough_width)/2

  conf["total_length"]=s_length+trough_length 
  conf["total_width"]=s_width

  p = path("M%f,%f" % (x,y))
  p.appendLineToPath(x+s_width,y,False)
  p.appendLineToPath(x+s_width,y+s_length,False)
  p.appendLineToPath(x+s_width-lip,y+s_length,False)
  p.appendLineToPath(x+s_width-lip,y+s_length+trough_length,False)
  p.appendLineToPath(x+lip,y+s_length+trough_length,False)
  p.appendLineToPath(x+lip,y+s_length,False)
  p.appendLineToPath(x,y+s_length,False)
  p.appendLineToPath(x,y,False)
  p.set_style(Styles.get_cut_style(d))

  return p

def motor_mount(d):
    conf=d["base"]
    #draw the stepper mount hole
    import Stepper;

    stepper_mount_holes=Stepper.stepper_mount_holes(d)
    th=TransformBuilder()
    th.setRotation('90.0')
    conf["stepper_mount_hole_x"]=d["margin"]+d["stepper"]["length"]
    conf["stepper_mount_hole_y"]=d["margin"]+d["stepper"]["width"]
    th.setTranslation('%f,%f' % (conf["stepper_mount_hole_x"],conf["stepper_mount_hole_y"]))
    stepper_mount_holes.set_transform(th.getTransform())

    #how much is this going to add to the width and length?
    conf["width"]+=conf["stepper_mount_hole_x"]+d["thickness"]
    conf["length"]+=conf["stepper_mount_hole_y"]+d["stepper"]["width"]
    print conf["width"]
    return stepper_mount_holes

