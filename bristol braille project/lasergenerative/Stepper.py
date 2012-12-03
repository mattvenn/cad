from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import *
from pysvg.builders import *

import Styles

def stepper(d):
    conf=d["stepper"]
    conf["back_x"]=conf["front_x"]-conf["length"]
    conf["top_y"]=conf["center_line_y"]-conf["width"]/2

    r=rect(conf["back_x"],conf["top_y"],conf["length"],conf["width"])
    r.set_style(Styles.get_construction_style(d))
    return r

def stepper_support(d):
  group=g();
  conf=d["stepper"]
  thickness=d["thickness"]
  conf["support_height"]=thickness+conf["height"]+thickness
  x=0
  y=0
  p = path("M%f,%f" % (x,y))
  p.appendLineToPath(conf["width"]/3,0)
  p.appendLineToPath(0,thickness)
  p.appendLineToPath(conf["width"]/3,0)
  p.appendLineToPath(0,-thickness)
  p.appendLineToPath(conf["width"]/3,0)
  p.appendLineToPath(0,conf["support_height"])
  p.appendLineToPath(-conf["width"]/3,0)
  p.appendLineToPath(0,-thickness)
  p.appendLineToPath(-conf["width"]/3,0)
  p.appendLineToPath(0,+thickness)
  p.appendLineToPath(-conf["width"]/3,0)
  p.appendLineToPath(0,-conf["support_height"])
  p.set_style(Styles.get_cut_style(d))
  group.addElement(p)
 
  #bush mounting
  c=circle(conf["width"]/2,conf["support_height"]/2,conf["bush_radius"])
  c.set_style(Styles.get_cut_style(d))
  group.addElement(c)

  #mount holes
  import math
  mount_x=math.sqrt(math.pow(conf["mount_hole_distance"],2)/2)
  mount_y=mount_x
  for x in -mount_x, mount_x:
    for y in -mount_y, mount_y:
      c=circle(conf["width"]/2+x,conf["support_height"]/2+y,conf["hole_radius"])
      c.set_style(Styles.get_cut_style(d))
      group.addElement(c)

  return group;

def stepper_mount_holes(d):
  conf=d["stepper"]
  thickness=d["thickness"]
  group=g();
  
  r=rect(2*conf["width"]/3,0,conf["width"]/3,thickness)
  r.set_style(Styles.get_cut_style(d))
  group.addElement(r);

  r=rect(0,0,conf["width"]/3,thickness)
  r.set_style(Styles.get_cut_style(d))
  group.addElement(r);

  return group

