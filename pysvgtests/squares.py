#!/usr/bin/python
#from SVG import *
import pickle
import svgwrite
import math
import argparse

def setup(args):
  widthmm = "%fmm" % args.width
  heightmm = "%fmm" % args.height

  dwg = svgwrite.Drawing(filename="squares.svg", debug=True, size=(widthmm,heightmm))
  dwg.viewbox(width=args.width,height=args.height)
  return dwg

def square(x,y, width,dwg):
  points = []
  hWidth = width/2
  path = svgwrite.path.Path("M0,0", fill='none', stroke='black', stroke_width='0.1')
  path.push("M%d,%d" % (x-hWidth,y-hWidth))
  path.push("L%d,%d" % (x+hWidth,y-hWidth))
  path.push("L%d,%d" % (x+hWidth,y+hWidth))
  path.push("L%d,%d" % (x-hWidth,y+hWidth))
  path.push("L%d,%d" % (x-hWidth,y-hWidth))
  dwg.add(path)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description="generates square based energy drawings")
  parser.add_argument('--height',
      action='store', dest='height', type=int, default=200,
      help="height of paper")
  parser.add_argument('--width',
      action='store', dest='width', type=int, default=200,
      help="width of paper")
  parser.add_argument('--startenv',
      action='store', dest='startenv', type=int, default=0,
      help="where to start from")
  parser.add_argument('--number',
      action='store', dest='number', type=int, default=0,
      help="will end up being the time")
  parser.add_argument('--env',
      action='store', dest='env', type=int, default=0,
      help="environmental var to plot")
  parser.add_argument('--xdiv',
      action='store', dest='xdiv', type=int, default=12,
      help="divide paper into x divs")
  parser.add_argument('--ydiv',
      action='store', dest='ydiv', type=int, default=12,
      help="divide paper into y divs")
  parser.add_argument('--value',
      action='store', dest='value', type=int, default=5000,
      help="value of each square")
  parser.add_argument('--squareIncMM',
      action='store', dest='squareIncMM', type=int, default=2,
      help="mm increase in size per square")
  parser.add_argument('--load',
      action='store_const', const=True, dest='load', default=False,
      help="load values for env and number")
  parser.add_argument('--nosavestate',
      action='store_const', const=False, dest='savestate', default=True,
      help="save state")
  parser.add_argument('--drawoutline',
      action='store_const', const=True, dest='drawoutline', default=False,
      help="draw the outline of the square")


  args = parser.parse_args()
  state = {}
  loadedvars = {} 

  if args.load:
    print "using numbers from file"
    loadedvars = pickle.load( open( "vars.p", "rb" ) )
    args.number = loadedvars["number"]
    args.env = loadedvars["env"]


  if args.savestate:
    print "using saved state"
    try:
      state = pickle.load( open( "save.p", "rb" ) )
    except:
      #duplicate code, avoid?
      state["number"] = args.number
      state["startenv"] = args.startenv
       
    #if we move on to a different number, set startenv back to 0
    if args.number != state["number"]:
      state["startenv"] = 0
      state["number"] = args.number
  else:
    state["number"] = args.number
    state["startenv"] = args.startenv

  print "number:%d\nstartenv:%d\nenv:%d" % (state["number"], state["startenv"], args.env)
  
  #work out where to draw
  import math
  startx = ( args.width / args.xdiv ) * (( state["number"] ) % args.xdiv ) + args.width / (args.xdiv * 2)
  starty = ( args.width / args.ydiv ) * math.ceil(state["number"] / args.ydiv ) + args.width / (args.ydiv * 2 )
 
  print "x:%d y:%d" % ( startx, starty )

  args.env += state["startenv"]
  startSquare = int(state["startenv"] / args.value)
  endSquare = int(args.env / args.value)
  print "start sq:%d end sq:%d" % ( startSquare, endSquare )
  if endSquare > startSquare:
    #create drawing
    dwg = setup(args)

    for i in range( startSquare, endSquare ):
      width = args.squareIncMM + i * args.squareIncMM
      print "square #%d width %d" % ( i, width )
      square( startx,starty, width, dwg )

    dwg.save()

  state["startenv"] = args.env;
  pickle.dump( state, open( "save.p", "wb" ) )

  #pycam can do text natively!
  #dwg.add(dwg.text('Test', insert=(0, 0.2), fill='black'))

