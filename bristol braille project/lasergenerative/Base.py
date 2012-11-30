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
    solenoid(defaults,svg,20,20)

def solenoid(d,svg,x,y):
  trough_width = 8
  trough_height= 8
  s_width=d["solenoid"]["width"]
  s_height=d["solenoid"]["length"]
  lip = (d["solenoid"]["width"]-trough_width)/2
  p = path("M%d,%d" % (x,y))
  p.appendLineToPath(x+s_width,y,False)
  p.appendLineToPath(x+s_width,y+s_height,False)
  p.appendLineToPath(x+s_width-lip,y+s_height,False)
  p.appendLineToPath(x+s_width-lip,y+s_height+trough_height,False)
  p.appendLineToPath(x+lip,y+s_height+trough_height,False)
  p.appendLineToPath(x+lip,y+s_height,False)
  p.appendLineToPath(x,y+s_height,False)
  p.appendLineToPath(x,y,False)
  p.set_style(get_style(d))
  svg.addElement(p)
  
