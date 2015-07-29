#!/usr/bin/python
from PIL import Image, ImageTk, ImageDraw
import math
import Tkinter
import pickle
from svgsimple import svgsimple

#how long to make all the sliders
scale_l = 150

#how much to scale the background image to make the lines smoother
resample = 3

#size of background image
size = (resample * 1000, resample * 600)


class Sine():
    #we store parent so we can call update() when a control is changed
    def __init__(self,number,parent):
        #used for storing our settings
        self.number = number
        self.parent = parent

        self.phase = Tkinter.DoubleVar()
        self.freq = Tkinter.DoubleVar()
        self.amp = Tkinter.DoubleVar()
        self.angle = Tkinter.DoubleVar()
        self.damp = Tkinter.DoubleVar()

        self.load()

        self.frame = Tkinter.LabelFrame(text=self.number)

        self.controls = []

        widget = Tkinter.Scale(self.frame,label='a',from_=300, to=0, resolution=1, orient=Tkinter.VERTICAL,variable=self.amp,length=scale_l,showvalue=0)
        widget.bind('<ButtonRelease>',self.parent.update)
        self.controls.append(widget)

        widget = Tkinter.Scale(self.frame,label='f',from_=1, to=0, resolution=0.01, orient=Tkinter.VERTICAL,variable=self.freq,length=scale_l,showvalue=0)
        widget.bind('<ButtonRelease>',self.parent.update)
        self.controls.append(widget)

        widget = Tkinter.Scale(self.frame,label='p',from_=math.pi*2, to=0, resolution=0.005, orient=Tkinter.VERTICAL,variable=self.phase,length=scale_l,showvalue=0)
        widget.bind('<ButtonRelease>',self.parent.update)
        self.controls.append(widget)

        widget = Tkinter.Scale(self.frame,label='A',from_=1, to=0, resolution=0.01, orient=Tkinter.VERTICAL,variable=self.angle,length=scale_l,showvalue=0)
        widget.bind('<ButtonRelease>',self.parent.update)
       
        self.controls.append(widget)

        widget = Tkinter.Scale(self.frame,label='d',from_=0.025, to=0, resolution=0.001, orient=Tkinter.VERTICAL,variable=self.damp,length=scale_l,showvalue=0)
        widget.bind('<ButtonRelease>',self.parent.update)
       
        self.controls.append(widget)


    def get_x(self,t):
        return resample * self.amp.get() * math.sin(t*self.freq.get()+self.phase.get()) * self.angle.get() * math.exp(-t*self.damp.get())

    
    def get_y(self,t):
        return resample * self.amp.get() * math.sin(t*self.freq.get()+self.phase.get()) * (1-self.angle.get()) * math.exp(-t*self.damp.get())

    def get_controls(self):
        for control in self.controls:
            control.pack(side=Tkinter.LEFT)
        return [self.frame] #self.controls
    
    def save(self):
        config = {
            'amp' : self.amp.get(),
            'damp' : self.damp.get(),
            'freq' : self.freq.get(),
            'phase' : self.phase.get(),
            'angle' : self.angle.get(),
            }
        with open('config.%d.pk' % self.number,'w') as fh:
            pickle.dump(config,fh)

    def load(self):
        #try and load saved config
        try:
            with open('config.%d.pk' % self.number) as fh:
                config = pickle.load(fh)
                self.phase.set(config['phase'])
                self.freq.set(config['freq'])
                self.amp.set(config['amp'])
                self.damp.set(config['damp'])
                self.angle.set(config['angle'])
        except:
            #initialise
            self.phase.set(0)
            self.freq.set(0)
            self.amp.set(0)
            self.angle.set(0)

        
