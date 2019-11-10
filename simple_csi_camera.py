#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# check to see if camera is available
# get_ipython().system('ls -ltrh /dev/video*')

import cv2

def gstreamer_pipeline(capture_width=1280,
                       capture_height=720,
                       display_width=1280,
                       display_height=720,
                       framerate=60,
                       flip_method=0):
    """
    returns a GStreamer pipeline for capturing from the CSI camera
    Defaults to 1280x720 @ 60fps
    """
    
    return (
        'nvarguscamerasrc ! '
        'video/x-raw(memory:NVMM), '
        'width=(int)%d, height=(int)%d, '
        'format=(string)NV12, framerate=(fraction)%d/1 ! '
        'nvvidconv flip-method=%d ! '
        'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
        'videoconvert ! '
        'video/x-raw, format=(string)BGR ! appsink'
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        ))

def show_camera():
    print(gstreamer_pipeline(flip_method=0))
    
    # load from CSI Camera(raspi camera v2)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0),
                           cv2.CAP_GSTREAMER)
    
    # check camera normally
    if cap.isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)  # window setting
        
        # when window closed: return -1
        while cv2.getWindowProperty('CSI Camera', 0) >= 0:
            ret_val, img = cap.read()
            cv2.imshow('CSI Camera', img)
            key_code = cv2.waitKey(30) & 0xFF
            
            # Stop program with ESC key
            if key_code == 27:
                break
        
        # Freeing camera object
        cap.release()
        cv2.destroyAllWindows()
    
    else:
        print('Unable to open camera')

if __name__ == '__main__':
    show_camera()
