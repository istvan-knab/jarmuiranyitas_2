"""
    Read a stream and display the left images using OpenCV
"""
import sys
import pyzed.sl as sl
import cv2


def main():

    orin = "fc94:776b:33a5:6f6a:337c:2e85:bc5e:da98"
    orin_sztaki = "10.1.0.167"
    balint_pc = "fc94:f3ae:8c82:1e80:c8ff:9154:6bc0:7252"
    kry_pc = "fc94:2785:f398:aa83:638f:aa15:a4fd:8e17"

    local = "127.0.0.1"

    init = sl.InitParameters()
    # init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_resolution = sl.RESOLUTION.HD1080

    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE

    init.set_from_stream(orin_sztaki, 30000)

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
