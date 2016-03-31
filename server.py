import socketserver
from datastore import Datastore
import logging
import threading

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    request_queue_size = 100


class ThreadedTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        cur_thread = threading.current_thread()
        for line in self.rfile:
            # self.data = self.rfile.readline()

            # print("{} wrote:".format(self.client_address[0]))
            # print(self.data)

            request_str = line.decode('utf-8')
            logging.info('from port ' + str(self.client_address[1]) + ', request_str ' + request_str)
            reply_str = get_datastore_ref().process_message(request_str)
            logging.info('thread ' + cur_thread.name + ', for port ' + str(self.client_address[1]) + ', reply_str ' + reply_str)
            reply_bytes = reply_str.encode('utf-8')
            self.wfile.write(reply_bytes)


# TODO: replace with datastore access handler
DATASTORE = Datastore()    
def get_datastore_ref():
    return DATASTORE


if __name__ == "__main__":
    # HOST, PORT = "localhost", 8080
    HOST, PORT = "0.0.0.0", 8080
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
    server.serve_forever()
