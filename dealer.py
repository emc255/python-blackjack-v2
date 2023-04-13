from card import Card
from person import Person


class Dealer(Person):
    def __init__(self):
        Person.__init__(self)

    def add_card(self, card: Card):
        super().add_card(card)

    def reset_hand(self):
        super().reset_hand()

    def calculate_hand_result(self):
        return super().calculate_hand_result()

    def reveal_one_card(self):
        return f"{self.cards[0].rank.value}"
