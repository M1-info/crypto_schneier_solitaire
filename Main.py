from Deck import Deck, Card
import unidecode as unidecode
from Solitary import Solitary

def main():
    # get message from user
    msg = input('Enter message: ')
    msg = ''.join([c for c in msg if c.isalpha()])  # keep only letters
    msg = unidecode.unidecode(msg)  # remove accents
    msg = msg.upper()

    encrypt_deck = Deck()
    encrypt_deck.build()
    encrypt_deck.shuffle()
    decrypt_deck = Deck(encrypt_deck.cards)

    solitary = Solitary()
    encrypted_msg = solitary.crypt(msg, encrypt_deck, is_encrypt=True)
    decrypted_msg = solitary.crypt(encrypted_msg, decrypt_deck, is_encrypt=False)

    print('Decrypted message: ', decrypted_msg)

if __name__ == '__main__':
    main()