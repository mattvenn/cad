from pysvg.shape import *
from pysvg import parser
from pysvg.style import *
from pysvg.builders import *

def get_construction_style(defaults):
    style=StyleBuilder()
    style.setFontFamily(fontfamily="Digital-7")
    style.setFontSize(defaults["fontsize"]) 
    style.setStroke("blue")
    style.setStrokeWidth(defaults["stroke"])
    style.setFilling("none")
    return style.getStyle()

def get_cut_style(defaults):
    style=StyleBuilder()
    style.setFontFamily(fontfamily="Digital-7")
    style.setFontSize(defaults["fontsize"]) 
    style.setStroke("#000")
    style.setStrokeWidth(defaults["stroke"])
    style.setFilling("none")
    return style.getStyle()

