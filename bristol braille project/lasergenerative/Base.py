from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

from Styles import get_style

def base(d,svg):
    x=d["width"]/2
    y=d["height"]/2
    r=rect(0,0,150,150,5,5)
    r.set_style(get_style(d))
    svg.addElement(r)

    #draw the solenoids
    solenoid_x_offset = d["stepper"]["width"]+d["stepper"]["margin"]
    solenoid_y_offset = 10
    x=solenoid_x_offset
    y=solenoid_y_offset
    sol_num=0
    for i in range(d["solenoid"]["number"]):
      solenoid(d,svg,x,y)
      sol_num+=1
      x=x+d["solenoid"]["x_shift"]
      y=y+d["solenoid"]["y_shift"]
      if sol_num == 4:
        y=solenoid_y_offset

def solenoid(d,svg,x,y):
  trough_width = 8
  trough_length= d["solenoid"]["t_length"]
  s_width=d["solenoid"]["width"]
  s_length=d["solenoid"]["length"]
  lip = (d["solenoid"]["width"]-trough_width)/2
  p = path("M%f,%f" % (x,y))
  p.appendLineToPath(x+s_width,y,False)
  p.appendLineToPath(x+s_width,y+s_length,False)
  p.appendLineToPath(x+s_width-lip,y+s_length,False)
  p.appendLineToPath(x+s_width-lip,y+s_length+trough_length,False)
  p.appendLineToPath(x+lip,y+s_length+trough_length,False)
  p.appendLineToPath(x+lip,y+s_length,False)
  p.appendLineToPath(x,y+s_length,False)
  p.appendLineToPath(x,y,False)
  p.set_style(get_style(d))
  svg.addElement(p)
