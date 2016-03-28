import socket
from datastore import Datastore

datastore = Datastore()

HOST = ''
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)
conn, addr = s.accept()
print ('connected by', addr)

while True:
    # conn, addr = s.accept()
    # print ('connected by', addr)

    request_bytes = conn.recv(1024)
    request_str = request_bytes.decode('utf-8')
    # if not data: break
    reply = datastore.process_message(request_str)
    reply_bytes = reply.encode('utf-8') # cut off b

    # conn.sendall(reploy_bytes)
    conn.sendall(reply_bytes)

conn.close()