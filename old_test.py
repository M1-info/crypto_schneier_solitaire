import unittest

from firstImpl import generate_key
from firstImpl import gererate_deck
from firstImpl import shuffle_deck


class TestDeck(unittest.TestCase):
    #too much dependent on the implementation ?

    deck = []
    def setUp(self):
        self.deck = gererate_deck()

    def test_deck_size(self):
        self.assertEqual(len(self.deck), 54)

    def test_deck_ids(self):
        for i in range(51):
            self.assertEqual(self.deck[i][2], i+1)
        self.assertEqual(self.deck[52][2], 53)
        self.assertEqual(self.deck[53][2], 53)

    def test_joker(self):
        self.assertEqual(self.deck[52][0], 0)
        self.assertEqual(self.deck[52][1], 'Black')
        self.assertEqual(self.deck[53][0], 0)
        self.assertEqual(self.deck[53][1], 'Red')

    def test_shuffle(self):
        new_deck = shuffle_deck(self.deck)
        self.assertNotEqual(new_deck, gererate_deck())
        self.assertEqual(len(new_deck), 54)

class TestKeyGenerate(unittest.TestCase):
    deck = []

    def setUp(self):
        self.deck = gererate_deck()
        self.deck = shuffle_deck(self.deck)

    def test_generateKey(self):
        (key, new_deck) = generate_key(self.deck)
        self.assertEqual(len(new_deck), 54)
        self.assertEqual(len(key), 1)
        self.assertTrue('A' <= key <= 'Z')



if __name__ == '__main__':
    unittest.main()

