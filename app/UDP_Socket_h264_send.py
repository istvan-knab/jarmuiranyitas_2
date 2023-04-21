
import cv2, imutils, socket
import numpy as np
import time
import base64
# import pyzed.sl as sl
#
#
# # Create a ZED camera object
# zed = sl.Camera()
#
# # Set configuration parameters
# init_params = sl.InitParameters()
# init_params.camera_resolution = sl.RESOLUTION.HD1080 # Use HD1080 video mode
# init_params.camera_fps = 30 # Set fps at 30
#
# # Open the camera
# err = zed.open(init_params)
# if (err != sl.ERROR_CODE.SUCCESS) :
#     exit(-1)


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

cap = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if cap.isOpened() == 0:
    exit(-1)
fps,st,frames_to_count,cnt = (0,0,20,0)

# frame = sl.Mat()

while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('GOT connection from ',client_addr)
	WIDTH = 700
	while(cap.isOpened()):
		_,frame = cap.read()
		left_right_image = np.split(frame, 2, axis=1)
		frame = left_right_image[0]
	# if (zed.grab() == sl.ERROR_CODE.SUCCESS):
	# 	# A new image is available if grab() returns SUCCESS
	# 	zed.retrieve_image(frame, sl.VIEW.LEFT)  # Get the left image
	# 	frame = frame.get_data()
		frame = imutils.resize(frame,width=WIDTH)
		encoded, buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
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

