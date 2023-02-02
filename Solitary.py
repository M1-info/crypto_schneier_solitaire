from Deck import CardSuit


class Solitary:

    def __init__(self):
        self.keys = []

    def generate_keys(self, msgSize, deck):
        self.keys = []
        for _ in range(msgSize):
            self.keys.append(self.generate_key(deck))

    def generate_key(self, deck):

        ####################
        ###### STEP 1 ######
        ####################

        index_black_joker = deck.index_of_joker(CardSuit.BLACK_JOKER)
        # if the black joker is the last card in the deck
        # move it to the front
        if deck.is_last_card(index_black_joker):
            deck.move_last_to_front()
            index_black_joker = 0

        # switch the black joker with the card after it
        deck.switch_cards(index_black_joker, index_black_joker + 1)

        ##################
        ##### STEP 2 #####
        ##################

        index_red_joker = deck.index_of_joker(CardSuit.RED_JOKER)
        # if the red joker is the last card in the deck
        # move it to the front
        if deck.is_last_card(index_red_joker):
            deck.move_last_to_front()
            index_red_joker = 0

        # switch the red joker with the card after it
        deck.switch_cards(index_red_joker, index_red_joker + 1)
        index_red_joker += 1

        # if the red joker is the last card in the deck
        # move it to the front
        if deck.is_last_card(index_red_joker):
            deck.move_last_to_front()
            index_red_joker = 0

        # switch the red joker with the card after it
        deck.switch_cards(index_red_joker, index_red_joker + 1)

        ##################
        ##### STEP 3 #####
        ##################

        index_black_joker = deck.index_of_joker(CardSuit.BLACK_JOKER)
        index_red_joker = deck.index_of_joker(CardSuit.RED_JOKER)

        first_joker = min(index_black_joker, index_red_joker)
        second_joker = max(index_black_joker, index_red_joker)

        # switch the two jokers sub-decks (the cards before the first and the cards after the second joker)
        deck.switch_sub_deck(first_joker, second_joker)

        ##################
        ##### STEP 4 #####
        ##################

        num_last_card = deck.get_card_id_by_index(-1)
        n_first_cards = deck.get_sub_deck(0, num_last_card)

        # recreate the deck with the first n cards at the end of the deck (except the last card)
        deck.cards = deck.get_sub_deck(num_last_card) + n_first_cards + [deck.cards[-1]]

        ##################
        ##### STEP 5 #####
        ##################

        # get the value of the first card
        value_first_card = deck.get_card_id_by_index(0)
        value_card = deck.get_card_id_by_index(value_first_card)

        [1, 2, 8, 7]

        # if the value of the first card is a joker, repeat the algorithm
        if deck.is_joker(value_card):
            return self.generate_key(deck)

        value_card = (value_card % 26)
        char = chr(value_card + 65)

        return char

    def crypt(self, message, deck, is_encrypt=True):
        self.generate_keys(len(message), deck)
        crypted_msg = ''
        for (x, y) in zip(message, self.keys):
            int_msg = (ord(x) - 65) + 1  # +1 because A = 1, B = 2, etc
            int_key = (ord(y) - 65) + 1
            if is_encrypt:
                res = int_msg + int_key if int_msg + int_key <= 26 else int_msg + int_key - 26
            else:
                res = int_msg - int_key if int_msg - int_key >= 1 else int_msg - int_key + 26
            crypted_msg += chr(res - 1 + 65)
        return crypted_msg
