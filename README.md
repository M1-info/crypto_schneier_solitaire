# Schneier's Solitaire Algorithm 🃏

This is a Python implementation of Bruce Schneier's Solitaire algorithm, as described in his book [Applied Cryptography](https://www.schneier.com/books/applied_cryptography/). It is a stream cipher that uses a deck of cards as a key generator.

## Usage 🚀

```bash
$ python3 ./Main.py
```

## Description 📝

The algorithm is based on a deck of 52 cards. The cards are numbered from 1 to 52, with 1 being the Ace of Spades, 2 being the 2 of Spades, and so on. The deck is used to generate a keystream, which is then used to encrypt or decrypt a message.
The same deck is used for both encryption and decryption.

&nbsp;

### 🔥 **The algorithm is as follows**  🔥
<br>

1. **Find the black joker and move it one card down the deck**. <br/> If the black joker is at the bottom of the deck, move it to just above the top card.

2. **Find the red joker and move it two cards down the deck**. <br/> If the red joker is at the bottom of the deck, move it to just above the top card. If the red joker is one card from the bottom of the deck, move it to just above the second card from the top.

3. **Triple cut: Swap the two blocks of cards above and below the two jokers**. <br/> If the top joker is above the bottom joker, the top block is the cards from the top of the deck to the card above the top joker, and the bottom block is the cards from the card below the bottom joker to the bottom of the deck.

4. **Count cut: Take the value of the bottom card and move that many cards from the top of the deck to just below the bottom card.** <br/> Do not include the bottom card in this move.

5. **Output the keystream value: Take the value of the top card. If the value is a joker, go to step 1. Otherwise, get the corresponding letter in the alphabet.** <br /> If the value is greater than 26, just get the remainder when divided by 26 (modulo operation). And find the corresponding letter in the ascii table by adding 65 to the value.
