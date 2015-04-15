import cv2
import numpy as np

# create video capture
cap = cv2.VideoCapture(0)

h = 480
w = 640
cap.set(3,w)
cap.set(4,h)

# we draw on a blank background
cv2.namedWindow('background', cv2.CV_WINDOW_AUTOSIZE)

while(1):
    # read the frames
    success,frame = cap.read()
    if success:
        
        # draw a line that shows the slit
        cv2.line(frame,(0,h/2),(w,h/2),255,1)
        cv2.line(frame,(w/2,0),(w/2,h),255,1)
        # crop it
        cropped = frame[h/4:3*h/4, w/4:3*w/4]
        cv2.imshow('background',cropped)

    #if key pressed is 'Esc', exit the loop
    if cv2.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
