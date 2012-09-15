#!/usr/bin/python
from SVG import *
import math
import argparse


def makeStones(prop):
    height = prop['stoneCutLength']
    width = prop['rows'] * (prop['stoneDiameter']  + prop['laserSpacing'] ) + prop['laserSpacing'] 
    d=Drawing('stones.svg',width,height)
    lasty=0
    for x in range(prop['rows']):
        for y in range(prop['columns']):
            centre = ( prop['laserSpacing'] + prop['stoneDiameter'] /2 + x*(prop['stoneDiameter'] + prop['laserSpacing']),prop['laserSpacing']+prop['stoneDiameter'] /2 + y*(prop['stoneDiameter']+prop['laserSpacing']))
            lasty = centre[1]
            d.idCircle('cut',centre,prop['stoneDiameter']/2)
   
    if prop['drawSizeLine']:
        draw100mmLine(d,0,lasty + prop['stoneDiameter']/2 + 10)

    d.saveas()

def makeBoard(prop):
    #cut
    d=Drawing('board.svg',prop['boardWidth'],prop['boardHeight'])
    d.idRectangle('cut',(0,0),prop['boardWidth'],prop['boardHeight'],prop['stoneDiameter'])

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
        fontSize = prop['boardBorder'] / 3 
        d.text('engrave',(prop['boardBorder'],prop['boardBorder']/2),"Make another board - thingiverse.com/thing:24532",fontSize)
        d.text('engrave',(prop['boardBorder'],prop['boardHeight']-(prop['boardBorder']/2)),"Getting started with Go - bit.ly/rQx2Lf",fontSize)

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
        action='store', dest='boardHeight', type=float,
        help="board height in mm")
    parser.add_argument('--stoneDiameter',
        action='store', dest='stoneDiameter', type=float,
        help="diameter of stones in mm")
    parser.add_argument('--lines',
        action='store', dest='lines', type=int, default=19,
        help="number of lines on the board")
    parser.add_argument('--stoneCutLength',
        action='store', dest='stoneCutLength', type=int, default=455,
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

    #measured from my big go board
    defaultBoardHeight=455.0
    defaultBoardBorder=17
    defaultStoneDiameter=21.6
    defaultBoardBorderToMarksHeightRatio = 17.0 / 422.0

    prop['drawText'] = args.drawText
    prop['drawSizeLine'] = args.drawSizeLine
    prop['splitEngraveFile'] = args.splitEngraveFile
    prop['widthHeightRatio'] = 0.93 #skew the board
    prop['lines'] = args.lines
    prop['laserSpacing'] = 2.0 ##from each other
    prop['stoneSizeRatio'] = 0.99 #ratio to square width
    prop['stoneCutLength'] = args.stoneCutLength
    prop['markCentre'] = True

#        prop['boardBorder'] = args.boardHeight * defaultBoardBorderToHeightRatio
    #specify stones or width?
    if args.stoneDiameter:
        squareWidth = args.stoneDiameter * 1/prop['stoneSizeRatio'] 
        boardMarksWidth = squareWidth * ( args.lines - 1 )
        boardMarksHeight=boardMarksWidth * 1/prop['widthHeightRatio']
        prop['boardBorder'] = boardMarksHeight * defaultBoardBorderToMarksHeightRatio
        prop['boardHeight'] = boardMarksHeight +prop['boardBorder']*2
        prop['stoneDiameter'] = args.stoneDiameter
    elif args.boardHeight:
        boardMarksHeight = 1 / (( defaultBoardBorderToMarksHeightRatio * 2 + 1 ) / args.boardHeight ) 
        boardMarksWidth = boardMarksHeight * prop['widthHeightRatio'] 
        stoneDiameter = boardMarksWidth / ( prop['lines'] -1 )
        prop['stoneDiameter'] = stoneDiameter * prop['stoneSizeRatio']
        prop['boardHeight'] = args.boardHeight
        prop['boardBorder'] = boardMarksHeight * defaultBoardBorderToMarksHeightRatio
    else:
        prop['boardHeight'] = defaultBoardHeight
        prop['stoneDiameter'] = defaultStoneDiameter
        prop['boardBorder'] = defaultBoardBorder

    #calculated values
    if prop['lines'] >= 13:
        prop['markCorners'] = True
    else:
        prop['markCorners'] = False

    prop['boardWidth'] = prop['boardHeight'] * prop['widthHeightRatio']
    prop['stoneMargin'] = 0 # boardWidth + laserSpacing
    prop['lineWidth'] = prop['boardWidth'] - prop['boardBorder'] * 2
    prop['lineLength'] = prop['boardHeight'] - prop['boardBorder'] * 2
    prop['lineWidthSpace'] = prop['lineWidth'] / ( prop['lines'] - 1 )
    prop['lineLengthSpace'] = prop['lineLength'] / ( prop['lines'] - 1 )
    prop['markSize'] = prop['lineWidthSpace'] * 0.03
    numDots = prop['lines'] * prop['lines']
    numPieces = numDots # * 0.75 #75% of the full number
    numPieces /= 2 #as we make 2 files, one for each colour
    prop['columns'] = int(( prop['stoneCutLength'] - prop['laserSpacing'] )  / ( (prop['stoneDiameter']  + prop['laserSpacing'] )))
    prop['rows'] = int(numPieces / prop['columns']) 
    actualNumPieces = prop['rows'] * prop['columns']

    print "making a %d x %d board, (%d mm x %d mm including % dmm border), with %d %.1fmm stones of each colour" % ( prop['lines'], prop['lines'], prop['boardWidth'], prop['boardHeight'], prop['boardBorder'], actualNumPieces, prop['stoneDiameter'] )

    #actually do it
    makeBoard(prop)
    makeStones(prop)
