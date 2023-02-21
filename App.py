import socket
import threading

from ui.UISolitary import UISolitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000


class Server:

    server: socket.socket
    already_running: bool = False
    clients = []

    def __init__(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDRESS)
        except socket.error as e:
            self.already_running = True

        if not self.already_running:
            server_thread = threading.Thread(target=self.launch_server)
            server_thread.start()

        client_thread = threading.Thread(target=self.launch_client)
        client_thread.start()
    
    def launch_server(self):
        self.server.listen(2)
        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = self.server.accept()
            print(f"New connection from {addr}")
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            self.clients.append((conn, addr))
            print(f"Active connections: {len(self.clients)}")

    def handle_client(self, conn: socket.socket, addr: tuple):
        print(f"New thread started for {addr}")
        while True:
            # receive the message from the client
            msg = conn.recv(MAX_DATA_SIZE).decode(FORMAT)
            if not msg:
                continue

            # get other clients with different addresses
            other_clients = [client for client in self.clients if client[1] != addr]
            for client in other_clients:
                client[0].send(msg.encode(FORMAT))
            
            break
        
        conn.close()
    
    def launch_client(self):
        UISolitary()

        

if __name__ == "__main__":
    Server()