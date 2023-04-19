# import sys
# import zmq
# import pyzed.sl as sl
# import cv2
# import numpy as np
# import socket
#
# def main():
#     # Initialize the ZED camera
#     zed = sl.Camera()
#
#     # Set configuration parameters
#     init_params = sl.InitParameters()
#     init_params.camera_resolution = sl.RESOLUTION.HD1080
#     init_params.camera_fps = 30
#     init_params.depth_mode = sl.DEPTH_MODE.NONE
#
#     # Open the camera
#     err = zed.open(init_params)
#     if err != sl.ERROR_CODE.SUCCESS:
#         print(repr(err))
#         exit(1)
#
#     # Initialize the ZMQ socket
#     # context = zmq.Context()
#     # socket = context.socket(zmq.PUSH)
#     # socket.bind("udp://[fc94:776b:33a5:6f6a:337c:2e85:bc5e:da98]:5000") # Use IPv6 address and port number
#     # socket.bind("udp://[::]:5000") # Use IPv6 address and port number
#     transmit_to = 'Orin'
#     port = 5005
#     udp_ip = socket.getaddrinfo(transmit_to, port, family=socket.AF_INET6, proto=socket.IPPROTO_UDP)[0][4][0]
#     sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
#
#     # Configure the video codec
#     fourcc = cv2.VideoWriter_fourcc(*"H264")
#
#     # Capture images and send them to the UDP socket
#     while True:
#         # Grab a new image from the camera
#         runtime_params = sl.RuntimeParameters()
#         image = sl.Mat()
#         err = zed.grab(runtime_params)
#         if err == sl.ERROR_CODE.SUCCESS:
#             # Retrieve the left image from the ZED camera
#             zed.retrieve_image(image, sl.VIEW.LEFT)
#
#             # Convert the image to a numpy array
#             array = image.get_data()
#
#             # Convert the array to a video frame
#             frame = cv2.imdecode(np.frombuffer(array, np.uint8), cv2.IMREAD_COLOR)
#
#             # Encode the frame using the video codec
#             _, encoded_frame = cv2.imencode(".h264", frame, [cv2.IMWRITE_VIDEO_BITRATE, 1000000])
#
#             # Send the encoded frame to the UDP socket
#             # message = encoded_frame.tobytes()
#             message = frame.tobytes()
#
#             # socket.send(message)
#
#             sock.sendto(message, (udp_ip, port))
#
# if __name__ == "__main__":
#     main()

# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'fc94:2785:f398:aa83:638f:aa15:a4fd:8e17'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)

while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('GOT connection from ',client_addr)
	WIDTH=400
	while(vid.isOpened()):
		_,frame = vid.read()
		frame = imutils.resize(frame,width=WIDTH)
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		cv2.imshow('TRANSMITTING VIDEO',frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			server_socket.close()
			break
		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1

