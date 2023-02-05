from unidecode import unidecode

from Deck import CardSuit, Deck

class Solitary:

    def __init__(self):
        self.keys = []

    def generate_keys(self, message_size: int, deck: Deck) -> None:
        self.keys = []
        for _ in range(message_size):
            self.keys.append(self.generate_key(deck))

    def generate_key(self, deck: Deck) -> str:

        ####################
        ###### STEP 1 ######
        ####################

        index_black_joker = deck.index_of_joker(CardSuit.BLACK_JOKER)

        # if the black joker is the last card in the deck
        # move it to second place
        if index_black_joker == len(deck.cards) - 1:
            black_joker = deck.cards.pop()
            sub_deck = deck.cards[1:]
            deck.cards = [deck.cards[0]] + [black_joker] + sub_deck
        else:
            # switch the black joker with the card after it
            deck.switch_cards(index_black_joker, index_black_joker + 1)

        ##################
        ##### STEP 2 #####
        ##################

        index_red_joker = deck.index_of_joker(CardSuit.RED_JOKER)

        # if the red joker is the second to last card in the deck
        # move it to the second place
        if index_red_joker == len(deck.cards) - 2:
            # red_joker = pop the second to last card
            red_joker = deck.cards.pop(index_red_joker)
            sub_deck = deck.get_sub_deck(1, len(deck.cards))
            deck.cards = [deck.cards[0]] + [red_joker] + sub_deck
        # if the red joker is the last card in the deck
        # move it to the third place
        elif index_red_joker == len(deck.cards) - 1:
            red_joker = deck.cards.pop()
            sub_deck = deck.get_sub_deck(2, len(deck.cards))
            deck.cards = [deck.cards[0]] + \
                [deck.cards[1]] + [red_joker] + sub_deck
        else:
            # go back two times
            deck.switch_cards(index_red_joker, index_red_joker + 1)
            index_red_joker += 1
            deck.switch_cards(index_red_joker, index_red_joker + 1)

        # ##################
        # ##### STEP 3 #####
        # ##################

        index_black_joker = deck.index_of_joker(CardSuit.BLACK_JOKER)
        index_red_joker = deck.index_of_joker(CardSuit.RED_JOKER)

        first_joker = min(index_black_joker, index_red_joker)
        second_joker = max(index_black_joker, index_red_joker)

        # switch the two jokers sub-decks (the cards before the first and the cards after the second joker)
        deck.switch_sub_deck(first_joker, second_joker)

        # ##################
        # ##### STEP 4 #####
        # ##################

        num_last_card = deck.get_card_id_by_index(-1)
        n_first_cards = deck.get_sub_deck(0, num_last_card)

        # recreate the deck with the first n cards at the end of the deck (except the last card)
        deck.cards = deck.get_sub_deck(
            num_last_card, -1) + n_first_cards + [deck.cards[-1]]

        # ##################
        # ##### STEP 5 #####
        # ##################

        # get the value of the first card
        value_first_card = deck.get_card_id_by_index(0)

        if deck.is_joker(value_first_card):
            return self.generate_key(deck)

        value_card = deck.get_card_id_by_index(value_first_card)
        value_card = (value_card % 26)
        char = chr(value_card + 65)

        return char
    
    def parse_message(self, message: str) -> str:
        parsed_message = message

        # get spaces and upper case positions
        spaces = [i for i, c in enumerate(parsed_message) if c == ' ']
        is_upper = [c.isupper() for c in parsed_message]

        parsed_message = ''.join([c for c in parsed_message if c.isalpha()])
        parsed_message = unidecode(parsed_message)
        parsed_message = parsed_message.upper()
        return [parsed_message, spaces, is_upper]

    def crypt(self, message: str, deck: Deck, is_encrypt: bool = True) -> str:
        [message, spaces, uppers] = self.parse_message(message)

        self.generate_keys(len(message), deck)
        
        crypted_msg = ''
        for (x, y) in zip(message, self.keys):
            int_msg = (ord(x) - 65) + 1  # +1 because A start from 1 and not 0
            int_key = (ord(y) - 65)
            if is_encrypt:
                res = int_msg + int_key if int_msg + int_key <= 26 else int_msg + int_key - 26
            else:
                res = int_msg - int_key if int_msg - int_key >= 1 else int_msg - int_key + 26
            crypted_msg += chr(res - 1 + 65)

        for i in spaces:
            crypted_msg = crypted_msg[:i] + ' ' + crypted_msg[i:]

        crypted_msg = ''.join([c.upper() if uppers[i] else c.lower() for i, c in enumerate(crypted_msg)])
        return crypted_msg
