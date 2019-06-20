#! /usr/bin/env python
"""
blackjack.py by jason@neisskids.org (Jason W. Neiss)

last updated 2019-06-17

based on the rules posted by Bicycle Playing Cards
at https://bicyclecards.com/how-to-play/blackjack/

TODO: splits, double-down, insurance.

There are probably bugs.
"""

import random
import sys
import time

from os import system, name

# check for python 3
if sys.version_info[0] < 3:
    print(f"Python 3 required; your version is {sys.version_info[0]}.{sys.version_info[1]}. Sorry.")
    sys.exit(1)

#######################
# constant declarations
#######################
suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
play = True


#######################
# class declarations
#######################

class Bankroll:
    def __init__(self, amount=100):
        self.amount = amount

    def __str__(self):
        return f"You have ${self.amount} in your bankroll."

    def add_to_roll(self, amount):
        self.amount += amount

    def del_from_roll(self, amount):
        self.amount -= amount
        if self.amount <= 0:
            print("You are BROKE. The bouncers will show you out now.")
            exit(1)


#######################
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


#######################
class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_descr = ''
        for carddesc in self.deck:
            deck_descr += '\n ' + carddesc.__str__()
        return "Cards in deck: " + deck_descr

    def shuffle_deck(self):
        # a real shuffle is more than just one, so we'll shuffle a random number of times
        x = random.randint(2, 50)
        y = 0

        while y < x:
            random.shuffle(self.deck)
            y += 1

        # split off the last 8 - 22 cards in the shoe to prevent card-counting
        cut = random.randint(8, 23)
        self.deck = self.deck[:-cut]
        # bug: what happens when we run out of cards?)

    def deal_card(self):
        single_card = self.deck.pop()
        return single_card


#######################
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.bust = False
        self.natural = False

    def add_card(self, card1):
        self.cards.append(card1)
        self.value += values[card1.rank]
        if card1.rank == 'Ace':
            self.aces += 1

    def ace_adjust(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def go_bust(self):
        self.bust = True

    def set_natural(self):
        self.natural = True


#######################
# function declarations
#######################

def clear_scr():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def dealershow():
    clear_scr()
    time.sleep(1)
    print(f"{playername} is showing {', '.join(str(x) for x in player.cards)}.\nYour Score: {player.value}")
    print(f"Dealer is showing {', '.join(str(x) for x in dealer.cards)}.\nDealer Score: {dealer.value}\n")


def getcard():
    return gamedeck.deal_card()


def place_bet():
    bet = int(input(f"{playername}, you have ${bankroll.amount}. You minimum bet is $2. Place your bet: "))
    if bet <= bankroll.amount:
        pass
    else:
        # if some smartass tries to bet more than they have
        while bet > bankroll.amount:
            bet = int(input(f"You have ${bankroll.amount}. Your minimum bet is $2, and your maximum"
                            f" is ${bankroll.amount}. Place your bet: "))

    return bet


def showcards():
    clear_scr()
    time.sleep(1)
    print(f"Dealer is showing {dealer.cards[0]}, and one face down.")
    print(f"{playername} is showing {', '.join(str(x) for x in player.cards)}.\n Your Score: {player.value}\n")


#######################
# program body
#######################

# clear the screen and generate beginning game state
clear_scr()
playername = input(f"Welcome to Blackjack. Please enter your name: ")
bankroll = Bankroll()
gamedeck = Deck()

# shuffle the deck
gamedeck.shuffle_deck()

while play:
    # place yer bets
    playerbet = place_bet()
    player = Hand()
    dealer = Hand()

    # initial deal: player gets one card face up, then dealer gets one face up.
    # Player gets another face up, and the dealer gets one face down.
    deal = 0
    while deal < 2:
        player.add_card(getcard())
        dealer.add_card(getcard())
        deal += 1

    showcards()

    # check for natural
    if player.value == 21:
        player.set_natural()

    if dealer.value == 21:
        dealer.set_natural()

    # seed the choice variable with something that shouldn't be there
    playerchoice = 'q'

    # player's turn
    while playerchoice != 's' and player.natural is False:
        playerchoice = input(f"{playername}, (s)tay or (h)it?")
        if playerchoice.lower() == 's':
            print(f"{playername} stays.\n")
            time.sleep(1)
            continue
        elif playerchoice.lower() == 'h':
            print(f"{playername} hits:\n")
            newcard = getcard()
            print(f"{newcard}")
            time.sleep(1)
            player.add_card(newcard)
            if player.value > 21:
                player.ace_adjust()
                if player.value > 21:
                    player.go_bust()
                    print(f"{playername} went BUST with {player.value}.")
                break
            showcards()
        else:
            continue

    # turn over the dealer's cards
    print(f"Dealer's hole card is turned up.")
    dealershow()

    # dealer's turn
    while dealer.value < 22 and dealer.natural is False:
        if dealer.value == 21:
            time.sleep(1)
            print("Dealer has 21; dealer stays.")
            break
        if dealer.value <= 16:
            time.sleep(1)
            print(f"Dealer has {dealer.value}; dealer hits:")
            newcard = getcard()
            time.sleep(1)
            print(f"{newcard}")
            dealer.add_card(newcard)
            dealershow()
            if dealer.value > 21:
                dealer.ace_adjust()
                if dealer.value > 21:
                    dealer.go_bust()
                    time.sleep(1)
                    print(f"Dealer went BUST with {dealer.value}.")
        elif dealer.value >= 17:
            break

    # cash out
    time.sleep(1)
    if player.natural is True and dealer.natural is True:
        print(f"Standoff, no payout.")
    elif player.natural is True and dealer.natural is False:
        playerbet = playerbet * 1.5
        print(f"{playername} has blackjack and wins ${playerbet}!")
        bankroll.add_to_roll(playerbet)
    elif player.natural is False and dealer.natural is True:
        print(f"Dealer has blackjack, and {playername} loses ${playerbet}!")
        bankroll.del_from_roll(playerbet)
    elif player.bust:
        bankroll.del_from_roll(playerbet)
        print(f"{playername} went bust and loses ${playerbet}.")
    elif dealer.bust:
        bankroll.add_to_roll(playerbet)
        print(f"Dealer went bust, and {playername} WINS ${playerbet}!\nPlayer bankroll: ${bankroll.amount}")
    elif player.value == dealer.value:  # also true for naturals
        print(f"Standoff, no payout.")
    elif dealer.value == 21 and player.value != 21:
        bankroll.del_from_roll(playerbet)
        print(f"Dealer WINS; player loses ${playerbet}.\nPlayer bankroll: ${bankroll.amount}")
    elif dealer.value < player.value:
        bankroll.add_to_roll(playerbet)
        print(f"{playername} WINS ${playerbet}!\nPlayer bankroll: ${bankroll.amount}")
    elif player.value < dealer.value:
        bankroll.del_from_roll(playerbet)
        print(f"Dealer WINS; player loses ${playerbet}.\nPlayer bankroll: ${bankroll.amount}")
    else:
        print(f"This probably shouldn't happen and means there's a bug. Dealer value: {dealer.value},"
              f" Player value: {player.value}, Bankroll amount: ${bankroll.amount}")

    answer = input("Play again (y/n)?")
    if answer.lower() == 'y':
        play = True
    else:
        play = False
