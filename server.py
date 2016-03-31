import socketserver
import logging
from datastore import Datastore

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

DATASTORE = Datastore()
def get_datastore_ref():
    return DATASTORE

class ThreadedTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        datastore = get_datastore_ref()
        for line in self.rfile:
            request_str = line.decode('utf-8')
            logging.info(request_str)
            reply_str = datastore.process_message(request_str)
            logging.info(reply_str)
            reply_bytes = reply_str.encode('utf-8')
            self.wfile.write(reply_bytes)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 100


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
    server.serve_forever()
