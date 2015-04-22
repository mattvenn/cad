# Drilling holes

## Camera setup

* Choose 2 holes and find the co-ords for them. Ideally far apart. Put the co-ords in the [cam_offset.py] program as x1,y1 and x2,y2
* Attach pcb to bed
* move z so that bottom of green is 150mm above the bed
* find the holes and put the co-ords in the [cam_offset.py] program as a1,b1 and a2,b2

## Generate the file

run the program:

    ./cam_offset.py

check length discrepancy is small (ideally less than 0.1). 

A new file [adjust.ngc] is generated. Load this into emc and run!

## First time setup

* Find a clear spot on the board
* Move to agreed position above bed (choosing 150mm)
* Move the mill until the camera cross hair is on the hole
* Change the camera offsets in the [cam_offset.py] program.


