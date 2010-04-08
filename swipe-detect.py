#
# Detection of cross-keyboard swipe motion to trigger Alt-Tab and Shift-Alt-Tab
# for window selection.
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv


BACKGROUND_GS = None

if __name__ == "__main__":

    # create windows
    cv.NamedWindow('Live', cv.CV_WINDOW_AUTOSIZE)

    #set up connection to camera
    capture = cv.CaptureFromCAM(0)
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    #get background of keyboard
    if not BACKGROUND_GS:
        discard = cv.QueryFrame(capture)
        import time
        time.sleep(5)
        BACKGROUND = cv.QueryFrame(capture)
        image_size = cv.GetSize(BACKGROUND)
        BACKGROUND_GS = cv.CreateImage(image_size, 8, 1)
        cv.Flip(BACKGROUND, None, 1)
        cv.CvtColor(BACKGROUND, BACKGROUND_GS, cv.CV_BGR2GRAY)
        cv.EqualizeHist(BACKGROUND_GS, BACKGROUND_GS)

    while 1:

        live = cv.QueryFrame(capture)
        image_size = cv.GetSize(live)
        cv.Flip(live, None, 1)
        live_gs = cv.CreateImage(image_size, 8, 1)
        cv.CvtColor(live, live_gs, cv.CV_BGR2GRAY)
        cv.EqualizeHist(live_gs, live_gs)

        diff = cv.CreateImage(image_size, 8, 1)

        cv.AbsDiff(live_gs, BACKGROUND_GS, diff)

        cv.Threshold(diff, diff, 150, 255, cv.CV_THRESH_BINARY)

        cv.ShowImage('Live', diff)

        # handle events
        k = cv.WaitKey(5)
        
        import pdb; pdb.set_trace()
