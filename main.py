import random as random

def gererate_deck():
    deck = []
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] #with jack, queen and king
    id = 0
    for suit in suits:
        for rank in ranks:
            id += 1
            deck.append((rank, suit, id))

    #Add joker
    deck.append((0, 'Black', 53))
    deck.append((0, 'Red', 53))
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


def getKeys(msgSize, deck):
    keys = []
    newDeck = deck
    for i in range(msgSize):
        (key, newDeck) = generateKey(newDeck)
        keys.append(key)
    return keys




def generateKey(deck):
    ## STEP 1
    indexBlackJoker = deck.index((0, 'Black', 53))
    if indexBlackJoker == 53:
        deck.insert(0, deck.pop())
        indexBlackJoker = 0
    deck[indexBlackJoker], deck[indexBlackJoker +1] = deck[indexBlackJoker +1], deck[indexBlackJoker]


    ## STEP 2
    indexRedJoker = deck.index((0, 'Red', 53))
    if indexRedJoker == 53:
        deck.insert(0, deck.pop())
        indexRedJoker = 0
    deck[indexRedJoker], deck[indexRedJoker + 1] = deck[indexRedJoker + 1], deck[indexRedJoker]
    indexRedJoker+=1
    if indexRedJoker == 53:
        deck.insert(0, deck.pop())
        indexRedJoker = 0
    deck[indexRedJoker], deck[indexRedJoker +1] = deck[indexRedJoker +1], deck[indexRedJoker]


    ## STEP 3
    indexBlackJoker = deck.index((0, 'Black', 53))
    indexRedJoker = deck.index((0, 'Red', 53))
    firstJoker = min(indexBlackJoker, indexRedJoker)
    secondJoker = max(indexBlackJoker, indexRedJoker)
    firstCards = deck[:firstJoker]
    secondCards = deck[secondJoker+1:]
    newDeck = firstCards + deck[firstJoker:secondJoker+1] + secondCards


    ## STEP 4
    numLastCard = newDeck[-1][2]
    print(newDeck)
    nFirstCards = newDeck[:numLastCard]
    newDeck = newDeck[numLastCard:-1] + nFirstCards + [newDeck[-1]]


    ## STEP 5
    valueFirstCard = newDeck[0][2]
    card = newDeck[valueFirstCard]

    # if card is joker, restart the process


    return -1, newDeck

def encrypt(msg, key):
    print('encrypt')

def main():
    deck = gererate_deck()
    deck = shuffle_deck(deck)
    #print(deck)
    getKeys(1, deck)
    #print(deck)


if __name__ == '__main__':
    main()
