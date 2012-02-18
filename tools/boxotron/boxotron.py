#!/usr/bin/python

# box-o-tron svg 0.1
# 2012 02 18
# Matt Venn
# GPL

# original boxotron: http://www.thingiverse.com/thing:404
# Simon Kirkby
# tigger@interthingy.com
# posted on thingiverse.com

import os,string,math
from SVG import *
from optparse import OptionParser
import ConfigParser

#bolt = 3.0 # size of the bolt
#bolt_length = 15.0 # length of the bolt
#bolt_tab_clearance = 2  # x times the size of the bolt
#nut_multiplier = 1.7 # diameter of the bolt to flats of the nut
nut_depth = 0.5 # proportion of the length of the bolt that the nut is placed


class construct:
    def __init__(self,opt,d):
        self.thickness = opt.thickness 
        self.opt = opt
        # main box
        self.box = box(opt)
        self.extra = []
        self.drawing = d

    def gen(self):
        print "Construct"
        d = self.drawing
        self.box.gen(d)
        for i in self.extra:
            i.gen(d)
        print "Finished Construction"
    
    def add(self,obj):
        self.extra.append(obj)

class box:
    def __init__(self,opt):
        self.opt = opt
        y = opt.length
        x = opt.width
        z = opt.depth
        self.x = x
        self.y = y
        self.z = z 
        self.faces = []
        self.blocks = []
        # generate the 6 sides
        top = face('top',x,z,opt)
        bottom = face('bottom',x,z,opt)
        left = face('left',y,z,opt)
        right = face('right',y,z,opt)
        front = face('front',x,y,opt)
        back = face('back',x,y,opt)
        self.faces.append(top)
        self.faces.append(left)
        self.faces.append(bottom)
        self.faces.append(right)
        self.faces.append(front)
        self.faces.append(back)
        # generate the 12 edges and bind
        # slot = 0 , tab = 1 , none = 2
        top.set_edges(0,0,0,0)
        bottom.set_edges(0,0,0,0)
        left.set_edges(0,1,0,1)
        right.set_edges(0,1,0,1)
        front.set_edges(1,1,1,1)
        back.set_edges(1,1,1,1)
        # set the inset
        t = self.opt.thickness
        h  = self.opt.inset + self.opt.thickness/2.0    
        top.set_inset(0,0,0,0)
        bottom.set_inset(0,0,0,0)
        left.set_inset(t,0,t,0)
        right.set_inset(t,0,t,0)
        front.set_inset(h,t,h,t)
        back.set_inset(h,t,h,t)
        
    def layout(self):
        width = self.opt.width
        height = self.opt.length
        depth = self.opt.depth
        clearance = self.opt.clearance
        # layout the sections in an unfolded cube
        x = 0 
        for i in range(4):
            self.faces[i].sx = x
            self.faces[i].sy = height + 2 * clearance
            x = x + self.faces[i].x + 2*clearance
        self.faces[4].sx = height + width + 4 * clearance
        self.faces[5].sx = height + width + 4 * clearance
        self.faces[5].sy = depth + height + 4 * clearance

    def gen(self,d):
        self.layout()
        for i in self.faces:
            i.gen(d)
        # add them into the drawing

