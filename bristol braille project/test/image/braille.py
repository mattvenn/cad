#!/usr/bin/env python
import time
import os
import pickle
import cv
import argparse

class Target:

    def __init__(self):
        self.match={}
        self.threshold=150
        try:
          pkl_file = open('match_data.pkl', 'rb')
          self.match = pickle.load(pkl_file)
          self.matching = True; 
        except:
          self.matching = False; 

        self.capture = cv.CaptureFromCAM(0)
        self.window_names = {
          "first" : "first frame",
          "live" : "live",
          "difference" : "difference",
          };
        cv.NamedWindow(self.window_names["first"])
        cv.NamedWindow(self.window_names["difference"])
#        cv.NamedWindow(self.window_names["live"])
        cv.CreateTrackbar("thresh", self.window_names["first"], 0, 255, self.update_threshold)
        cv.SetMouseCallback(self.window_names["difference"], self.diff_mouse)
#        cv.SetMouseCallback(self.window_names["live"], self.live_mouse)
        self.first_frame = cv.LoadImageM("firstframe.png", cv.CV_LOAD_IMAGE_GRAYSCALE)

    def update_threshold(self,threshold):
      self.threshold=threshold
      self.get_first_frame()

    def get_first_frame(self):
        #get first frame
        print "getting first frame"
#        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_EXPOSURE, 5000);
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        #make the grey scale
        first_frame = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, first_frame, cv.CV_RGB2GRAY)
        # Convert the image to black and white.
        cv.Threshold(first_frame, first_frame, self.threshold, 255, cv.CV_THRESH_BINARY)
        cv.Smooth(first_frame, first_frame, cv.CV_GAUSSIAN, 3, 0)
        self.first_frame = first_frame
        #save it
        cv.SaveImage("firstframe.png", t.first_frame)

    def diff_mouse(self,event, x, y, flags,user_data):
     # print cv.Get2D(self.difference, y, x)
      if event == cv.CV_EVENT_LBUTTONDOWN:
        self.match["top_corner"] = (x,y)
      if event == cv.CV_EVENT_LBUTTONUP:
        self.matching = True;
        self.match["dots"] = []
        self.match["bottom_corner"] = (x,y)

        match_width = abs(self.match["top_corner"][0] - self.match["bottom_corner"][0])
        match_height = abs(self.match["top_corner"][1] - self.match["bottom_corner"][1])
        print "matching to %d %d" % (match_width,match_height)

        #we have 3 dots and 2 spaces = 5
        self.match["dot_width"] = int(match_width / 5)
        self.match["dot_height"]= match_height

        first_dot = ( self.match["top_corner"][0], self.match["top_corner"][1] )
        for dot_num in range(3):
          dot = (first_dot[0]+dot_num*2*self.match["dot_width"],first_dot[1])
          self.match["dots"].append(dot)
        print self.match
        output = open('match_data.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.match, output)
        output.close()

    def run(self):
          frame = cv.QueryFrame(self.capture)
          grey_frame = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
          cv.CvtColor(frame, grey_frame, cv.CV_RGB2GRAY)
          cv.Threshold(grey_frame, grey_frame, self.threshold, 255, cv.CV_THRESH_BINARY)
          cv.Smooth(grey_frame, grey_frame, cv.CV_GAUSSIAN, 3, 0)
          
          difference = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
          cv.AbsDiff(grey_frame, self.first_frame, difference)
          self.difference = difference
          if self.matching:
            """
            storage = cv.CreateMemStorage(0)
  #          cv.ConvertScale(contour_frame, contour_frame, 1.0, 0.0)
            #this seems to destroy the difference frame
            contours = cv.FindContours(contour_frame, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            #cv.DrawContours(img=frame, contour=contours, external_color=cv.RGB(255, 0, 0), hole_color=cv.RGB(0, 255, 0), max_level=1 )
            points = []
            while contours:
                bound_rect = cv.BoundingRect(list(contours))
                contours = contours.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                x = bound_rect[0]+bound_rect[2]/2
                y = bound_rect[1]+bound_rect[3]/2
                cv.Circle(frame, (x,y), self.dot_width/4, cv.CV_RGB(0, 255, 255), 2)
                points.append((x,y))
                cv.Rectangle(frame, pt1, pt2, cv.CV_RGB(255,0,0), 1)

            """
            dot_num = 0
            dot_value=[]
            temp = cv.CloneImage(difference)
            for dot in self.match["dots"]:
              src_region = cv.GetSubRect(temp, (dot[0], dot[1], self.match["dot_width"], self.match["dot_height"]) )
              dot_value.append(cv.Avg(src_region)[0])
              cv.Rectangle(difference, dot,(dot[0]+self.match["dot_width"],dot[1]+self.match["dot_height"]), cv.CV_RGB(255, 0, 255), 2, 7)
              #print "dot %d avg %3.1f" % (dot_num, cv.Avg(src_region)[0])
              """
              for point in points:
                if abs(point[0]-dot[0]) < self.match_dist and abs(point[1]-dot[1]) < self.match_dist:
                  print "match on dot %d" % dot_num
              """
              #print "%3.0f" % ( dot_value[dot_num] ) #'1' if dot_value[dot_num] > 100 else '0' ),
              dot_num += 1
            
            for dot in dot_value:
                print "%s" % ( '1' if dot > 100 else '0' ),
            print "" 

          #show images
          cv.ShowImage(self.window_names["first"], self.first_frame)
#          cv.ShowImage(self.window_names["live"], frame)
          cv.ShowImage(self.window_names["difference"], difference)

          c = cv.WaitKey(10)

def advance(steps=0):
  print steps
  os.system("./feed.py --command f%d" % steps )

if __name__=="__main__":
  argparser = argparse.ArgumentParser()

  group = argparser.add_mutually_exclusive_group(required=True)
  group.add_argument('--live',
      action='store_const', const=True, dest='live', default=False,
      help="run the live video")
  group.add_argument('--single',
      action='store_const', const=True, dest='single', default=False,
      help="take one shot")
  group.add_argument('--rotor',
      action='store_const', const=True, dest='rotor', default=False,
      help="take one shot of each side of the rotor")
      
  args = argparser.parse_args()

  t = Target()
  if args.live:
    while(True):
      t.run()

  if args.single:
    t.run()

  if args.rotor:
    pos = []
    for i in range(8):
      pos.append( int(i*12.5) )
  
    last_pos=0
    for p in pos:
      t.run()
      advance(p-last_pos)
      last_pos = p
    
    os.system("./feed.py --command f-%d" % (12.5*8) )
    

