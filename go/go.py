#!/usr/bin/python
from SVG import *
import math

#set values
boardWidth = 150.0 #mm
boardBorder = 10.0
lines = 9
laserSpacing = 2.0 ##from each other
stoneSizeRatio = 0.8 #ratio to square width
stoneCutLength = 150 #mm long side of material to cut the stones from

#calculated values
markCentre = True
if lines >= 13:
    markCorners = True
else:
    markCorners = False
stoneRadius =  stoneSizeRatio * boardWidth / lines / 2
stoneMargin = 0 # boardWidth + laserSpacing
lineWidth = boardWidth - boardBorder * 2
lineSpace = lineWidth / ( lines - 1 )
markSize = lineSpace * 0.05
numDots = lines * lines
numPieces = numDots / 2 #?
numPieces /= 2 #as we make 2 files, one for each colour
rows = int(stoneCutLength / (stoneRadius * 2 + laserSpacing ))
columns = int(numPieces / rows) 
actualNumPieces = rows * columns

import pdb; pdb.set_trace() 
def makeStones(name):
    d=Drawing(name)

    for x in range(rows):
        for y in range(columns):
            centre = ( stoneMargin + stoneRadius + x*(stoneRadius*2 + laserSpacing),stoneRadius + y*(stoneRadius*2+laserSpacing))
            d.idCircle('cut',centre,stoneRadius)
   
    d.saveas()

        
def makeBoard(name):
    d=Drawing(name)

    #cut
    d.idRectangle('cut',(0,0),boardWidth,boardWidth)

    #engraved lines
    #vern tickle
    for x in range(lines):
        points = [ ( boardBorder + x * lineSpace , boardBorder ), (boardBorder + x * lineSpace, boardBorder+ lineWidth ) ]
        d.idLine('engrave',points)

    #harry zontal
    for y in range(lines):
        points = [ ( boardBorder, boardBorder + y * lineSpace), (boardBorder + lineWidth, boardBorder + y * lineSpace) ]
        d.idLine('engrave',points)

    #marks
    if markCentre:
        d.idCircle('engrave',(boardWidth/2,boardWidth/2),markSize)

    cornerMarkDivs = 3
    if markCorners:
        d.idCircle('engrave',(boardBorder+ cornerMarkDivs * lineSpace,boardBorder+cornerMarkDivs * lineSpace),markSize)
        d.idCircle('engrave',(boardBorder+ cornerMarkDivs * lineSpace,boardBorder+lineWidth-cornerMarkDivs * lineSpace),markSize)
        d.idCircle('engrave',(boardBorder+lineWidth- cornerMarkDivs * lineSpace,boardBorder+cornerMarkDivs * lineSpace),markSize)
        d.idCircle('engrave',(boardBorder+lineWidth- cornerMarkDivs * lineSpace,boardBorder+lineWidth-cornerMarkDivs * lineSpace),markSize)

    d.saveas()

if __name__ == '__main__':
    print "making a %d x %d board, %d mm wide, with %d peices of each colour" % ( lines, lines, boardWidth, actualNumPieces )

    makeBoard('board.svg')
    makeStones('stonesB.svg')
    makeStones('stonesW.svg')
