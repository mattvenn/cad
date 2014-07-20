"""
todo
needs better way of converting between px and mm. losing precision by working in px

work out how to lift the drill at the end of the lines
"""
#requires python-imaging-tk
from PIL import Image, ImageTk
from PIL import ImageDraw
import math
import Tkinter
import pickle

tk = Tkinter.Tk()

#the background image
background_img = Image.open("face.jpg").convert('L')
img_width = background_img.size[0]
img_height = background_img.size[1]

def mm2px(mm):
    return int((float(img_width)/real_width.get()) * mm)
def px2mm(px):
    return (float(real_width.get())/img_width) * px

#returns the average value of a region of pixels
def avg_region(image,x,y,width):
    x = int(x)
    y = int(y) 
    box = ( x-width, y-width, x+width, y+width)
    region = image.crop(box)
    colors = region.getcolors(region.size[0]*region.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present


#loads the background photo or a blank image depending on the show image checkbox
def load_photo():
    if show_image.get() == 1:
        image = background_img.copy()
    else:
        image = Image.new("L", background_img.size, "white")
    draw = ImageDraw.Draw(image)
    return image,draw

#loads the given image into the label we're using as a way of displaying the iamge
#http://stackoverflow.com/questions/3482081/tkinter-label-widget-with-image-update 
def update_image(image):
    tk_image = ImageTk.PhotoImage(image)
    label.configure(image = tk_image)
    label.image = tk_image

#the function that draws the lines
def update(*args):
    if lockxy.get():
        c_ystep.config(state='disabled')
#        c_ystep.config(
        ystep.set(xstep.get())
    else:
        c_ystep.config(state='normal')
    points = []
    image, draw = load_photo()

    x_step= mm2px(xstep.get())
    y_step = mm2px(ystep.get())
    last_x = -1
    last_y = -1
    last_r = 0
    tan_angle = math.tan((2*math.pi/360)*drill_angle.get())
    for c in range(0,num_lines.get()):
        for x in range(0,image.size[0],x_step):
            #the main bit
            y = amp.get() * math.sin(x*freq.get()/img_width) + x * pitch.get() + c * y_step + offset.get() + img_height/2 - y_step * num_lines.get() / 2
            avg_color = avg_region(background_img,x,y,x_step/2)
            if invert.get():
                avg_color = 255 - avg_color
            #avg color is from 0 to 255, we have to map this to z depth
            #so now z ranges from 0 to z_range when colour is fully black
            z = z_range.get() * (avg_color / 255.0)
            r = tan_angle * z
            if r > drill_size.get() / 2:
                r = drill_size.get() / 2
            r_pix = mm2px(r)
            last_r_pix = mm2px(last_r)
            if drill.get():
                draw.ellipse((x-r_pix,y-r_pix,x+r_pix,y+r_pix), fill=0)
            else:
                if last_x > 0 and last_y > 0:
                    draw.polygon([(last_x, last_y-last_r_pix), (x, y-r_pix), (x, y+r_pix), (last_x,last_y+last_r_pix)],0)

            #save the points for the gcode
            points.append((px2mm(x),px2mm(y),z))

            #history for the line drawing
            last_x = x
            last_y = y
            last_r = r
        #reset
        last_x = 0
        last_y = 0
    update_image(image)
    return points

def export():
    gcode = []
    #header
    safez = 5
    feedspeed = 10
    gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
    gcode.append( 'G00 X0 Y0 Z%.4f' % float(safez) )

    #points
    points = update()
    if drill.get():
        for (x,y,z) in points:
            #g81 is a simple drill
            gcode.append( 'G81 X%.4f Y%.4f Z%.4f R%.4f' %( x, y, -z, float(safez)))
    else:
        last_x = 0
        for (x,y,z) in points:
            if x < last_x:
                #lift first
                gcode.append('G01 Z%.4f' % float(safez))
                gcode.append('G00 X%.4f Y%.4f' % (x,y))
                gcode.append('G01 Z%.4f' % -z)
            else:
                gcode.append('G01 X%.4f Y%.4f Z%.4f' % (x,y,-z))
            last_x = x

    gcode.append( 'M5 M9 M2' )
    #export to file
    with open('gcode.ngc','w') as fh:
        for line in gcode:
            fh.write("%s\n" % line)

#vars for controls
show_image = Tkinter.IntVar()
invert = Tkinter.IntVar()
freq = Tkinter.DoubleVar()
amp = Tkinter.IntVar()
pitch = Tkinter.DoubleVar()
xstep = Tkinter.DoubleVar()
ystep = Tkinter.DoubleVar()
num_lines = Tkinter.IntVar()
z_range = Tkinter.DoubleVar()
drill = Tkinter.IntVar()
lockxy = Tkinter.IntVar()
offset = Tkinter.IntVar()
drill_size = Tkinter.DoubleVar()
drill_angle = Tkinter.DoubleVar()
real_width = Tkinter.DoubleVar()

#try to load last time's values into the controls
try:
    with open('config.pk') as fh:
        config = pickle.load(fh)
        freq.set(config['freq'])
        amp.set(config['amp'])
        pitch.set(config['pitch'])
        xstep.set(config['xstep'])
        ystep.set(config['ystep'])
        num_lines.set(config['num_lines'])
        z_range.set(config['z_range'])
        invert.set(config['invert'])
        drill.set(config['drill'])
        lockxy.set(config['lockxy'])
        offset.set(config['offset'])
        drill_size.set(config['drill_size'])
        drill_angle.set(config['drill_angle'])
        real_width.set(config['real_width'])
except EOFError :
    print("no config")
except KeyError :
    pass

#create the widgets
#checkboxes
c_show_image = Tkinter.Checkbutton(text='show image', variable=show_image,command=update)
c_invert = Tkinter.Checkbutton(text='invert', variable=invert,command=update)
c_drill = Tkinter.Checkbutton(text='drill', variable=drill,command=update)
c_lockxy = Tkinter.Checkbutton(text='lock x&y', variable=lockxy,command=update)

#scales
c_amp =   Tkinter.Scale(label='amp',from_=0, to=45, orient=Tkinter.VERTICAL,variable=amp,command=update)
c_freq =  Tkinter.Scale(label='freq',from_=0, to=20, resolution=0.1, orient=Tkinter.VERTICAL,variable=freq,command=update)
c_pitch = Tkinter.Scale(label='pitch',from_=-1, to=1, resolution=0.1, orient=Tkinter.VERTICAL,variable=pitch,command=update)
c_xstep = Tkinter.Scale(label='x step',from_=1, to=10, resolution=0.1, orient=Tkinter.VERTICAL,variable=xstep,command=update)
c_ystep = Tkinter.Scale(label='y step', from_=1, to=10, resolution=0.1, orient=Tkinter.VERTICAL,variable=ystep,command=update)
c_num_lines = Tkinter.Scale(label='num lines', from_=1, to=100, resolution=1, orient=Tkinter.VERTICAL,variable=num_lines,command=update)
c_z_range = Tkinter.Scale(label='z range', from_=0, to=5, resolution=0.01, orient=Tkinter.VERTICAL,variable=z_range,command=update)
c_offset = Tkinter.Scale(label='y offset', from_=-img_height, to=img_height, orient=Tkinter.VERTICAL,variable=offset,command=update)

c_drill_size = Tkinter.Scale(label='drill size', from_=0.1, to=5, resolution=0.5, orient=Tkinter.HORIZONTAL,variable=drill_size,command=update)
c_drill_angle = Tkinter.Scale(label='drill angle', from_=20, to=45, resolution=5, orient=Tkinter.HORIZONTAL,variable=drill_angle,command=update)
c_real_width = Tkinter.Scale(label='real width', from_=10, to=500, resolution=1, orient=Tkinter.HORIZONTAL,variable=real_width,command=update)

#label is where we show the image
label = Tkinter.Label()

"""bullshit entry widgets have totally different args
#entry for the drill diameter, and real width,how to label
#c_drill_size = Tkinter.Entry(text="drill size",textvariable=drill_size)
#c_real_width = Tkinter.Entry(text='100')
"""

#buttons
c_export = Tkinter.Button(text="Export",command=export)

#grid em up
c_show_image.grid(row=1,column=0)
c_invert.grid(row=2,column=0)
c_drill.grid(row=3,column=0)
c_lockxy.grid(row=4,column=0)
c_drill_size.grid(row=5,column=0)
c_drill_angle.grid(row=6,column=0)
c_real_width.grid(row=7,column=0)
c_export.grid(row=8,column=0)

c_z_range.grid(row=0,column=0)
c_xstep.grid(row=0,column=1)
c_ystep.grid(row=0,column=2)
c_num_lines.grid(row=0,column=3)
c_offset.grid(row=0,column=4)
c_amp.grid(row=0,column=5)
c_freq.grid(row=0,column=6)
c_pitch.grid(row=0,column=7)

label.grid(row=1,column=1,columnspan=30,rowspan=30)


#start up
image, draw = load_photo()
update_image(image)

#go!
tk.mainloop()

#afterwards, dump config
config = { 
    'show_image' : show_image.get(),
    'freq' : freq.get(),
    'amp' : amp.get(),
    'pitch' : pitch.get(),
    'xstep' : xstep.get(),
    'ystep' : ystep.get(),
    'num_lines' : num_lines.get(),
    'z_range' : z_range.get(),
    'invert' : invert.get(),
    'drill' : drill.get(),
    'lockxy' : lockxy.get(),
    'offset' : offset.get(),
    'drill_size' : drill_size.get(),
    'real_width' : real_width.get(),
    'drill_angle' : drill_angle.get(),
    }

with open('config.pk','w') as fh:
    pickle.dump(config,fh)