class face:
    # faces are generated anticlockwise from bottom left
    def __init__(self,name,x,y,opt):
        self.name = name
        self.opt = opt
        self.sx = 0 
        self.sy = 0
        self.x = x
        self.y = y
        self.extra = [] 
        self.edges = []
        self.inset = []
        self.set_type(opt.type)

    def set_type(self,type):
        if type == 'slot':
            self.slot = self.simple_slot
            self.tab = self.simple_tab
        if type == 'bolt':
            self.slot = self.bolt_slot
            self.tab= self.bolt_tab

    def set_inset(self,a,b,c,d):
        self.inset= []
        self.inset.append(a)
        self.inset.append(b)
        self.inset.append(c)
        self.inset.append(d)

    def set_edges(self,a,b,c,d):
        self.edges = []
        self.edges.append(a)
        self.edges.append(b)
        self.edges.append(c)
        self.edges.append(d)

    
    def bolt_slot(self,d,x,y,orient,flip):
        if flip == 0:
            flipper = 1
        else:
            flipper = -1
        sr = self.opt.radius
        hl = self.opt.slot_length / 2.0
        ht = self.opt.thickness / 2.0
        db = self.opt.bolt * self.opt.bolt_tab_clearance 
        hs = self.opt.slot_length / 2.0 
        co = self.opt.bolt_hole_offset * flipper
        thickness = self.opt.thickness

        """ work in progress
        if self.name == 'top' and self.opt.bigslot:
            print "setting hl to width"
            if orient == 'h':
                hs = self.opt.width / 2
                hl = self.opt.width / 2
            if orient == 'v':
                hs = self.opt.depth / 2
                hl = self.opt.depth / 2
        """

        if orient == 'h':
            d.Circle(cent=(x,y+co),radius=self.opt.bolt/2.0)
            d.Rectangle(point=(x-hl-sr,y-ht),width=hs-db+2*sr,height=thickness)
            d.Rectangle(point=(x-hl-sr+hs+db,y-ht),width=hs-db+2*sr,height=thickness)
        if orient == 'v':
            d.Circle(cent=(x+co,y),radius=self.opt.bolt/2.0)
            d.Rectangle(point=(x-ht,y-hl-sr),height=hs-db+2*sr,width=thickness)
            d.Rectangle(point=(x-ht,y-hl-sr+hs+db),height=hs-db+2*sr,width=thickness)

    def bolt_tab(self,d,x,y,orient,flip):
        # bolty tab
        #d.append(Circle(center=(x,y),radius=bolt/2,layer="CONSTRUCTION"))
        # flip left right , up down
        if flip == 0:
            flipper = 1
        else:
            flipper = -1
        hl = self.opt.slot_length / 2.0
        ht = self.opt.thickness / 2.0
        fl = self.opt.thickness * flipper
        bf = ( self.opt.bolt_length + self.opt.radius ) * flipper
        db = self.opt.bolt * self.opt.bolt_tab_clearance 
        hb = self.opt.bolt / 2.0
        bb = ( self.opt.bolt + self.opt.radius )* flipper
        hs = self.opt.slot_length / 2.0 
        nd = self.opt.bolt_length * self.opt.nut_depth * flipper
        nw = self.opt.bolt * self.opt.nut_multiplier / 2.0
        thickness = self.opt.thickness
        if orient == 'h':
            # tab 1 
            d.Line(points=[(x-hl,y),(x-hl,y-fl)])
            d.Line(points=[(x-hl,y-fl),(x+hl-hs-db,y-fl)])
            d.Line(points=[(x-hl+hs-db,y),(x-hl+hs-db,y-fl)])
            # tab 2
            d.Line(points=[(x+hl-hs+db,y),(x+hl-hs+db,y-fl)])
            d.Line(points=[(x+hl-hs+db,y-fl),(x+hl,y-fl)])
            d.Line(points=[(x+hl,y),(x+hl,y-fl)])
            # bolt hole vertical 
            d.Line(points=[(x-hl+hs-db,y),(x-hb,y)])
            d.Line(points=[(x-hb,y),(x-hb,y+nd)])
            # bolt detent a
            d.Line(points=[(x-hb,y+nd),(x-nw,y+nd)])
            d.Line(points=[(x-nw,y+nd),(x-nw,y+nd+bb)])
            d.Line(points=[(x-nw,y+nd+bb),(x-hb,y+nd+bb)])
            d.Line(points=[(x-hb,y+nd+bb),(x-hb,y+bf)])
            # bottom
            d.Line(points=[(x+hb,y+bf),(x-hb,y+bf)])
            # bolt detent b
            d.Line(points=[(x+hb,y+nd+bb),(x+hb,y+bf)])
            d.Line(points=[(x+nw,y+nd+bb),(x+hb,y+nd+bb)])
            d.Line(points=[(x+nw,y+nd),(x+nw,y+nd+bb)])
            d.Line(points=[(x+hb,y+nd),(x+nw,y+nd)])
            # side
            d.Line(points=[(x+hb,y+nd),(x+hb,y)])
            # top
            d.Line(points=[(x+hb,y),(x+hl-hs+db,y)])

        if orient == 'v':
            #d.Line(points=[(x+fl,y-hl),(x+fl,y+hl)])
            # tab 1
            d.Line(points=[(x,y-hl),(x+fl,y-hl)])
            d.Line(points=[(x+fl,y-hl),(x+fl,y-hl+hs-db)])
            d.Line(points=[(x,y-hl+hs-db),(x+fl,y-hl+hs-db)])
            # tab 2
            d.Line(points=[(x,y+hl),(x+fl,y+hl)])
            d.Line(points=[(x+fl,y+hl),(x+fl,y+hl-hs+db)])
            d.Line(points=[(x,y+hl-hs+db),(x+fl,y+hl-hs+db)])
            #bolt hole horizontal
            d.Line(points=[(x,y-hl+hs-db),(x,y-hb)])
            d.Line(points=[(x,y-hb,),(x-nd,y-hb)])
            # bolt detent a
            d.Line(points=[(x-nd,y-hb),(x-nd,y-nw)])
            d.Line(points=[(x-nd,y-nw),(x-nd-bb,y-nw)])
            d.Line(points=[(x-nd-bb,y-nw),(x-nd-bb,y-hb)])
            d.Line(points=[(x-nd-bb,y-hb),(x-bf,y-hb)])
            # bottom
            d.Line(points=[(x-bf,y-hb),(x-bf,y+hb)])
            # bolt detent a
            d.Line(points=[(x-nd,y+hb),(x-nd,y+nw)])
            d.Line(points=[(x-nd,y+nw),(x-nd-bb,y+nw)])
            d.Line(points=[(x-nd-bb,y+nw),(x-nd-bb,y+hb)])
            d.Line(points=[(x-nd-bb,y+hb),(x-bf,y+hb)])
            # side
            d.Line(points=[(x-nd,y+hb,),(x,y+hb)])
            d.Line(points=[(x,y+hb),(x,y+hl-hs+db)])


    def simple_slot(self,d,x,y,orient):
        hl = self.opt.slot_length / 2.0
        ht = self.opt.thickness / 2.0
        slot_length = self.opt.slot_length
        thickness = self.opt.thickness
        if orient == 'h':
            d.Rectangle(point=(x-hl,y-ht,0),width=slot_length,height=thickness)
        if orient == 'v':
            d.Rectangle(point=(x-ht,y-hl,0),height=slot_length,width=thickness)

    def simple_tab(self,d,x,y,orient,flip):
        # flip left right , up down
        if flip == 0:
            flipper = 1
        else:
            flipper = -1
        hl = self.opt.slot_length / 2.0
        ht = self.opt.thickness / 2.0
        fl = self.opt.thickness*flipper
        if orient == 'h':
            d.Line(points=[(x-hl,y-fl),(x+hl,y-fl)])
            d.Line(points=[(x-hl,y),(x-hl,y-fl)])
            d.Line(points=[(x+hl,y),(x+hl,y-fl)])
        if orient == 'v':
            d.Line(points=[(x+fl,y-hl),(x+fl,y+hl)])
            d.Line(points=[(x,y-hl),(x+fl,y-hl)])
            d.Line(points=[(x,y+hl),(x+fl,y+hl)])

    def gen(self,d):
        print '\tgen face ' + self.name + ' ('+str(self.x)+','+str(self.y)+')'
        sx = self.sx
        sy = self.sy
        x = self.x
        y = self.y
        # basic outline ( for inset testing ) 
        d.CLine(points=[(sx,sy),(sx+x,sy)])
        d.CLine(points=[(sx+x,sy),(sx+x,sy+y)])
        d.CLine(points=[(sx,sy),(sx,sy+y)])
        d.CLine(points=[(sx,sy+y),(sx+x,sy+y)])

        # bodging up inset 
        osx = self.sx
        osy = self.sy
        sx = self.sx + self.inset[0]
        sy = self.sy + self.inset[1]
        x = self.x - self.inset[0] - self.inset[2]
        y = self.y - self.inset[1] - self.inset[3]
        # calculations 
        xjoins = int(self.x/self.opt.join_every)-1
        if xjoins == 0:
            xjoins = 1

        if self.opt.bigslot:
            xjoins = 1

        xstart = self.x/(xjoins*2)
        xinc = self.x/xjoins

        yjoins = int(self.y/self.opt.join_every)-1
        if yjoins == 0:
            yjoins = 1

        if self.opt.bigslot:
            yjoins = 1

        ystart = self.y/(yjoins*2)
        yinc = self.y/yjoins
        hl = self.opt.slot_length / 2.0
        inset = self.opt.inset
        slot_length = self.opt.slot_length
        # first
        if self.edges[0] == 0:
            d.Line(points=[(sx,sy),(sx+x,sy)])
            for i in range(0,xjoins):
                self.slot(d,osx+xstart+i*xinc,sy+inset,'h',0)
        if self.edges[0] == 1:
            d.Line(points=[(sx,sy),(osx+xstart-hl,sy)])
            for i in range(0,xjoins):
                if i < xjoins-1:
                    d.Line(points=[(osx+xstart+i*xinc+hl,sy),(osx+xstart+(i+1)*xinc-hl,sy)])
                self.tab(d,osx+xstart+i*xinc,sy,'h',0)
            d.Line(points=[(osx+xinc*xjoins-xstart+hl,sy),(sx+x,sy)])
            
        # second
        if self.edges[1] == 0:
            d.Line(points=[(sx+x,sy),(sx+x,sy+y)])
            for i in range(0,yjoins):
                self.slot(d,osx + x - inset ,osy+ystart+i*yinc,'v',1)
        if self.edges[1] == 1:
            d.Line(points=[(sx+x,sy),(sx+x,osy+ystart-hl)])
            for i in range(0,yjoins):
                if i < yjoins-1:
                    d.Line(points=[(sx+x,osy+ystart+i*yinc+hl),(sx+x,osy+ystart+(i+1)*yinc-hl)])
                self.tab(d,sx+x,osy+ystart+i*yinc,'v',0)
            d.Line(points=[(sx+x,osy+yinc*yjoins-ystart+hl),(sx+x,sy+y)])

        # third 
        if self.edges[2] == 0:
            d.Line(points=[(sx,sy+y),(sx+x,sy+y)])
            for i in range(0,xjoins):
                self.slot(d,osx+xstart+i*xinc,osy+y-inset,'h',1)
        if self.edges[2] == 1:
            d.Line(points=[(sx,sy+y),(osx+xstart-hl,sy+y)])
            for i in range(0,xjoins):
                if i < xjoins-1:
                    d.Line(points=[(osx+xstart+i*xinc+hl,sy+y),(osx+xstart+(i+1)*xinc-hl,sy+y)])
                self.tab(d,osx+xstart+i*xinc,sy+y,'h',1)
            d.Line(points=[(osx+xinc*xjoins-xstart+hl,sy+y),(sx+x,sy+y)])

        # fourth
        if self.edges[1] == 0:
            d.Line(points=[(sx,sy),(sx,sy+y)])
            for i in range(0,yjoins):
                self.slot(d,osx + inset ,osy+ystart+i*yinc,'v',0)
        if self.edges[1] == 1:
            d.Line(points=[(sx,sy),(sx,osy+ystart-hl)])
            for i in range(0,yjoins):
                if i < yjoins-1:
                    d.Line(points=[(sx,osy+ystart+i*yinc+hl),(sx,osy+ystart+(i+1)*yinc-hl)])
                self.tab(d,sx,osy+ystart+i*yinc,'v',1)
            d.Line(points=[(sx,osy+yinc*yjoins-ystart+hl),(sx,sy+y)])
        #label
        d.Text(self.name,point=(sx+x/2,sy+y/2,0),height=5)
        for i in self.extra:
            i.gen(d)


