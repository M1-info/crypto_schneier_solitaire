import random as random
import unidecode as unidecode


def gererate_deck():
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades'] # bridge order
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # with jack, queen and king

    deck = [(rank, suit, id) for suit in suits for rank in ranks for id in range(1, 53)]

    # Add joker
    deck.append((0, 'Black', 53))
    deck.append((0, 'Red', 53))
    return deck


def shuffle_deck(deck):
    return random.shuffle(deck)

def get_keys(msgSize, deck):
    keys = []
    newDeck = list(deck)
    for _ in range(msgSize):
        (key, newDeck) = generate_key(newDeck)
        keys.append(key)
    return keys


def generate_key(deck):
    ## STEP 1
    indexBlackJoker = deck.index((0, 'Black', 53))
    if indexBlackJoker == 53:
        deck.insert(0, deck.pop())
        indexBlackJoker = 0
    deck[indexBlackJoker], deck[indexBlackJoker + 1] = deck[indexBlackJoker + 1], deck[indexBlackJoker]

    # STEP 2
    indexRedJoker = deck.index((0, 'Red', 53))
    if indexRedJoker == 53:
        deck.insert(0, deck.pop())
        indexRedJoker = 0
    deck[indexRedJoker], deck[indexRedJoker + 1] = deck[indexRedJoker + 1], deck[indexRedJoker]
    indexRedJoker += 1
    if indexRedJoker == 53:
        deck.insert(0, deck.pop())
        indexRedJoker = 0
    deck[indexRedJoker], deck[indexRedJoker + 1] = deck[indexRedJoker + 1], deck[indexRedJoker]

    # STEP 3
    indexBlackJoker = deck.index((0, 'Black', 53))
    indexRedJoker = deck.index((0, 'Red', 53))
    firstJoker = min(indexBlackJoker, indexRedJoker)
    secondJoker = max(indexBlackJoker, indexRedJoker)
    firstCards = deck[:firstJoker]
    secondCards = deck[secondJoker+1:]
    newDeck = firstCards + deck[firstJoker:secondJoker+1] + secondCards

    # STEP 4
    numLastCard = newDeck[-1][2]
    nFirstCards = newDeck[:numLastCard]
    newDeck = newDeck[numLastCard:-1] + nFirstCards + [newDeck[-1]]

    # STEP 5
    valueFirstCard = newDeck[0][2]
    valueCard = newDeck[valueFirstCard][2]

    # if card is joker, restart the process
    if valueCard == 53:
        return generate_key(newDeck)

    valueCard = (valueCard % 26)
    char = chr(valueCard + 65)

    return char, newDeck


def encrypt(msg, deck):
    keys = get_keys(len(msg), deck)
    print(keys)
    encryptedMsg = ''
    for (x, y) in zip(msg, keys):
        intMsg = (ord(x) - 65) + 1  # +1 because A = 1, B = 2, etc
        intKey = (ord(y) - 65) + 1
        res = intMsg + intKey if intMsg + intKey <= 26 else intMsg + intKey - 26
        encryptedMsg += chr(res - 1 + 65)
    return encryptedMsg


def decrypt(msg, deck):
    keys = get_keys(len(msg), deck)
    print(keys)
    decryptedMsg = ''
    for (x, y) in zip(msg, keys):
        intMsg = (ord(x) - 65) + 1  # +1 because A = 1, B = 2, etc
        intKey = (ord(y) - 65) + 1
        res = intMsg - intKey if intMsg - intKey > 0 else intMsg - intKey + 26
        print('intMsg: ', intMsg, 'intKey: ', intKey, 'res: ', res)
        decryptedMsg += chr(res - 1 + 65)
    return decryptedMsg


def main():
    # get message from user
    msg = input('Enter message: ')
    msg = ''.join([c for c in msg if c.isalpha()])  # keep only letters
    msg = unidecode.unidecode(msg)  # remove accents
    msg = msg.upper()

    deck = gererate_deck()
    deck = shuffle_deck(deck)
    encryptedMsg = encrypt(msg, deck)
    print('Encrypted message: ', encryptedMsg)
    decryptedMsg = decrypt(encryptedMsg, deck)
    print('Decrypted message: ', decryptedMsg)


# abcdefghijklmnopqrstuvwxyz

if __name__ == '__main__':
    main()
