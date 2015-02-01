# Harmonograph

A [harmonograph](http://en.wikipedia.org/wiki/Harmonograph) is a simple machine that draws amazing patterns. 

This is an attempt to make a computer program that produces similiar patterns with additional features:

* allow an extra sine wave for modulating pen width
* export the path as a GCODE file for engraving with a CNC machine
* export path as SVG

![sine](sine.png)

# Controls

All sliders have minimum at the bottom and max at the top.

## Main controls

* points - number of points to calculate
* res - time resolution - will make curves smoother but more calculations required

## Sine controls

You have 4 sine waves that are added to get the x and y of the curve. The
controls are:

* a - amplitude
* f - frequency
* p - phase
* A - angle
* d - damping

The final sine (5) controls the pen thickness (or z depth). Angle (A) has no
effect.

# Requirements

* Python
* Tkinter (should be installed with your Python)
* PIL library:
    * Linux - sudo pip install PIL
    * [Mac](http://stackoverflow.com/questions/9070074/how-to-install-pil-on-mac-os-x-10-7-2-lion)
    * [Windows](http://stackoverflow.com/a/4579917)

# Todo

* done - add damping?
* done - global scale for zooming
* done - define min and max z
* done - define size for gcode export
* fix bad zsine stuff
* ditch binded variables?
* save export settings
* z damping should -> 0 width rather than A width

# Notes on the code

Scale widgets don't use callback because when they are loaded at the program
start they then queue events for update() to be drawn lots of times (once for
each slider).

Image is made larger than you see and then resized with anti aliasing. This is
because PIL can't draw antialiased lines and I wanted the curves to look good.
