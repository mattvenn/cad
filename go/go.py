#!/usr/bin/python
from SVG import *
import math
import argparse


def makeStones(prop,name):
    d=Drawing(name)

    for x in range(prop['rows']):
        for y in range(prop['columns']):
            centre = ( prop['stoneMargin'] + prop['stoneRadius'] + x*(prop['stoneRadius']*2 + prop['laserSpacing']),prop['stoneRadius'] + y*(prop['stoneRadius']*2+prop['laserSpacing']))
            d.idCircle('cut',centre,prop['stoneRadius'])
   
    draw100mmLine(d,0,(prop['columns']+1)*(prop['stoneRadius']*2) + 10)

    d.saveas()

        
def makeBoard(prop,name):
    d=Drawing(name)

    #cut
    d.idRectangle('cut',(0,0),prop['boardWidth'],prop['boardHeight'])

    #engraved lines
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

    draw100mmLine(d,0,prop['boardHeight'] + 10)

    d.saveas()

def draw100mmLine(d,x,y):
   d.idLine('cline',[(x,y),(x+100,y)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="go board")
    parser.add_argument('--boardwidth',
        action='store', dest='boardWidth', type=float, default="280",
        help="board width in mm")
    parser.add_argument('--lines',
        action='store', dest='lines', type=int, default=19,
        help="number of lines on the board")
    parser.add_argument('--stoneCutLength',
        action='store', dest='stoneCutLength', type=int, default=150,
        help="mm long side of material to cut the stones from")
    args = parser.parse_args()

    #set values
    prop = {}
    prop['boardWidth'] = args.boardWidth
    prop['widthHeightRatio'] = 1.1 #skew the board
    prop['lines'] = args.lines
    prop['laserSpacing'] = 2.0 ##from each other
    prop['stoneSizeRatio'] = 0.8 #ratio to square width
    prop['stoneCutLength'] = args.stoneCutLength
    prop['markCentre'] = True

    #calculated values
    prop['boardBorder'] = prop['boardWidth'] / 20
    if prop['lines'] >= 13:
        prop['markCorners'] = True
    else:
        prop['markCorners'] = False

    prop['boardHeight'] = prop['boardWidth'] * prop['widthHeightRatio']
    prop['stoneRadius'] =  prop['stoneSizeRatio'] * prop['boardWidth'] / prop['lines'] / 2
    prop['stoneMargin'] = 0 # boardWidth + laserSpacing
    prop['lineWidth'] = prop['boardWidth'] - prop['boardBorder'] * 2
    prop['lineLength'] = prop['boardHeight'] - prop['boardBorder'] * 2
    prop['lineWidthSpace'] = prop['lineWidth'] / ( prop['lines'] - 1 )
    prop['lineLengthSpace'] = prop['lineLength'] / ( prop['lines'] - 1 )
    prop['markSize'] = prop['lineWidthSpace'] * 0.05
    numDots = prop['lines'] * prop['lines']
    numPieces = numDots * 0.75 #75% of the full number
    numPieces /= 2 #as we make 2 files, one for each colour
    prop['rows'] = int(prop['stoneCutLength'] / (prop['stoneRadius'] * 2 + prop['laserSpacing'] ))
    prop['columns'] = int(numPieces / prop['rows']) 
    actualNumPieces = prop['rows'] * prop['columns']

    print "making a %d x %d board, %d mm wide, with %d stones of each colour" % ( prop['lines'], prop['lines'], prop['boardWidth'], actualNumPieces )

    makeBoard(prop,'board.svg')
    makeStones(prop,'stonesB.svg')
    makeStones(prop,'stonesW.svg')
