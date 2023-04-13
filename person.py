from abc import ABC, abstractmethod

from card import Card
from commons import Rank


class Person(ABC):
    def __init__(self):
        self.cards = []

    @abstractmethod
    def add_card(self, card: Card):
        self.cards.append(card)

    @abstractmethod
    def reset_hand(self):
        self.cards = []

    @abstractmethod
    def calculate_hand_result(self):
        hand_result = 0
        for card in self.cards:
            if card.rank == Rank.ACE:
                one, eleven = card.rank.value
                hand_result += one if hand_result + eleven > 21 else eleven
            elif any(card.rank == r for r in [Rank.JACK, Rank.QUEEN, Rank.KING]):
                hand_result += 10
            else:
                hand_result += card.rank.value

        return hand_result

    # @abc.abstractmethod
    # def my_abstract_method(self):
    #     pass
    # @staticmethod
    # @abc.abstractmethod
    # def my_abstract_static_method():
    #     pass
    #
    # @classmethod
    # @abc.abstractmethod
    # def my_abstract_class_method(cls):
    #     pass
