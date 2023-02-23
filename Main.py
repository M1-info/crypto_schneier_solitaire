import socket
import selectors
import threading

from ui.UISolitary import UISolitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000

class App:

    server: socket.socket
    selector: selectors.DefaultSelector
    client: socket.socket
    thread: threading.Thread

    clients: list[tuple[socket.socket, tuple]] = []
    interface: UISolitary

    def __init__(self):
        self.selector = selectors.DefaultSelector()
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDRESS)
            self.server.listen(100)
            self.server.setblocking(False)
            self.selector.register(self.server, selectors.EVENT_READ, self.on_client)
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        except Exception as e:
            pass

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)
        self.client.setblocking(False)
        self.selector.register(self.client, selectors.EVENT_READ, self.on_message)

        self.interface = UISolitary(self.client)
        self.interface.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_client(self, sock: socket.socket, mask: selectors.EVENT_READ):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.clients.append((conn, addr))
        self.selector.register(conn, selectors.EVENT_READ, self.on_message)

    def on_message(self, conn: socket.socket, mask: selectors.EVENT_READ):
        data = conn.recv(MAX_DATA_SIZE)
        if data:
            for client in self.clients:
                if client[0] != conn:
                    client[0].send(data)
        # else:
        #     self.selector.unregister(conn)
        #     conn.close()

    def on_closing(self):
        self.interface.on_closing()

        for client in self.clients:
            client[0].close()

        self.clients.clear()
        self.thread.join()
        self.server.close()
        self.selector.close()
        self.interface.window.destroy()

    def run(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == "__main__":
    App()