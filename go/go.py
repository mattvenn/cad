#!/usr/bin/python
from SVG import *
import math
import argparse


def makeStones(prop):
    d=Drawing('stones.svg')
    lasty=0
    for x in range(prop['rows']):
        for y in range(prop['columns']):
            centre = ( prop['stoneMargin'] + prop['stoneRadius'] + x*(prop['stoneRadius']*2 + prop['laserSpacing']),prop['stoneRadius'] + y*(prop['stoneRadius']*2+prop['laserSpacing']))
            lasty = centre[1]
            d.idCircle('cut',centre,prop['stoneRadius'])
   
    if prop['drawSizeLine']:
        draw100mmLine(d,0,lasty + prop['stoneRadius'] + 10)

    d.saveas()

def makeBoard(prop):
    #cut
    d=Drawing('board.svg')
    d.idRectangle('cut',(0,0),prop['boardWidth'],prop['boardHeight'])

    if prop['splitEngraveFile']:
        d.saveas()
        d=Drawing('engrave.svg')
        drawAlignmentCorners(d,prop)

    #engraved lines kindly provided by Cartesian Co-ordinates Ltd.
    #vern tickle
    for x in range(prop['lines']):
        points = [ ( prop['boardBorder'] + x * prop['lineWidthSpace'] , prop['boardBorder'] ), (prop['boardBorder'] + x * prop['lineWidthSpace'], prop['boardBorder']+ prop['lineLength'] ) ]
        d.idLine('engrave',points)

    #harry zontal
    for y in range(prop['lines']):
        points = [ ( prop['boardBorder'], prop['boardBorder'] + y * prop['lineLengthSpace']), (prop['boardBorder'] + prop['lineWidth'], prop['boardBorder'] + y * prop['lineLengthSpace']) ]
        d.idLine('engrave',points)

    #marks
    if prop['markCentre']:
        d.idCircle('engrave',(prop['boardWidth']/2,prop['boardHeight']/2),prop['markSize'])

    cornerMarkDivs = 3
    if prop['markCorners']:
        #top left
        d.idCircle('engrave',(prop['boardBorder']+ cornerMarkDivs * prop['lineWidthSpace'],prop['boardBorder']+cornerMarkDivs * prop['lineLengthSpace']),prop['markSize'])
        #bottom left 
        d.idCircle('engrave',(prop['boardBorder']+ cornerMarkDivs * prop['lineWidthSpace'],prop['boardBorder']+prop['lineLength']-cornerMarkDivs * prop['lineLengthSpace']),prop['markSize'])
        #top right
        d.idCircle('engrave',(prop['boardBorder']+prop['lineWidth']- cornerMarkDivs * prop['lineWidthSpace'],prop['boardBorder']+cornerMarkDivs * prop['lineLengthSpace']),prop['markSize'])
        #bottom right
        d.idCircle('engrave',(prop['boardBorder']+prop['lineWidth']- cornerMarkDivs * prop['lineWidthSpace'],prop['boardBorder']+prop['lineLength']-cornerMarkDivs * prop['lineLengthSpace']),prop['markSize'])

    #text
    if prop['drawText']:
        fontSize = 10 #what units?
        d.text('engrave',(prop['boardBorder'],prop['boardBorder']/2+1),"Make another board - thingiverse.com/thing:24532",fontSize)
        d.text('engrave',(prop['boardBorder'],prop['boardHeight']-(prop['boardBorder']/2)+1),"Getting started with Go - bit.ly/rQx2Lf",fontSize)

    d.saveas()

def drawAlignmentCorners(d,prop):
    cutLength = 10 #mm
    #bottom left
    points = [(cutLength,prop['boardHeight']),(0,prop['boardHeight']),(0,prop['boardHeight']-cutLength)]
    d.idLine('engrave',points)
    #top right
    points = [(prop['boardWidth']-cutLength,0),(prop['boardWidth'],0),(prop['boardWidth'],cutLength)]
    d.idLine('engrave',points)

def draw100mmLine(d,x,y):
   d.idLine('cline',[(x,y),(x+100,y)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="go board")
    parser.add_argument('--boardHeight',
        action='store', dest='boardHeight', type=float, default="280",
        help="board height in mm")
    parser.add_argument('--lines',
        action='store', dest='lines', type=int, default=19,
        help="number of lines on the board")
    parser.add_argument('--stoneCutLength',
        action='store', dest='stoneCutLength', type=int, default=280,
        help="mm long side of material to cut the stones from")
    parser.add_argument('--drawSizeLine',
        action='store_const', const=True, dest='drawSizeLine', default=False,
        help="Draw a 100mm sizing line to help with scaling problems")
    parser.add_argument('--splitEngraveFile',
        action='store_const', const=True, dest='splitEngraveFile', default=False,
        help="split the engrave file to a separate file")
    parser.add_argument('--noText',
        action='store_const', const=False, dest='drawText', default=True,
        help="don't draw the text for thingiverse and go introduction")

    args = parser.parse_args()

    #set values, must be a better way of doing this
    prop = {}
    prop['drawText'] = args.drawText
    prop['drawSizeLine'] = args.drawSizeLine
    prop['splitEngraveFile'] = args.splitEngraveFile
    prop['boardHeight'] = args.boardHeight
    prop['widthHeightRatio'] = 0.95 #skew the board
    prop['lines'] = args.lines
    prop['laserSpacing'] = 2.0 ##from each other
    prop['stoneSizeRatio'] = 0.9 #ratio to square width
    prop['stoneCutLength'] = args.stoneCutLength
    prop['markCentre'] = True

    #calculated values
    prop['boardBorder'] = prop['boardHeight'] / 20
    if prop['lines'] >= 13:
        prop['markCorners'] = True
    else:
        prop['markCorners'] = False

    prop['boardWidth'] = prop['boardHeight'] * prop['widthHeightRatio']
    prop['stoneRadius'] =  prop['stoneSizeRatio'] * prop['boardWidth'] / prop['lines'] / 2
    prop['stoneMargin'] = 0 # boardWidth + laserSpacing
    prop['lineWidth'] = prop['boardWidth'] - prop['boardBorder'] * 2
    prop['lineLength'] = prop['boardHeight'] - prop['boardBorder'] * 2
    prop['lineWidthSpace'] = prop['lineWidth'] / ( prop['lines'] - 1 )
    prop['lineLengthSpace'] = prop['lineLength'] / ( prop['lines'] - 1 )
    prop['markSize'] = prop['lineWidthSpace'] * 0.03
    numDots = prop['lines'] * prop['lines']
    numPieces = numDots * 0.75 #75% of the full number
    numPieces /= 2 #as we make 2 files, one for each colour
    prop['columns'] = int(prop['stoneCutLength'] / (prop['stoneRadius'] * 2 + prop['laserSpacing'] ))
    prop['rows'] = int(numPieces / prop['columns']) 
    actualNumPieces = prop['rows'] * prop['columns']

    print "making a %d x %d board, (%d mm x %d mm), with %d stones of each colour" % ( prop['lines'], prop['lines'], prop['boardWidth'], prop['boardHeight'], actualNumPieces )

    #actually do it
    makeBoard(prop)
    makeStones(prop)
