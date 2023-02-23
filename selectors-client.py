import socket
import selectors

# make client socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

# make selector

sel = selectors.DefaultSelector()

# register client socket

sel.register(client, selectors.EVENT_READ)

# send data

client.send(b'hello')

# wait for data

while True:
    events = sel.select()
    for key, mask in events:
        print(key.fileobj.recv(1024))

