import socketserver
from datastore import Datastore
import logging
import threading

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 100


class ThreadedTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        for line in self.rfile:
            request_str = line.decode('utf-8')
            logging.info(request_str)
            reply_str = get_datastore_ref().process_message(request_str)
            logging.info(reply_str)
            reply_bytes = reply_str.encode('utf-8')
            self.wfile.write(reply_bytes)


# TODO: replace with datastore access handler
DATASTORE = Datastore()    
def get_datastore_ref():
    return DATASTORE

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
    server.serve_forever()
