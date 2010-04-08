#
# Detection of cross-keyboard swipe motion to trigger Alt-Tab and Shift-Alt-Tab
# for window selection.
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv


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
    cv.Split(hsv, hue, sat, val, None);
    return val

def get_diff(image1, image2):
    """ Returns the diff. """
    size = cv.GetSize(image)
    diff = cv.CreateImage(size, 8, 1)
    cv.AbsDiff(image1, image2, diff)
    cv.Threshold(diff, diff, 100, 255, cv.CV_THRESH_BINARY)
    cv.Smooth(diff, diff, smoothtype=cv.CV_GAUSSIAN, param1=13, param2=13)
    cv.Threshold(diff, diff, 100, 255, cv.CV_THRESH_BINARY)
    return diff

if __name__ == "__main__":

    #set up connection to camera
    capture = cv.CaptureFromCAM(0)
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    bg = get_hands(get_img(capture))

    while 1:
        image = get_img(capture)
        hands = get_hands(image)
        valdiff = get_diff(bg, hands)

        cv.ShowImage('Live', image)
        cv.ShowImage('Value', hands)
        cv.ShowImage('Value Diff', valdiff)

        # handle events
        k = cv.WaitKey(5)
