import socket
import sys

def send_to_server(data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))

HOST, PORT = "localhost", 8080
data = 'INDEX|cloog|\n'

legal_messages = ['INDEX|cloog|gmp,isl,pkg-config\n', 'INDEX|cloog|\n', 'QUERY|cloog|\n', 'REMOVE|cloog|\n', 'REMOVE|cloog|bla\n', 'QUERY|cloog|\n']

for mess in legal_messages:
    send_to_server(mess)
