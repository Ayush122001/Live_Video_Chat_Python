import socket
import cv2
import numpy as np


# Server socket
HOST = '192.168.43.188'
PORT = 50500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

# Connection to client socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.43.46', 50500))

# Accepting Client request
conn, addr = s.accept()


capture = cv2.VideoCapture(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(('192.168.43.46', 50500))



while True:
    ret, frame = capture.read()
    data = cv2.imencode('.jpg', frame)[1].tostring()
    sock.sendall(data)
    data = conn.recv(90456)
    nparr = np.fromstring(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if type(frame) is type(None):
        pass
    else:
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) == 13:
            break
cv2.destroyAllWindows()
