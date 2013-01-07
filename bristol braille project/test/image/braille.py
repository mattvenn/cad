#!/usr/bin/env python
import time
import cv

class Target:

    def __init__(self):
        self.dots = []
        self.windowed = False; #let user specify window to care about
        self.threshold=150
        self.matching = False; #wait till user specifies area
        self.capture = cv.CaptureFromCAM(0)
        self.window_names = {
          "first" : "first frame",
          "live" : "live",
          "difference" : "difference",
          };
        cv.NamedWindow(self.window_names["first"])
        cv.NamedWindow(self.window_names["difference"])
        cv.NamedWindow(self.window_names["live"])
        cv.CreateTrackbar("thresh", self.window_names["first"], 0, 255, self.update_threshold)
        cv.SetMouseCallback(self.window_names["difference"], self.diff_mouse)
        cv.SetMouseCallback(self.window_names["live"], self.live_mouse)

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

    def diff_mouse(self,event, x, y, flags,user_data):
#      print "got mouse: %d %d" % (x,y)
      if event == cv.CV_EVENT_LBUTTONDOWN:
        self.top_corner = (x,y)
      if event == cv.CV_EVENT_LBUTTONUP:
        self.bottom_corner = (x,y)
        self.windowed = True;
        self.new_width = abs(self.top_corner[0] - self.bottom_corner[0])
        self.new_height = abs(self.top_corner[1] - self.bottom_corner[1])
        print "cropping to %d %d" % (self.new_width,self.new_height)
      
    def live_mouse(self,event, x, y, flags,user_data):
#      print "got mouse: %d %d" % (x,y)
      if event == cv.CV_EVENT_LBUTTONDOWN:
        self.match_top_corner = (x,y)
      if event == cv.CV_EVENT_LBUTTONUP:
        self.dots = []
        self.match_bottom_corner = (x,y)
        self.matching = True;
        self.match_width = abs(self.match_top_corner[0] - self.match_bottom_corner[0])
        self.match_height = abs(self.match_top_corner[1] - self.match_bottom_corner[1])
        print "matching to %d %d" % (self.match_width,self.match_height)

        #we have 3 dots and 2 spaces = 5
        dot_width = self.match_width / 5
        dot_height = self.match_height
        self.dot_width = dot_width
        self.match_dist = self.dot_width / 2
        print "dots are %d x %d" % (dot_width, dot_height)
        first_dot = ( self.match_top_corner[0] + dot_width / 2, self.match_top_corner[1] + dot_height / 2 )
        for dot_num in range(3):
          dot = (first_dot[0]+dot_num*2*dot_width,first_dot[1])
          self.dots.append(dot)
        print self.dots

    def run(self):
        while(True):
          frame = cv.QueryFrame(self.capture)
          grey_frame = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
          cv.CvtColor(frame, grey_frame, cv.CV_RGB2GRAY)
          cv.Threshold(grey_frame, grey_frame, self.threshold, 255, cv.CV_THRESH_BINARY)
          cv.Smooth(grey_frame, grey_frame, cv.CV_GAUSSIAN, 3, 0)
          
          difference = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
          cv.AbsDiff(grey_frame, self.first_frame, difference)

          #crop the image
          if self.windowed:
            #create new 
            contour_frame = cv.CreateImage( (self.new_width, self.new_height), cv.IPL_DEPTH_8U, 1)
            src_region = cv.GetSubRect(difference, (self.top_corner[0], self.top_corner[1], self.new_width, self.new_height) )
            cv.Copy(src_region, contour_frame)

            src_region = cv.GetSubRect(frame, (self.top_corner[0], self.top_corner[1], self.new_width, self.new_height) )
            cropped_frame = cv.CreateImage( (self.new_width, self.new_height), cv.IPL_DEPTH_8U, 3)
            cv.Copy(src_region, cropped_frame)
            frame=cropped_frame

          else:
            contour_frame = cv.CloneImage(difference)

          if self.matching:
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

            dot_num = 0
            for dot in self.dots:
              cv.Circle(frame, dot, self.dot_width/2, cv.CV_RGB(255, 0, 255), 2)
              for point in points:
                if abs(point[0]-dot[0]) < self.match_dist and abs(point[1]-dot[1]) < self.match_dist:
                  print "match on dot %d" % dot_num
              dot_num += 1
            

          #show images
          cv.ShowImage(self.window_names["first"], self.first_frame)
          cv.ShowImage(self.window_names["live"], frame)
          cv.ShowImage(self.window_names["difference"], difference)

          c = cv.WaitKey(17) % 100
          if c == 27:
              break
          if c == 89:
              self.get_first_frame()

if __name__=="__main__":
    t = Target()
    t.get_first_frame()
    t.run()

