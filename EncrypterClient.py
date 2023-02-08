import socket
from Solitary import Solitary
from Deck import Deck
from utils import Logger
import json

try:
    from art import text2art
except ImportError:
    Logger.missing_module("art")
    from art import text2art
    


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def main():

    title = '''Solitaire
Encryption'''
    title = text2art(title)
    Logger.make_title(title)

    encrypt_deck = Deck()
    encrypt_deck.build()
    encrypt_deck.print_deck()
    encrypt_deck.ask_to_shuffle()
    decrypt_deck = Deck(encrypt_deck.cards.copy())

    print("\n" + Logger.separator, end="\n\n")
    print(Logger.Style.underline + Logger.Foreground.yellow + "Input the message do you want to encrypt ⌨️" + Logger.reset, end="\n\n")
    msg = input('')

    solitary = Solitary()

    encrypted_msg = solitary.crypt(msg, encrypt_deck, is_encrypt=True)
    print("\n" + Logger.Foreground.cyan + 'Encrypted message to send: ' + encrypted_msg + Logger.reset, end="\n\n")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        # send the encrypted message to the server and the deck
        sock.sendall(encrypted_msg.encode())
        sock.sendall(json.dumps(decrypt_deck.serialize()).encode())
        sock.close()

if __name__ == '__main__':
    main()