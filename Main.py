import socket
import selectors
import threading
import json

from ui.UISolitary import UISolitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000

class App:

    server: socket.socket
    selector: selectors.DefaultSelector
    client: socket.socket
    thread: threading.Thread

    clients: list[tuple[socket.socket, tuple]] = []
    interface: UISolitary

    is_someone_building_deck: bool = False
    is_deck_built: bool = False

    close_app: bool = False

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

        self.interface = UISolitary()
        self.interface.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.interface.window.mainloop()

    def on_client(self, sock: socket.socket, mask: selectors.EVENT_READ):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.clients.append((conn, addr))
        self.selector.register(conn, selectors.EVENT_READ, self.on_message)

        if not self.is_deck_built :
            conn.send(json.dumps({"type": "ack" ,"is_someone_building_deck": self.is_someone_building_deck}).encode())
        else:
            deck = self.interface.ui_deck.deck.serialize()
            conn.send(json.dumps({"type": "deck", "deck": deck}).encode())
    
    def on_message(self, conn: socket.socket, mask: selectors.EVENT_READ):
        data = conn.recv(MAX_DATA_SIZE)
        if data:
            if "building_deck" in data.decode() :
                self.is_someone_building_deck = True
            elif "deck" in data.decode() :
                self.is_deck_built = True
            clients = list(filter(lambda client: client[0] != conn, self.clients))
            for client in clients:
                client[0].send(data)

    def on_closing(self):
        self.interface.close_app = True
        self.close_app = True

        self.interface.on_close()

        for client in self.clients:
            client[0].close()
        self.clients.clear()

        if hasattr(self, "thread"):
            self.thread.join()
            self.selector.unregister(self.server)
            self.server.close()
            self.selector.close()

        self.interface.window.destroy()

    def run(self):
        while not self.close_app:
            events = self.selector.select(timeout=0)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == "__main__":
    App()