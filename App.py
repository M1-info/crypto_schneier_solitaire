import socket
import threading

from ui.UISolitary import UISolitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000


class Server:

    server_socket: socket.socket
    server_thread: threading.Thread
    server_already_running: bool = False
    clients: list[tuple[socket.socket, tuple, threading.Thread]] = []

    def __init__(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setblocking(False)
            self.server_socket.bind(ADDRESS)
        except socket.error as e:
            self.server_already_running = True

        self.ui = UISolitary()

        if not self.server_already_running:
            self.server_thread = threading.Thread(target=self.launch_server)
            self.server_thread.start()

        self.ui.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui.client.connect(ADDRESS)
        self.ui.client.setblocking(False)

        self.thread = threading.Thread(target=self.ui.listen_to_receive_deck)
        self.thread.start()

        self.ui.window.mainloop()

    
    def launch_server(self):
        self.server_socket.listen(2)
        while True:
            if self.ui.want_to_close:
                break
            try :
                conn, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                self.clients.append((conn, addr, thread))
                print(f"Active connections: {len(self.clients)}")
            except Exception as e:
                continue


            

    def handle_client(self, conn: socket.socket, addr: tuple):
        print(f"New thread started for {addr}")
        while True:
            if self.ui.want_to_close:
                break

            # receive the message from the client
            try: 
                msg = conn.recv(MAX_DATA_SIZE).decode(FORMAT)
                print(f"Received message from {addr}: {msg}")
                if not msg:
                    continue

                # get other clients with different addresses
                other_clients = [client for client in self.clients if client[1] != addr]
                print(f"Sending message to {len(other_clients)} clients")
                for (conn, _) in other_clients:
                    conn.send(msg.encode(FORMAT))
            except Exception as e:
                continue
            

    def on_closing(self):
        for (conn, _, thread) in self.clients:
            conn.close()
            thread.join()
        self.server_thread.join()
        self.thread.join()
        self.server_socket.close()

        

if __name__ == "__main__":
    Server()