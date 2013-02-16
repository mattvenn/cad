#!/usr/bin/python
import argparse
from PIL import Image, ImageDraw

def get_main_color(img):
    colors = img.getcolors(img.size[0]*img.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

def get_region_box(img,x,y):
    
    cell_width = img.size[0]/args.xdiv
    cell_height = img.size[1]/args.ydiv
    box = (
        x*cell_width,
        y*cell_height,
        x*cell_width+cell_width,
        y*cell_height+cell_height)
    return box

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="make a gcode file from a pic")

    parser.add_argument('--image', action='store', dest='image_file', help="image", required = True)
    parser.add_argument('--xdiv', action='store', dest='xdiv', type=int, default=5, help="xdiv")
    parser.add_argument('--ydiv', action='store', dest='ydiv', type=int, default=5, help="ydiv")

    args = parser.parse_args()

    gcodes = []

    src = Image.open(args.image_file)
    drill = Image.new(src.mode,src.size)
    draw = ImageDraw.Draw(drill)

#    im.show()
    (x,y) = src.size
    for i in range(args.xdiv):
        for j in range(args.ydiv):
            box = get_region_box(src,i,j)
            region = src.crop(box)
            main_color = get_main_color(region)
            draw.rectangle(box, fill=main_color)

    drill.save("drill.png")
