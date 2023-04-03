"""
    Open the camera and start streaming images using H264 codec
"""
import sys
import pyzed.sl as sl

def main():

    init = sl.InitParameters()
    # init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_resolution = sl.RESOLUTION.HD1080

    init.depth_mode = sl.DEPTH_MODE.NONE
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()

    stream = sl.StreamingParameters()
    stream.codec = sl.STREAMING_CODEC.H265
    # stream.bitrate = 4000
    stream.bitrate = 11000

    status = cam.enable_streaming(stream)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    print("  Quit : CTRL+C\n")
    while True:
        err = cam.grab(runtime)

    cam.disable_streaming()
    cam.close()

if __name__ == "__main__":
    main()
