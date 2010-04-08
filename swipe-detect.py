#
# Detection of cross-keyboard swipe motion to trigger Alt-Tab and Shift-Alt-Tab
# for window selection.
#
# Requires OpenCV 2.0 and Python 2.6
#

import cv

BACKGROUND = None

def hand(image):
    image_size = cv.GetSize(image)

    # create grayscale version
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    # create storage
    storage = cv.CreateMemStorage(0)

    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)

    # show processed image
    cv.ShowImage('Processed', grayscale)

    # detect objects
    cascade = cv.Load('haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING)

    if faces:
        for i in faces:
            cv.Rectangle(image,
                         (i[0][0], i[0][1]),
                         (i[0][0] + i[0][2], i[0][1] + i[0][3]),
                         (0, 255, 0),
                         3,
                         8,
                         0)


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
    if not BACKGROUND:
        BACKGROUND = cv.QueryFrame(capture)

    while 1:

        live = cv.QueryFrame(capture)

        cv.ShowImage('Live', live)

        # handle events
        k = cv.WaitKey(10)

        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break
