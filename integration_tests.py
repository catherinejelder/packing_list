import socket
import sys
import unittest

def send_to_server(data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.connect(("192.168.99.100", 8080))
        sock.connect(("172.17.0.2", 8080))
        sock.sendall(bytes(data + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()
    return received

def get_replies(messages):
    replies = []
    for message in messages:
        replies.append(send_to_server(message))  
    return replies 

class TestSeriesOfMessages(unittest.TestCase):
    """
    For now, make sure to start with an empty datastore, and end with an empty datastore.
    """
    def test_index_checks_dependencies(self):
        messages = ['QUERY|gmp|\n', 'QUERY|cloog|\n', 'INDEX|cloog|gmp\n', 'INDEX|gmp|\n', 'INDEX|cloog|gmp\n']
        replies_wanted = ['FAIL\n', 'FAIL\n', 'FAIL\n', 'OK\n', 'OK\n']
        self.assertEqual(replies_wanted, get_replies(messages))
        # flush datastore
        get_replies(['REMOVE|cloog|\n', 'REMOVE|gmp|\n'])

    def test_remove_checks_dependencies(self):
        messages = ['INDEX|isl|\n', 'INDEX|cloog|isl\n', 'REMOVE|isl|\n', 'REMOVE|cloog|\n', 'REMOVE|isl|\n']
        replies_wanted = ['OK\n', 'OK\n', 'FAIL\n', 'OK\n', 'OK\n']
        self.assertEqual(replies_wanted, get_replies(messages))

    def test_query(self):
        messages = ['QUERY|ceylon|\n', 'INDEX|ceylon|\n', 'QUERY|ceylon|\n', 'REMOVE|ceylon|\n', 'QUERY|ceylon|\n']
        replies_wanted = ['FAIL\n', 'OK\n', 'OK\n', 'OK\n', 'FAIL\n']
        self.assertEqual(replies_wanted, get_replies(messages))

if __name__ == '__main__':
    unittest.main()
