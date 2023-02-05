import unittest

from Deck import Deck, Card, CardSuit, CardValue
from Solitary import Solitary


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.build()

    # init deck with no cards
    # should be empty
    def test_deck_init(self):
        empty_deck = Deck()
        self.assertEqual(len(empty_deck.cards), 0)

    # build deck with all cards
    # should have 54 cards
    def test_deck_size(self):
        self.assertEqual(len(self.deck.cards), 54)

    # check if all cards are in the deck
    def test_deck_ids(self):
        for i in range(53):
            if i <= 52:
                self.assertEqual(self.deck.cards[i].id, i+1)
            else:
                self.assertEqual(self.deck.cards[i].id, i)

    # check if joker are well initialized
    # should have 2 jokers with rank 0 and color red and black
    def test_jokers(self):
        self.assertEqual(self.deck.cards[53].rank, CardValue.JOKER)
        self.assertEqual(self.deck.cards[53].suit, CardSuit.RED_JOKER)

        self.assertEqual(self.deck.cards[52].rank, CardValue.JOKER)
        self.assertEqual(self.deck.cards[52].suit, CardSuit.BLACK_JOKER)

    # check if shuffle is working
    # should not be the same deck after shuffle
    # should have 54 cards
    def test_shuffle(self):
        new_deck = Deck(self.deck.cards)
        new_deck.shuffle()
        self.assertNotEqual(new_deck, self.deck)
        self.assertEqual(len(new_deck.cards), 54)

    # check if get_joker_index is working
    # should return the index of the joker and it will be contained in the range 1-54
    def test_joker_id(self):
        for i in range(10):
            self.deck.shuffle()
            self.assertTrue(0 <= self.deck.index_of_joker(
                CardSuit.RED_JOKER) < 54)
            self.assertTrue(0 <= self.deck.index_of_joker(
                CardSuit.BLACK_JOKER) < 54)

    def test_is_joker(self):
        # test with full deck (jokers are at the end when the deck is built and not shuffled)
        self.assertTrue(self.deck.is_joker(53))
        self.assertTrue(self.deck.is_joker(52))
        self.assertFalse(self.deck.is_joker(51))

        other_deck = Deck()
        other_deck.cards = [
            Card(CardSuit.SPADES, CardValue.ACE, 1),
            Card(CardSuit.RED_JOKER, CardValue.JOKER, 2),
            Card(CardSuit.BLACK_JOKER, CardValue.JOKER, 3),
            Card(CardSuit.SPADES, CardValue.FOUR, 4)
        ]
        self.assertTrue(other_deck.is_joker(2))
        self.assertTrue(other_deck.is_joker(1))
        self.assertFalse(other_deck.is_joker(3))

    def test_get_sub_deck(self):
        sub_deck = self.deck.get_sub_deck(0, 12)
        self.assertEqual(len(sub_deck), 12)
        self.assertEqual(sub_deck[0].id, 1)
        self.assertEqual(sub_deck[11].id, 12)

        try:
            sub_deck = self.deck.get_sub_deck(0, 55)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertEqual(str(e), "Should have raised an exception")


