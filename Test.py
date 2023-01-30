import unittest

from Deck import Deck
from Solitary import Solitary


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.build()

    def test_deck_init(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 0)

    def test_deck_size(self):
        self.assertEqual(len(self.deck.cards), 54)

    def test_deck_ids(self):
        for i in range(51):
            self.assertEqual(self.deck.cards[i].id, i+1)
        self.assertEqual(self.deck.cards[52].id, 53)
        self.assertEqual(self.deck.cards[53].id, 54)

    def test_joker(self):
        self.assertEqual(self.deck.cards[52].rank, 0)
        self.assertEqual(self.deck.cards[52].suit, 'Red')
        self.assertEqual(self.deck.cards[53].rank, 0)
        self.assertEqual(self.deck.cards[53].suit, 'Black')

    def test_shuffle(self):
        new_deck = Deck(self.deck.cards)
        new_deck.shuffle()
        self.assertNotEqual(new_deck, self.deck)
        self.assertEqual(len(new_deck.cards), 54)

    def test_get_card(self):
        for i in range(54):
            self.assertTrue(1 <= self.deck.get_card_id_by_index(i) <= 54)

    def test_joker_id(self):
        for i in range(10):
            self.deck.shuffle()
            self.assertTrue(1 <= self.deck.get_joker_index('Red') <= 54)
            self.assertTrue(1 <= self.deck.get_joker_index('Black') <= 54)


    #TODO: test our fonction (get_sub_deck, switch_cards, switch_sub_deck, is_last_card, is_joker, move_last_to_front)


class TestSolitary(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.build()
        self.deck.shuffle()
        self.solitary = Solitary()

    def test_generateKey(self):
        for i in range(50):
            key = self.solitary.generate_key(self.deck)
            self.assertEqual(len(key), 1)
            self.assertTrue('A' <= key <= 'Z')

    def test_keys_generation_size(self):
        self.assertEqual(len(self.solitary.keys), 0)
        for i in range(0, 10):
            self.solitary.generate_keys(i, self.deck)
            self.assertEqual(len(self.solitary.keys), i)

    #TODO: test with special cases


    def test_encrypt_decrypt(self):
        message = 'Hello World'
        the_deck = Deck(self.deck.cards)
        encrypted = self.solitary.crypt(message, self.deck, is_encrypt=True)
        self.assertEqual(self.deck.cards, the_deck.cards)
        decrypted = self.solitary.crypt(encrypted, self.deck, is_encrypt=False)
        self.assertEqual(message, decrypted)



    # def test_keys_generation_huge(self):
    #     message = ''
    #     for i in range(1000):
    #         message += 'A'


if __name__ == '__main__':
    unittest.main()
