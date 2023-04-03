"""
    Read a stream and display the left images using OpenCV
"""
import sys
import pyzed.sl as sl
import cv2


def main():

    # Orin IPv6 address:
    # fc94:776b:33a5:6f6a:337c:2e85:bc5e:da98

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE

    init.set_from_stream("127.0.0.1", 30000)

    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()

    key = ''
    print("  Quit : CTRL+C\n")
    while key != 113:
        err = cam.grab(runtime)
        if (err == sl.ERROR_CODE.SUCCESS) :
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            cv2.imshow("ZED", mat.get_data())
            key = cv2.waitKey(1)
        else :
            key = cv2.waitKey(1)

    cam.close()

if __name__ == "__main__":
    main()