class TestSolitary(unittest.TestCase):
    def setUp(self):
        self.encrypt_deck = Deck()
        self.encrypt_deck.build()
        self.encrypt_deck.shuffle()
        self.decrypt_deck = Deck(self.encrypt_deck.cards.copy())
        self.solitary = Solitary()

    # test if generate_key is returning a valid key : one letter between A and Z
    def test_generateKey(self):
        for i in range(50):
            key = self.solitary.generate_key(self.encrypt_deck)
            self.assertEqual(len(key), 1)
            self.assertTrue('A' <= key <= 'Z')

    # test if generate_keys is returning a key list of the right size
    def test_keys_generation_size(self):
        self.assertEqual(len(self.solitary.keys), 0)
        for i in range(0, 10):
            self.solitary.generate_keys(i, self.encrypt_deck)
            self.assertEqual(len(self.solitary.keys), i)

    # test if generate_keys is returning same keys when same deck is used
    def test_keys_deterministic_without_shuffle(self):
        deck1 = Deck()
        deck1.build()
        self.solitary.generate_keys(10, deck1)
        keys1 = self.solitary.keys
        deck2 = Deck()
        deck2.build()
        self.solitary.generate_keys(10, deck2)
        keys2 = self.solitary.keys
        self.assertEqual(keys1, keys2)

    # test if encrypt is creating the same keys when same deck is used
    def test_keys_without_shuffle(self):
        deck1 = Deck()
        deck1.build()
        self.solitary.crypt('AAAA', deck1, is_encrypt=True)
        keys1 = self.solitary.keys
        deck2 = Deck()
        deck2.build()
        self.solitary.crypt('AAAA', deck2, is_encrypt=True)
        keys2 = self.solitary.keys
        self.assertEqual(keys1, keys2)
        deck3 = Deck()
        deck3.build()
        self.solitary.crypt('DDDD', deck3, is_encrypt=True)
        keys3 = self.solitary.keys
        self.assertEqual(keys2, keys3)
        deck4 = Deck()
        deck4.build()
        self.solitary.crypt('OUIP', deck4, is_encrypt=True)
        keys4 = self.solitary.keys
        self.assertEqual(keys3, keys4)

    # test if encrypt is creating different keys when different deck is used
    def test_keys_deterministic(self):
        deck1 = Deck()
        deck1.build()
        deck1.shuffle()
        self.solitary.crypt('AAAA', deck1, is_encrypt=True)
        keys1 = self.solitary.keys
        deck2 = Deck()
        deck2.build()
        deck2.shuffle()
        self.solitary.crypt('AAAA', deck2, is_encrypt=True)
        keys2 = self.solitary.keys
        self.assertNotEqual(keys1, keys2)
        deck3 = Deck()
        deck3.build()
        deck3.shuffle()
        self.solitary.crypt('DDDD', deck3, is_encrypt=True)
        keys3 = self.solitary.keys
        self.assertNotEqual(keys2, keys3)
        deck4 = Deck()
        deck4.build()
        deck4.shuffle()
        self.solitary.crypt('OUIP', deck4, is_encrypt=True)
        keys4 = self.solitary.keys
        self.assertNotEqual(keys3, keys4)

    # test if decrypted crypted alphabet is the same as the original alphabet

    def test_encrypt_decrypt_alphabet(self):
        message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        encrypted_msg = self.solitary.crypt(
            message, self.encrypt_deck, is_encrypt=True)
        decrypted_msg = self.solitary.crypt(
            encrypted_msg, self.decrypt_deck, is_encrypt=False)
        self.assertEqual(message, decrypted_msg)

    # test if decrypted message is the same as the original message
    def test_encrypt_decrypt_(self):
        message = 'Hello World !'
        message_wanted = 'HELLOWORLD'
        encrypted_msg = self.solitary.crypt(
            message, self.encrypt_deck, is_encrypt=True)
        decrypted_msg = self.solitary.crypt(
            encrypted_msg, self.decrypt_deck, is_encrypt=False)
        self.assertEqual(message_wanted, decrypted_msg)

    # same test as above but with special characters and space
    def test_encrypt_decrypt_with_special_characters(self):
        message = 'A    BCDEF GHIJKLMN OPQRS TUVWX YZ !@#$%^&*()_+ 1234567890-=[]\{}|;:,./<>?'
        message_wanted = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        encrypted_msg = self.solitary.crypt(
            message, self.encrypt_deck, is_encrypt=True)
        decrypted_msg = self.solitary.crypt(
            encrypted_msg, self.decrypt_deck, is_encrypt=False)
        self.assertEqual(message_wanted, decrypted_msg)

    # same test as above but with accents
    def test_encrypt_decrypt_with_accents(self):
        message = 'éèàçù'
        message_wanted = 'EEACU'
        encrypted_msg = self.solitary.crypt(
            message, self.encrypt_deck, is_encrypt=True)
        decrypted_msg = self.solitary.crypt(
            encrypted_msg, self.decrypt_deck, is_encrypt=False)
        self.assertEqual(message_wanted, decrypted_msg)

    # big test with multiple messages

    def test_cipher(self):
        messages = [
            ('Bonjour', 'BONJOUR'),
            ('Hello world !', 'HELLOWORLD'),
            ('Comment ça va là ? ', 'COMMENTCAVALA'),
            ('étérogènité.', 'ETEROGENITE'),
        ]
        for message, message_wanted in messages:
            encrypted_msg = self.solitary.crypt(
                message, self.encrypt_deck, is_encrypt=True)
            decrypted_msg = self.solitary.crypt(
                encrypted_msg, self.decrypt_deck, is_encrypt=False)
            self.assertEqual(message_wanted, decrypted_msg)


if __name__ == '__main__':
    unittest.main()
