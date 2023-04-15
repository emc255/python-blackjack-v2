from dealer import Dealer
from deck import Deck
from player import Player


class GameV2:
    def __init__(self, deck: Deck, dealer: Dealer, player: Player):
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self.cards_played = []

    def add_played_cards(self, cards):
        if type(cards) == list:
            self.cards_played.extend(cards)
        else:
            self.cards_played.append(cards)

    def start(self):
        self.deck.shuffle()
        play = True
        while play and self.player.balance > 0:
            again = input("Again y/n: ")
            if again == "y":
                self.player_bet()
                self.deal_card()
                self.player_turn()
                self.dealer_turn()
                self.check_winners()
                self.reset_hands()
            elif again == "n":
                play = False

    def player_bet(self):
        print(f"{self.player}")
        betting = True
        while betting:
            try:
                amount = float(input("How much do you wanna bet:"))
            except ValueError:
                print("Sorry")
            else:
                if amount > self.player.balance + 1:
                    print("too much")
                else:
                    self.player.add_bet(amount)
                    betting = False

    def deal_card(self):
        players = 2
        if self.deck.check_remaining_cards_count(players * 2):
            for _ in range(players):
                self.player.add_card(self.deck.remove_card())
                self.dealer.add_card(self.deck.remove_card())

            print(f"dealer has {self.dealer.reveal_one_card()}")

    def player_turn(self):
        decision = True
        while decision and len(self.player.cards) < 5:
            print(f"Your Hand: {self.player.calculate_hand_result()}")
            for a in self.player.cards:
                print(a)
            result = input("Hit/Stay: ")
            if result.lower() == "stay" or result.lower() == "s":
                decision = False
            if result.lower() == "hit" or result.lower() == "h":
                self.player.add_card(self.deck.remove_card())
                if self.player.calculate_hand_result() > 21:
                    print("Player Busted")
                    decision = False

    def dealer_turn(self):
        hand_to_beat = self.player.calculate_hand_result()
        dealer_hand = self.dealer.calculate_hand_result()
        if hand_to_beat <= 21:
            while dealer_hand < hand_to_beat and dealer_hand <= 21:
                print(f"Dealer Hand: {dealer_hand}")
                self.dealer.add_card(self.deck.remove_card())
                dealer_hand = self.dealer.calculate_hand_result()

    def check_winners(self):
        print(f"Dealer Hand: {self.dealer.calculate_hand_result()}")
        if self.dealer.calculate_hand_result() > 21:
            print("Everybody wins")
            self.player.add_balance(self.player.bet)
        elif self.dealer.calculate_hand_result() > self.player.calculate_hand_result():
            print("Dealer Wins")
            self.player.subtract_bet()
        elif self.player.calculate_hand_result() > 21:
            self.player.subtract_bet()
        elif self.player.calculate_hand_result() > self.dealer.calculate_hand_result():
            self.player.add_balance(self.player.bet)
            print("Player Wins")
        else:
            print("Draw")

    def reset_hands(self):
        self.cards_played.extend(self.dealer.cards)
        self.cards_played.extend(self.player.cards)
        self.dealer.reset_hand()
        self.player.reset_hand()
        self.player.reset_bet()
