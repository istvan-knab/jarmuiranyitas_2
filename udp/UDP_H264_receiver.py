import cv2
import numpy as np
import socket

def main():
    # Configure the UDP socket
    address = ("::", 5000) # Use IPv6 address and port number
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind(address)

    # Initialize the video codec
    decoder = cv2.VideoCapture()
    decoder.open("appsrc ! video/x-h264, stream-format=byte-stream, width=1920, height=1080, framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! appsink")

    # Display the video stream
    while True:
        # Receive a frame from the UDP socket
        data, _ = sock.recvfrom(65507) # Use the maximum IPv6 UDP packet size

        # Decode the frame using the video codec
        if decoder.isOpened():
            buffer = np.frombuffer(data, dtype=np.uint8)
            frame = buffer.reshape((1080, 1920, 3))
            decoder.write(frame)

            # Display the left camera image
            ret, left_image = decoder.read()
            if ret:
                cv2.imshow("Left Camera Image", left_image)
                if cv2.waitKey(1) == ord("q"):
                    break

    # Clean up
    decoder.release()
    cv2.destroyAllWindows()
    sock.close()

if __name__ == "__main__":
    main()


# import cv2
# import numpy as np
# import zmq
#
# def main():
#     # Configure the ZMQ socket
#     context = zmq.Context()
#     socket = context.socket(zmq.SUB)
#     socket.setsockopt(zmq.IPV6, 1) # Use IPv6
#     socket.bind("tcp://[::]:5000") # Bind to all IPv6 addresses
#     socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
#
#     # Initialize the video codec
#     decoder = cv2.VideoCapture()
#     decoder.open("appsrc ! video/x-h264, stream-format=byte-stream, width=1920, height=1080, framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! appsink")
#
#     # Display the video stream
#     while True:
#         # Receive a frame from the ZMQ socket
#         data = socket.recv()
#
#         # Decode the frame using the video codec
#         if decoder.isOpened():
#             buffer = np.frombuffer(data, dtype=np.uint8)
#             frame = buffer.reshape((1080, 1920, 3))
#             decoder.write(frame)
#
#             # Display the left camera image
#             ret, left_image = decoder.read()
#             if ret:
#                 cv2.imshow("Left Camera Image", left_image)
#                 if cv2.waitKey(1) == ord("q"):
#                     break
#
#     # Clean up
#     decoder.release()
#     cv2.destroyAllWindows()
#     socket.close()
#     context.term()
#
# if __name__ == "__main__":
#     main()
