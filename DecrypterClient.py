import multiprocessing
import socket
import json
import signal

from Deck import Deck
from Solitary import Solitary
from utils import Logger

try:
    from art import text2art
except ImportError:
    Logger.missing_module("art")
    from art import text2art

HOST = "127.0.0.1" 
PORT = 65432

def main():
    title = '''Solitaire
Encryption'''
    title = text2art(title)
    Logger.make_title(title)

    process = multiprocessing.Process(target=Logger.wait_animation)
    process.start()

    def handler(signum, frame):
        process.terminate()

    # terminate process if the user press Ctrl+C
    signal.signal(signal.SIGINT, handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        connection, _ = sock.accept()
        with connection:
            message = ""
            deck = None
            received_count = 0
            while True:
                # receive the encrypted message and the deck
                data = connection.recv(4000)
                # decrypt the message
                if received_count == 0:
                    message = data.decode()
                    received_count += 1
                elif received_count == 1:
                    deck = Deck(Deck.deserialize(json.loads(data.decode())).cards.copy())
                    received_count += 1
                if not data:
                    process.terminate()
                    print("\r" + Logger.Foreground.green + "Data received, connection closed" + Logger.reset, end="\n\n")
                    print(Logger.separator, end="\n\n")
                    break
            
            print("\n" + Logger.Foreground.cyan + 'Received crypted message: ' + message + Logger.reset, end="\n")
            print("\n" + Logger.Foreground.cyan + 'Received deck: ' + Logger.reset, end="\n")
            deck.print_deck()

            solitary = Solitary()
            decrypted_msg = solitary.crypt(message, deck, is_encrypt=False)

            print(Logger.Foreground.green + 'Decrypted message: ' + decrypted_msg + Logger.reset, end="\n\n")

if __name__ == '__main__':
    main()