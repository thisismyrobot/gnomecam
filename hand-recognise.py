#
# Hand recognition
#
# Aims to recognise the side of a hand using the proportions of a bounding
# rectangle around an area of change
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv


def get_img(capture):
    img = cv.QueryFrame(capture)
    return img

def get_diff(old, new):
    """ Returns the difference between two BGR images.
    """
    size = cv.GetSize(old)
    diff = cv.CreateImage(size, 8, 1)
    old_grayscale = cv.CreateImage(size, 8, 1)
    new_grayscale = cv.CreateImage(size, 8, 1)
    cv.CvtColor(old, old_grayscale, cv.CV_BGR2GRAY)
    cv.CvtColor(new, new_grayscale, cv.CV_BGR2GRAY)
    cv.AbsDiff(old_grayscale, new_grayscale, diff)
    cv.Smooth(diff, diff, smoothtype=cv.CV_GAUSSIAN, param1=3, param2=3)
    cv.Threshold(diff, diff, 16, 255, cv.CV_THRESH_BINARY)
    cv.Smooth(diff, diff, smoothtype=cv.CV_GAUSSIAN, param1=13, param2=13)
    cv.Threshold(diff, diff, 200, 255, cv.CV_THRESH_BINARY)
    return diff

if __name__ == "__main__":
    #set up connection to camera
    capture = cv.CaptureFromCAM(0)
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    size = cv.GetSize(get_img(capture))
    old = cv.CreateImage(size, 8, 3)
    new = cv.CreateImage(size, 8, 3)

    while 1:
        new = get_img(capture)
        diff = get_diff(old, new)
        cv.ShowImage('Diff', diff)

        # handle events, alow windows to refresh
        k = cv.WaitKey(5)

        cv.Copy(new, old)