class Frame():

    def __init__(self):
        self.tk = Tkinter.Tk()
        #this will be halved as we will antialias the lines
        self.size = size
        #label is where we show the image
        self.bg = Tkinter.Label()
        self.bg.grid(row=1,column=0,columnspan=30,rowspan=30)
        self.image = None
        self.new_background()
        self.update_image()
        
        self.length = Tkinter.IntVar()
        length = Tkinter.Scale(label='points',from_=20000, to=100,resolution=100, orient=Tkinter.VERTICAL,variable=self.length,length=scale_l,showvalue=0)
        length.bind('<ButtonRelease>',self.update)
        length.grid(row=0,column=0)

        self.res = Tkinter.DoubleVar()
        res = Tkinter.Scale(label='res',from_=0.01, to=0.1, resolution=0.001, orient=Tkinter.VERTICAL,variable=self.res,length=scale_l,showvalue=0)
        res.bind('<ButtonRelease>',self.update)
        res.grid(row=0,column=1)

        self.zoom = Tkinter.DoubleVar()
        zoom = Tkinter.Scale(label='zoom',from_=0.1, to=5, resolution=0.1, orient=Tkinter.VERTICAL,variable=self.zoom,length=scale_l,showvalue=0)
        zoom.bind('<ButtonRelease>',self.update)
        zoom.grid(row=0,column=2)
   
        export_frame = Tkinter.LabelFrame(text='Export')

        self.real_width = Tkinter.Scale(export_frame,label='width',from_=10, to=500,orient=Tkinter.HORIZONTAL)
        self.real_width.pack()

        self.min_drill_z = Tkinter.Scale(export_frame,label='min z',from_=1, to=-1,resolution=0.1,orient=Tkinter.HORIZONTAL)
        self.min_drill_z.pack()

        self.max_drill_z = Tkinter.Scale(export_frame,label='max z',from_=-1, to=-5,resolution=0.1,orient=Tkinter.HORIZONTAL)
        self.max_drill_z.pack()

        export = Tkinter.Button(export_frame,text="GCODE",command=self.export)
        export.pack()

        export = Tkinter.Button(export_frame,text="Image",command=self.save_image)
        export.pack()
        export_frame.grid(row=0,column=3)
        
        #load defaults
        self.load()

        #for all our sine waves
        self.sines = []
        self.sines.append(Sine(1,self))
        self.sines.append(Sine(2,self))
        self.sines.append(Sine(3,self))
        self.sines.append(Sine(4,self))

        self.zsine = Sine(5,self)
        #starting column for grid layout
        col = 4
        for sine in self.sines + [self.zsine]:
            for c in sine.get_controls():
                c.grid(row=0,column=col)
                col += 1

        #do one update to start
        self.update()

    def export(self):
        print(self.min_x,self.max_x,self.min_y,self.max_y,self.max_z)
        print(self.real_width.get(),self.min_drill_z.get(),self.max_drill_z.get())
        print(self.x_off,self.y_off)
        print(self.img_width,self.img_height)
        svg = svgsimple()
        svg.create(self.size[0],self.size[1])
        dim_scale = self.real_width.get() / (self.max_x - self.min_x)
        if self.max_z == 0:
            z_scale = 1
        else:
            z_scale = (self.max_drill_z.get() - self.min_drill_z.get()) / self.max_z
        z_min = self.min_drill_z.get()

        print dim_scale
        print z_scale

        gcode = []
        #header
        safez = 3
        feedspeed = 400
        gcode.append( 'G17 G21 G90 G64 P0.003 M3 S3000 M7')
        gcode.append( 'G00 Z%.4f F%d' % (float(safez), feedspeed) )

        #points
        #ensure the first cut we move to the position before lowering tool
        (x,y,z) = self.points[0]
        gcode.append( 'G00 X%.4f Y%.4f' % (x*dim_scale,y*dim_scale))
        svg.start_path(x+self.x_off,y+self.y_off)
        for (x,y,z) in self.points:
            gcode.append('G01 X%.4f Y%.4f Z%.4f' % (x*dim_scale,y*dim_scale,z*z_scale+z_min))
            svg.extend_path(x+self.x_off,y+self.y_off)

        gcode.append('G01 Z%.4f' % float(safez))
        gcode.append( 'G00 X0 Y0')
        gcode.append( 'M5 M9 M2' )
        svg.end_path()
        #export to file
        with open('gcode.ngc','w') as fh:
            for line in gcode:
                fh.write("%s\n" % line)
        svg.save('harmono.svg') 
    def update(self,*args):
        #print("updated")
        self.new_background()
        self.min_x = self.size[0]
        self.max_x = - self.size[0]
        self.min_y = self.size[1]
        self.max_y = - self.size[1]
        self.max_z = 0

        self.points = []

        t = 0
        for step in range(self.length.get()):
            x = 0 #self.size[0]/2
            y = 0 #self.size[1]/2
            t = t + self.res.get()
            for sine in self.sines:
                x += sine.get_x(t)
                y += sine.get_y(t)
                #print(x,y)
                #hack for depth - need a separate type of sine for the z
                z =  (self.zsine.get_x(t) / resample + self.zsine.get_y(t) / resample)
                z += self.zsine.amp.get()  *math.exp(-t*self.zsine.damp.get())

            x = x * self.zoom.get()
            y = y * self.zoom.get()
            self.points.append((x,y,z))

            #store min and max data
            if x > self.max_x:
                self.max_x = x
            if x < self.min_x:
                self.min_x = x
            if y > self.max_y:
                self.max_y = y
            if y < self.min_y:
                self.min_y = y
            if z > self.max_z:
                self.max_z = z

        self.img_width = self.max_x - self.min_x
        self.img_height = self.max_y - self.min_y
        width = self.img_width
        height = self.img_height

        self.x_off = width / 2 + self.size[0] / 2 - self.max_x
        self.y_off = height / 2 + self.size[1] / 2 - self.max_y
        x_off = self.x_off
        y_off = self.y_off


        """
        print self.min_x,self.max_x
        print self.min_x,self.min_y
        print max_x,max_y
        print width, height
        print x_off
        print y_off
        """

        last_point = None
        for point in self.points:
            if last_point:
                self.draw.line([point[0]+x_off,point[1]+y_off,last_point[0]+x_off,last_point[1]+y_off],255,int(point[2]))
            last_point = point
        self.update_image()
        
    def start(self):
        self.tk.mainloop()

    def save(self):
        #our sine waves 
        for sine in self.sines + [self.zsine]:
            sine.save()
        #our controls
        config = {
            'length' : self.length.get(),
            'res' : self.res.get(),
            'zoom' : self.zoom.get(),
            }
        with open('config.pk','w') as fh:
            pickle.dump(config,fh)

    def load(self):
        #try and load saved config
        try:
            with open('config.pk') as fh:
                config = pickle.load(fh)
                self.length.set(config['length'])
                self.res.set(config['res'])
                self.zoom.set(config['zoom'])
        except:
            #initialise
            self.length.set(100)
            self.res.set(0.1)
            self.zoom.set(1)
    
    def new_background(self):
        self.image = Image.new("L", self.size, "black")
        self.draw = ImageDraw.Draw(self.image)

    def update_image(self):
        #halve the image size
        resized_image = self.image.resize((self.size[0]/resample,self.size[1]/resample),resample=Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(resized_image)
        self.bg.configure(image = tk_image)
        self.bg.image = tk_image

    def save_image(self):
        #write it out
        self.image.save("sine.png")


frame = Frame()
frame.start()
frame.save()
