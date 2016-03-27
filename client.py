import socket

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# s.sendall('Hello world!')

legal_messages = [b'INDEX|cloog|gmp,isl,pkg-config\n', b'INDEX|cloog|\n', b'QUERY|cloog|\n', b'REMOVE|cloog|\n', b'REMOVE|cloog|bla\n', b'QUERY|cloog|\n']
print ('request_messages', legal_messages)

reply_messages = []

for message in legal_messages:
    s.sendall(message)
    reply_bytes = s.recv(1024)
    reply_messages.append(str(reply_bytes))

# data_1 = s.recv(1024)

s.close()
# reply_str_1 = str(data_1)
# reply_str_2 = str(data_2)

# print ('received reply_1', reply_str_1)
# print ('received reply_2', reply_str_2)
print ('reply_messages', reply_messages)