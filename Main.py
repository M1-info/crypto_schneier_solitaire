from Deck import Deck
from Solitary import Solitary
from utils import Logger

def main():

    Logger.make_title()

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
    print("\n" + Logger.Foreground.cyan + 'Encrypted message: ' + encrypted_msg + Logger.reset, end="\n")

    decrypted_msg = solitary.crypt(encrypted_msg, decrypt_deck, is_encrypt=False)
    print(Logger.Foreground.green + 'Decrypted message: ' + decrypted_msg + Logger.reset, end="\n\n")


if __name__ == '__main__':
    main()
