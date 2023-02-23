import socket
import threading

from ui.UISolitary_old import UISolitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000
DISCONNECT_MESSAGE = "!DISCONNECT"

class App:

    server: socket.socket
    thread: threading.Thread
    clients: list[tuple[threading.Thread, socket.socket, tuple]] = []
    interface: UISolitary
    close_app: bool = False

    def __init__(self):
        self.interface = UISolitary()
        self.interface.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setblocking(False)
            self.server.bind(ADDRESS)
            self.thread = threading.Thread(target=self.launch_server)
            self.thread.start()
        except Exception as e:
            pass

        self.interface.init_socket()
        self.interface.window.mainloop()

    def launch_server(self):
        self.server.listen(2)
        while True:
            if self.close_app:
                break
            try:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                self.clients.append((thread, conn, addr))
            except Exception as e:
                continue

    def handle_client(self, conn: socket.socket, addr: tuple):
        while True:
            try:
                if self.close_app:
                    break

                message = conn.recv(MAX_DATA_SIZE).decode(FORMAT)

                if not message:
                    continue

                other_clients = [client for client in self.clients if client[2] != addr]
                for (_, conn, _) in other_clients:
                    print(f"Sending message to {addr} : {message}")
                    conn.send(message.encode(FORMAT))

            except Exception as e:
                continue

    def on_closing(self):
        self.close_app = True
        self.interface.close_app = True

        self.interface.on_closing()

        for (thread, connection, _) in self.clients:
            connection.close()
            thread.join()

        if hasattr(self, "thread"):
            self.thread.join()
            self.server.close()


if __name__ == "__main__":
    App()
