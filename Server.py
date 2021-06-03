import socket
import cv2
import numpy as np


# Server socket
HOST = '192.168.43.46'
PORT = 50500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind(('192.168.43.46',50500))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

# Client Socket
capture = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.43.188', 50500))

model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    data = conn.recv(90456)
    nparr = np.fromstring(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if type(frame) is type(None):
        pass
    else:
        face = model.detectMultiScale(frame)
        if len(face) !=0 :
            x1 = face[0][0]
            y1 = face[0][1]
            x2 = x1 + face[0][2]
            y2 = y1 + face[0][3]
            frame = cv2.rectangle(frame,(x1,y1),(x2,y2),[0,0,255],4)
        cv2.imshow('Linux', frame)
        if cv2.waitKey(10) == 13:
            break
    ret, frame = capture.read()
    data = cv2.imencode('.jpg', frame)[1].tostring()
    sock.sendall(data)

cv2.destroyAllWindows()

                             
