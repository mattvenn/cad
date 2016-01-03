#!/usr/bin/python

import os
import math
import argparse
from xml.sax.saxutils import escape

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

def get_font_style(fontsize):
        style=StyleBuilder()
        style.setFontFamily(fontfamily=args.font)
        style.setFontSize(fontsize) 
        style.setFilling("black")
        return style.getStyle()

def get_line_style():
        style=StyleBuilder()
        style.setFilling("none")
        style.setStroke("black")
        style.setStrokeWidth("0.1")
        return style.getStyle()

def write_label(svg,labeltext,x=0,y=0):

        #xml escape
        labeltext = escape(labeltext)
        if args.toupper:
                labeltext = str.upper(labeltext)
        #if autofontsize, work out max fontsize that will fit
        if args.autofontsize:
            autofontsize = 1
            textWidth=0
            textHeight=0
            while textWidth+label_margin < width and textHeight+label_margin < height:
                (textWidth,textHeight)=get_font_size(autofontsize,labeltext)
                autofontsize+=1
            autofontsize-=1
            global fontsize
            fontsize=autofontsize
        #otherwise just check the default font size will fit
        else:
            (textWidth,textHeight)=get_font_size(fontsize,labeltext)
            if textWidth+label_margin > width or textHeight+label_margin > height:
                print "text too big, try a smaller font"
                exit(1)

        #positioning
        x+=(width-textWidth)/2
        y+=height/2+textHeight/2
        y=y+args.y_offset
        x=x+args.x_offset
        t=text(labeltext,x+margin,y+margin)
        t.set_style(get_font_style(fontsize))
        svg.addElement(t)

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

def square(dwg,x=0,y=0):

    x+=margin
    y+=margin
    points = []

    p = path("M%d,%d" % (x,y))
    p.appendLineToPath(x,y+height,False)
    p.appendLineToPath(x+width,y+height,False)
    p.appendLineToPath(x+width,y,False)
    p.appendLineToPath(x,y,False)
    p.set_style(get_line_style())
    dwg.addElement(p)

        
def setup(pagewidth,pageheight):
    widthmm = "%fmm" % pagewidth
    heightmm = "%fmm" % pageheight
    print "page size %dmm x %dmm" % (pagewidth,pageheight)

    dwg = svg(width=widthmm,height=heightmm)
    dwg.set_viewBox("0 0 %s %s" % (pagewidth, pageheight))
    return dwg

def print_label(args,text):

    pagewidth=width+2*margin
    pageheight=height+2*margin
    dwg = setup(pagewidth,pageheight)
    square(dwg)
    write_label(dwg,text)

    filename = 'label'
    dwg.save(filename + ".svg")
    os.system("inkscape -E %s.eps %s.svg" % (filename,filename)) 
    os.system("lp -d Zebra_LP2824 %s.eps" % (filename))

    #get rid of old temp files
    if args.remove:
        os.system("rm %s.svg" % filename)
        os.system("rm %s.eps" % filename)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='''program to print to zebra label printer.

        process a newline separated file in one go with --file argument

        requirements
        ------------

        * an old version of pysvg: http://code.google.com/p/pysvg/downloads/detail?name=pysvg-0.2.1.zip&can=2&q=
        * some python modules that can query ttf fonts:
                * http://pypi.python.org/pypi/TTFQuery
                * http://sourceforge.net/projects/fonttools/?source=dlp
        * an up to date version of pstoedit http://www.pstoedit.net/
        * inkscape

	printer setup
	-------------

	* use cups at localhost:631, login as your username and password (make sure in the lpadmin group)
	* add zebra usb printer, epl2, custom label 50x25mm
''')

    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file',
            action='store', dest='file',
            help="file to generate labels from")
    group.add_argument('text',
            default=None, nargs='?',
            help="text to print")
    argparser.add_argument('--font',
            action='store', dest='font', default="DejaVu Sans Condensed",
            help="font to use")
    argparser.add_argument('--x_offset',
            action='store', dest='x_offset', type=int, default=0,
            help="positive numbers move text right")
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
    group = argparser.add_mutually_exclusive_group()
    group.add_argument('--fontsize',
            action='store', type=int, dest='fontsize', default=None,
            help="override default fontsize")
    group.add_argument('--autofontsize',
            action='store_const', const=True, dest='autofontsize', default=True,
            help="work out maximum font size for the label")
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
        height=25
        width=50
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

    #margin from the page's width to the outside of the label
    margin = 0
    #twice the margin from the outer edge of the label to the closest text
    label_margin = 10

    if args.debug:
        print "label size %dx%dmm, fontsize %d" % (height,width,fontsize)


    font=find_font()

    #if only one label:
    if args.text:        
        print_label(args,args.text)
    #make a sheet
    elif args.file:
        labels=[]
        list=open(args.file)
        labels=list.read().splitlines()
        for label in labels:
            print_label(args,label)
