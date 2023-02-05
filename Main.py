from Deck import Deck
from Solitary import Solitary

def main():
    msg = input('Enter message: ')

    encrypt_deck = Deck()
    encrypt_deck.build()
    # encrypt_deck.shuffle()
    decrypt_deck = Deck(encrypt_deck.cards.copy())

    solitary = Solitary()

    encrypted_msg = solitary.crypt(msg, encrypt_deck, is_encrypt=True)
    print('Encrypted message: ', encrypted_msg)

    decrypted_msg = solitary.crypt(encrypted_msg, decrypt_deck, is_encrypt=False)
    print('Decrypted message: ', decrypted_msg)


if __name__ == '__main__':
    main()
