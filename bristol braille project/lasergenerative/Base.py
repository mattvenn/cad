from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.structure import svg
from pysvg.builders import *

from Styles import get_style

def base(defaults,svg):
    x=defaults["width"]/2
    y=defaults["height"]/2
#    t=text("yo",x,y)
#    t.set_style(get_style(defaults))
    r=rect(0,0,50,50,5,5)
    r.set_style(get_style(defaults))
    svg.addElement(r)
    x=10
    y=10
    sol_num=0
    for i in range(defaults["solenoid"]["number"]):
      solenoid(defaults,svg,x,y)
      sol_num+=1
      x=x+defaults["solenoid"]["x_shift"]
      y=y+defaults["solenoid"]["y_shift"]
      if sol_num == 4:
        y=10

def solenoid(d,svg,x,y):
  trough_width = 8
  trough_length= d["solenoid"]["t_length"]
  s_width=d["solenoid"]["width"]
  s_length=d["solenoid"]["length"]
  lip = (d["solenoid"]["width"]-trough_width)/2
  p = path("M%d,%d" % (x,y))
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
  
