import sys
import zmq
import pyzed.sl as sl
import cv2
import numpy as np

def main():
    # Initialize the ZED camera
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Failed to open the camera")
        return

    # Initialize the ZMQ socket
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("udp://[fc94:776b:33a5:6f6a:337c:2e85:bc5e:da98]:5000") # Use IPv6 address and port number

    # Configure the video codec
    fourcc = cv2.VideoWriter_fourcc(*"H264")

    # Capture images and send them to the UDP socket
    while True:
        # Grab a new image from the camera
        runtime_params = sl.RuntimeParameters()
        image = sl.Mat()
        err = zed.grab(runtime_params)
        if err == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left image from the ZED camera
            zed.retrieve_image(image, sl.VIEW.LEFT)

            # Convert the image to a numpy array
            array = image.get_data()

            # Convert the array to a video frame
            frame = cv2.imdecode(np.frombuffer(array, np.uint8), cv2.IMREAD_COLOR)

            # Encode the frame using the video codec
            _, encoded_frame = cv2.imencode(".h264", frame, [cv2.IMWRITE_VIDEO_BITRATE, 1000000])

            # Send the encoded frame to the UDP socket
            message = encoded_frame.tobytes()
            socket.send(message)

if __name__ == "__main__":
    main()
