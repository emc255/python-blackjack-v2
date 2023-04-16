from card import Card
from person import Person


class Player(Person):
    def __init__(self, name: str, balance: float):
        super().__init__()
        self.name = name
        self.balance = balance
        self.bet = 0

    def add_card(self, card: Card):
        super().add_card(card)

    def reset_hand(self):
        super().reset_hand()

    def calculate_hand_result(self):
        return super().calculate_hand_result()

    def add_balance(self, amount: float):
        self.balance += amount

    def add_bet(self, amount: float):
        self.bet += amount
        self.balance -= amount

    def reset_bet(self):
        self.bet = 0

    def __str__(self):
        return f"{self.name} has a balance of ${self.balance:.2f}"
