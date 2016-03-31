import socketserver
from datastore import Datastore

class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    request_queue_size = 100


class TCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.datastore = get_datastore_ref()
        self.data = self.rfile.readline()
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)

        request_str = self.data.decode('ascii')
        print('request_str', request_str)
        reply_str = get_datastore_ref().process_message(request_str)
        print('reply_str', reply_str) 
        reply_bytes = reply_str.encode('ascii')
        self.wfile.write(reply_bytes)


# TODO: replace with datastore access handler
DATASTORE = Datastore()    
def get_datastore_ref():
    return DATASTORE


if __name__ == "__main__":
    # HOST, PORT = "localhost", 8080
    HOST, PORT = "0.0.0.0", 8080
    server = MyTCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()
