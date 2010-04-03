#
# Python 2.6 and OpenCV 2.0 face detection
#
# Detects face(s) visible to a webcam using a bright green border, trys to center
# image on vertical axis using a servo hooked up to a K1001 (ozitronics.com) RS232
# servo controller.
#
# This code requires OpenCV 2.0 - very very good instructions available here:
# http://subsumption.blogspot.com/2010/02/these-are-instructions-i-used-to.html
#
# This code needs the Haar casade file:
# http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml
#

import sys
import cv
import serial


LAST_DIRECTION = None
SCAN_SPEED = 1

def filterfaces(faces):
    filtered = [face for face in faces if face[0][2] > 50 and face[0][3] > 50]
    if len(filtered) > 0:
        return filtered[0]
    else:
        return None

def detect(image):
    image_size = cv.GetSize(image)
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
    storage = cv.CreateMemStorage(0)
    cv.EqualizeHist(grayscale, grayscale)
    cascade = cv.Load('haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING)
    face = filterfaces(faces)

    if face:
        cv.Rectangle(image,
                     (face[0][0], face[0][1]),
                     (face[0][0] + face[0][2], face[0][1] + face[0][3]),
                     (0, 255, 0),
                     3,
                     8,
                     0)
        center = (face[0][0] + (face[0][2]*0.5), face[0][1] + (face[0][3]*0.5))
        return center

if __name__ == "__main__":
    serialpos = 127
    conn = serial.Serial("/dev/ttyUSB0", 9600, timeout=0)
    conn.write(chr(int(255))+chr(int(0))+chr(int(127)))
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
    capture = cv.CaptureFromCAM(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    while 1:
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
        cv.Flip(frame, None, 1)
        face_center = detect(frame)
        if face_center:
            offset = face_center[0] - (cv.GetSize(frame)[0]/2)
            if abs(offset) > 5:
                serialpos = serialpos + (float(offset)/50)
                if offset > 0:
                    LAST_DIRECTION = SCAN_SPEED
                else:
                    LAST_DIRECTION = -SCAN_SPEED
            else:
                LAST_DIRECTION = None
        else:
            if LAST_DIRECTION:
                serialpos += LAST_DIRECTION
        if serialpos > 200:
            serialpos = 200
            LAST_DIRECTION = -LAST_DIRECTION
        if serialpos < 54:
            serialpos = 54
            LAST_DIRECTION = -LAST_DIRECTION
        conn.write(chr(int(255))+chr(int(0))+chr(int(serialpos)))
