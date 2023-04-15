import random

from card import Card
from commons import Suit, Rank


class Deck:
   
    def __init__(self, number_of_deck: int = 1):
        self.cards = [Card(suit, rank) for _ in range(number_of_deck) for suit in Suit for rank in Rank]
        self.played_cards = []

    def add_cards(self, cards):
        self.cards.extend(cards) if isinstance(cards, list) else self.cards.append(cards)

    def add_played_cards(self, cards):
        self.played_cards.extend(cards) if isinstance(cards, list) else self.played_cards.append(cards)

    def remove_card(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)

    def reset_cards(self):
        self.cards.extend(self.played_cards)
        self.played_cards = []

    def check_remaining_cards_count(self, players: int):
        return len(self.cards) >= (players * 2)

    def get_cards_count(self):
        return len(self.cards)

    # def get_played_cards_count(self):
    #     return len(self.played_cards)