def conffile(opt,config_file):
    c = ConfigParser.ConfigParser()
    try:
        os.stat(config_file)
        # read the configs
        c.readfp(open(config_file))
        items = c.options('default')
        # scan through the options
        for i in items:
            value = c.get('default',i)
            # cast as float if you can
            try:
                value = float(value)
            except:
                pass
            vars(opt)[i] = value 
    except:
        # no config file, strip out defaults and write to config.
        print 'no such config , populating default '
        c.add_section('default')
        k = vars(opt).keys()
        for i in k:
            c.set('default',i,vars(opt)[i])
        c.write(open(config_file,'w'))
        
def parse(parser):
    # parse the command line options
    print 'Options'
    # define the command line variables
    parser.add_option("-l","--length",dest="length",help="Length of box in mm",type=float,default=100.0)
    parser.add_option("-w","--width",dest="width",help="width of box in mm",type=float,default=100.0)
    parser.add_option("-d","--depth",dest="depth",help="depth of box in mm",type=float,default=100.0)
    parser.add_option("-t","--thickness",dest="thickness",help="thickness of material in mm",type=float,default=3.0)
    parser.add_option("-c","--clearance",dest="clearance",help="clearance between panels of material in mm",type=float,default=3.0)
    parser.add_option("-i","--inset",dest="inset",help="inset to middle of slot material in mm",type=float,default=5.0)
    parser.add_option("-s","--slot_length",dest="slot_length",help="length of slot in mm",type=float,default=60.0)
    parser.add_option("-f","--file_name",dest="filename",help="file_name",default="box.svg")
    parser.add_option("-j","--join_every",dest="join_every",type=float,help="join every x in mm ",default=60.0)
    parser.add_option("--type",dest="type",help="box type = slot , bolt ",default="bolt")
    parser.add_option("-b","--bolt_size",dest="bolt",help="bolt size in mm",type=float,default=3.0)
    parser.add_option("--bolt_length",dest="bolt_length",help="bolt length in mm",type=int,default=16.0)
    parser.add_option("--bolt_clearance",dest="bolt_tab_clearance",help="clearance between bolt and tab , multiple of bolt size",type=float,default=2.0)
    parser.add_option("--nut_multiplier",dest="nut_multiplier",help="nut size - multiple of bolt size",type=float,default=1.9)
    parser.add_option("--nut_depth",dest="nut_depth",help="nut depth - multiple of bolt size",type=float,default=0.5)
    parser.add_option("--radius",dest="radius",help="radius of cutting bit",type=float,default=1.5)
    parser.add_option("--bolt_hole_offset",dest="bolt_hole_offset",help="allows you to move the bolt further away from the edge - useful with low inset values",type=float,default=0)
    parser.add_option("--minslots",dest="bigslot",help="overrides a bunch of options to give you the biggest joins with fewest bolts",action="store_true")
        
