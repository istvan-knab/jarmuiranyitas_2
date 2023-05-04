# import cv2
# import numpy as np
# import socket
#
# def main():
#     # Configure the UDP socket
#     address = ("::", 5000) # Use IPv6 address and port number
#     sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
#     sock.bind(address)
#
#     # Initialize the video codec
#     decoder = cv2.VideoCapture()
#     decoder.open("appsrc ! video/x-h264, stream-format=byte-stream, width=1920, height=1080, framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! appsink")
#
#     # Display the video stream
#     while True:
#         # Receive a frame from the UDP socket
#         data, _ = sock.recvfrom(65507) # Use the maximum IPv6 UDP packet size
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
#     sock.close()
#
# if __name__ == "__main__":
#     main()
#
#
# # import cv2
# # import numpy as np
# # import zmq
# #
# # def main():
# #     # Configure the ZMQ socket
# #     context = zmq.Context()
# #     socket = context.socket(zmq.SUB)
# #     socket.setsockopt(zmq.IPV6, 1) # Use IPv6
# #     socket.bind("tcp://[::]:5000") # Bind to all IPv6 addresses
# #     socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
# #
# #     # Initialize the video codec
# #     decoder = cv2.VideoCapture()
# #     decoder.open("appsrc ! video/x-h264, stream-format=byte-stream, width=1920, height=1080, framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! appsink")
# #
# #     # Display the video stream
# #     while True:
# #         # Receive a frame from the ZMQ socket
# #         data = socket.recv()
# #
# #         # Decode the frame using the video codec
# #         if decoder.isOpened():
# #             buffer = np.frombuffer(data, dtype=np.uint8)
# #             frame = buffer.reshape((1080, 1920, 3))
# #             decoder.write(frame)
# #
# #             # Display the left camera image
# #             ret, left_image = decoder.read()
# #             if ret:
# #                 cv2.imshow("Left Camera Image", left_image)
# #                 if cv2.waitKey(1) == ord("q"):
# #                     break
# #
# #     # Clean up
# #     decoder.release()
# #     cv2.destroyAllWindows()
# #     socket.close()
# #     context.term()
# #
# # if __name__ == "__main__":
# #     main()

# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'fc94:776b:33a5:6f6a:337c:2e85:bc5e:da98'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999
message = b'Hello'

client_socket.sendto(message,(host_ip,port))
fps,st,frames_to_count,cnt = (0, 0, 20, 0)
while True:
	packet,_ = client_socket.recvfrom(BUFF_SIZE)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1

