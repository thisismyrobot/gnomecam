#
# Detection of cross-keyboard swipe motion to trigger Alt-Tab and Shift-Alt-Tab
# for window selection.
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv
import time


def get_img(capture):
    img = cv.QueryFrame(capture)
    return img

def get_hands(image):
    """ Returns the hand as white on black. Uses value in HSV to determine
        hands."""
    size = cv.GetSize(image)
    hsv = cv.CreateImage(size, 8, 3)
    hue = cv.CreateImage(size, 8, 1)
    sat = cv.CreateImage(size, 8, 1)
    val = cv.CreateImage(size, 8, 1)
    hands = cv.CreateImage(size, 8, 1)
    cv.CvtColor(image, hsv, cv.CV_BGR2HSV)
    cv.Split(hsv, hue, sat, val, None)

    cv.ShowImage('Live', image)
    cv.ShowImage('Hue', hue)
    cv.ShowImage('Saturation', sat)

    cv.Threshold(hue, hue, 10, 255, cv.CV_THRESH_TOZERO) #set to 0 if <= 10, otherwise leave as is
    cv.Threshold(hue, hue, 244, 255, cv.CV_THRESH_TOZERO_INV) #set to 0 if > 244, otherwise leave as is
    cv.Threshold(hue, hue, 0, 255, cv.CV_THRESH_BINARY_INV) #set to 255 if = 0, otherwise 0
    cv.Threshold(sat, sat, 64, 255, cv.CV_THRESH_TOZERO) #set to 0 if <= 64, otherwise leave as is
    cv.EqualizeHist(sat, sat)

    cv.Threshold(sat, sat, 64, 255, cv.CV_THRESH_BINARY) #set to 0 if <= 64, otherwise 255

    cv.ShowImage('Saturation threshold', sat)
    cv.ShowImage('Hue threshold', hue)

    cv.Mul(hue, sat, hands)

    #smooth + threshold to filter noise
#    cv.Smooth(hands, hands, smoothtype=cv.CV_GAUSSIAN, param1=13, param2=13)
#    cv.Threshold(hands, hands, 200, 255, cv.CV_THRESH_BINARY)

    cv.ShowImage('Hands', hands)

    return hands

if __name__ == "__main__":
    cv.NamedWindow('Live', cv.CV_WINDOW_AUTOSIZE)

    #set up connection to camera
    capture = cv.CaptureFromCAM(0)
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    while 1:
        image = get_img(capture)
        hands = get_hands(image)

        # handle events
        k = cv.WaitKey(5)
