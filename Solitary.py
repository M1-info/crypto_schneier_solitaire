class Solitary:

    def __init__(self):
        self.keys = []

    def generate_keys(self, msgSize, deck):
        self.keys = []
        for _ in range(msgSize):
            self.keys.append(self.generate_key(deck))

    def generate_key(self, deck):
        #STEP 1
        index_black_joker = deck.get_joker_index('Black')
        if deck.is_last_card(index_black_joker):
            deck.move_last_to_front()
            index_black_joker = 0
        deck.switch_cards(index_black_joker, index_black_joker + 1)

        #STEP 2
        index_red_joker = deck.get_joker_index('Red')
        if deck.is_last_card(index_red_joker):
            deck.move_last_to_front()
            index_red_joker = 0
        deck.switch_cards(index_red_joker, index_red_joker + 1)
        index_red_joker += 1
        if deck.is_last_card(index_red_joker):
            deck.move_last_to_front()
            index_red_joker = 0
        deck.switch_cards(index_red_joker, index_red_joker + 1)

        #STEP 3
        index_black_joker = deck.get_joker_index('Black')
        index_red_joker = deck.get_joker_index('Red')
        first_joker = min(index_black_joker, index_red_joker)
        second_joker = max(index_black_joker, index_red_joker)
        deck.switch_sub_deck(first_joker, second_joker)

        #STEP 4
        num_last_card = deck.get_card_id_by_index(-1)
        n_first_cards = deck.get_sub_deck(0, num_last_card)
        deck.cards = deck.get_sub_deck(num_last_card) + n_first_cards + [deck.cards[-1]]

        #STEP 5
        value_first_card = deck.get_card_id_by_index(0)
        value_card = deck.get_card_id_by_index(value_first_card)
        if deck.is_joker(value_card):
            return self.generate_key(deck)

        value_card = (value_card % 26)
        char = chr(value_card + 65)

        return char

    def crypt(self, message, deck, is_encrypt=True):
        self.generate_keys(len(message), deck)
        crypted_msg = ''
        for (x, y) in zip(message, self.keys):
            intMsg = (ord(x) - 65) + 1  # +1 because A = 1, B = 2, etc
            intKey = (ord(y) - 65) + 1
            if is_encrypt:
                res = intMsg + intKey if intMsg + intKey <= 26 else intMsg + intKey - 26
            else:
                res = intMsg - intKey if intMsg - intKey >= 1 else intMsg - intKey + 26
            crypted_msg += chr(res - 1 + 65)
        return crypted_msg
