import random

list_of_suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
list_of_ranks = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
                 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

# CREATING CLASSES FOR CARD, DECK, HAND, PLAYER(CHIPS)


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

    def __int__(self):
        global list_of_ranks
        return list_of_ranks[self.rank]


class Deck:

    def __init__(self):
        self.deck = []
        for suit in list_of_suits:
            for rank in list_of_ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for y in self.deck:
            deck_comp += '\n' + y.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        new_card = self.deck.pop()
        return new_card


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value = self.value - 10
            self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + card.__int__()
        if card.__int__() == 11:
            self.aces = self.aces + 1
        self.adjust_for_ace()


class Player:

    def __init__(self):
        self.name = input('Enter your name: ')
        self.balance = 1000
        print('Hi {}, your balance is {}.'.format(self.name,self.balance))
        self.bet_value = 0

    def win_bet(self):
        self.balance += self.bet_value
        print('Your balance is {}'.format(self.balance))

    def lose_bet(self):
        self.balance -= self.bet_value
        print('Your balance is {}'.format(self.balance))

    def push(self):
        print('PUSH')
        print('Your balance is {}'.format(self.balance))


# GAME FUNCTIONS


def ask_bet(player_chip):
    while True:
        try:
            player_chip.bet_value = int(input('Enter bet value: '))
        except ValueError:
            continue
        else:
            if player_chip.bet_value > player_chip.balance:
                print('You do not have enough balance! Your balance is {}.'.format(player_chip.balance))
                continue
            else:
                return player_chip.bet_value


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    while True:
        try:
            decision = input('\nHit (H) or Stand (S): ').upper()
        except ValueError:
            continue
        else:
            if decision == 'H':
                hit(deck,hand)
                break
            elif decision == 'S':
                if hand.value < 16:
                    print('You cannot stand yet!')
                    continue
                else:
                    return 'S'
            else:
                continue


def show_some(dealer,player):
    print('\n\nDealer\'s hand: ')
    print(dealer.cards[0])
    print('\nYour hand:')
    for z in player.cards:
        print(z)
    print('\nTotal value: {}'.format(player.value))


def show_all(dealer,player):
    print('\n\nSHOWING ALL')
    print('Dealer\'s hand: ')
    for c in dealer.cards:
        print(c)
    print('Total value: {}'.format(dealer.value))
    print('\nYour hand:')
    for c in player.cards:
        print(c)
    print('\nTotal value: {}'.format(player.value))


def play_again(player):
    global Playing
    if player.balance == 0:
        print('You have no more money! Thank you for playing!')
        Playing = False
    else:
        while True:
            try:
                decision = input('Play again? (Y/N): ').upper()
            except TypeError:
                continue
            else:
                if decision == 'N':
                    Playing = False
                    break
                elif decision == 'Y':
                    Playing = True
                    break
                else:
                    continue

# START GAME


new_player = Player()

Playing = True
Turn = True

while Playing:
    ask_bet(new_player)
    new_deck = Deck()
    new_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())

    if player_hand.value == 21 and dealer_hand.value != 21:
        show_all(dealer_hand,player_hand)
        print('BLACKJACK !!!')
        new_player.win_bet()
        play_again(new_player)
    elif player_hand.value == 21 and dealer_hand.value == 21:
        show_all(dealer_hand,player_hand)
        print('BOTH BLACKJACK !!! PUSH !!!')
        new_player.push()
        play_again(new_player)
    elif player_hand.value != 21 and dealer_hand.value == 21:
        show_all(dealer_hand,player_hand)
        print('DEALER BLACKJACK !!!')
        new_player.lose_bet()
        play_again(new_player)
    else:
        show_some(dealer_hand, player_hand)
        while player_hand.value <= 21:
            x = hit_or_stand(new_deck,player_hand)
            show_some(dealer_hand, player_hand)
            player_hand.adjust_for_ace()
            if x == 'S':
                print('\nPLAYER STANDS')
                while dealer_hand.value < 18:
                    dealer_hand.add_card(new_deck.deal())
                show_all(dealer_hand, player_hand)
                if dealer_hand.value > 21:
                    print('DEALER BUST')
                    new_player.win_bet()
                    play_again(new_player)
                    break
                elif dealer_hand.value > player_hand.value:
                    print('DEALER WINS')
                    new_player.lose_bet()
                    play_again(new_player)
                    break
                elif dealer_hand.value < player_hand.value:
                    print('PLAYER WINS')
                    new_player.win_bet()
                    play_again(new_player)
                    break
                elif dealer_hand.value == player_hand.value:
                    new_player.push()
                    play_again(new_player)
                    break
        else:
            print('BUST')
            new_player.lose_bet()
            play_again(new_player)