def main():
    op = OptionParser()
    parse(op)
    (option,args) = op.parse_args()
    if len(args) == 1:
        if args[0][-3:] == 'cfg':
            print "using " + args[0]    
            conffile(option,args[0])
        else:
            print 'config file name must end in .cfg'

    #sanity checking
    
    safety_gap = 0
    #a half assed guess at what the minimum amount of material we can remove with a mill
    if option.radius > 0:
        safety_gap = option.radius * 2

    #check slot tabs are at least 2mm wide
    min_slot = 2*(option.bolt * option.bolt_tab_clearance) + safety_gap 
    if option.slot_length < min_slot:
        print 'impossibly small slot length for this bolt size and bolt clearance'
        print 'slot length must be at least %d mm' % min_slot
        exit(1)

    #check inset is more than 1/2 thickness
    if option.inset < option.thickness/2:
        print 'inset has to be more than 1/2 thickness: %f mm' % (option.thickness / 2)
        exit(1)

    #check slot length is smaller than minimum dimension
    min_dim = min( option.length, option.depth, option.width )

    max_slot = (min_dim - (2 * option.thickness +option.radius * 2+2*safety_gap))
    if option.slot_length > max_slot:
        print 'slot length (%f) is more than room available on smallest dimension. Needs to be less than %f' % (option.slot_length,min_dim+max_slot-min_dim)
        exit(1)

    #check join_every vs min_dim is valid
    if option.join_every > min_dim:
        print 'join_every is bigger than the smallest dimension: %d' % min_dim
        exit(1)

    #check bolt_hole_offset is small
    if option.bolt_hole_offset > 2:
        print "bolts won't work if bolt_hole_offset is more than 2mm"
        exit(1)

    #fixups

    #bolt length was depth of bolt hole in material, rather than actual bolt length
    option.bolt_length = option.bolt_length - option.thickness

    # create the drawing
    d = Drawing(option.filename)
    # generate the box object
    cc = construct(option,d)
    # generage the dxf file
    cc.gen()
    d.saveas()

if __name__ == '__main__' : main()
