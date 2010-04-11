#
# Hand recognition
#
# Aims to recognise the side of a hand using the proportions of a bounding
# rectangle around an area of change
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv


HORIZPOS = None

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

def add_rect(display, rect):
    """ Filters discovered rectangles to isolate hand swipes.
    """
    global HORIZPOS

    rect = list(rect)

    #if either dimension is tiny, don't draw
    if rect[2] < 10 or rect[3] < 10:
        return

    #compensate for the actual movement
    if not HORIZPOS:
        HORIZPOS = rect[0] + (float(rect[2])/2)
    else:
        offset = HORIZPOS - (rect[0] + (float(rect[2])/2))
        HORIZPOS = rect[0] + (float(rect[2])/2)
        rect[2] = rect[2] - abs(offset) #decrease the width by the movement
        rect[0] = rect[0] + (-offset/2) #offset by half the movement

    #if width > 1/2 height, don't draw
    if rect[2] * 2 > rect[3]:
        return

    cv.Rectangle(display,
                 (rect[0], rect[1]),
                 (rect[0] + rect[2], rect[1] + rect[3]),
                 (255, 0, 0),
                 3,
                 8,
                 0)

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
        rect = cv.BoundingRect(diff)

        display = cv.CreateImage(size, 8, 3)
        cv.Copy(new, display)

        add_rect(display, rect)
        cv.ShowImage('Diff', display)

        # handle events, alow windows to refresh
        k = cv.WaitKey(5)

        cv.Copy(new, old)
