from dealer import Dealer
from deck import Deck
from player import Player


class Game:
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

    def bet(self, amount):
        self.player.add_bet(amount)

    def deal_card(self):
        players = 2
        if self.deck.check_remaining_cards_count(players * 2):
            for _ in range(players):
                self.player.add_card(self.deck.remove_card())
                self.dealer.add_card(self.deck.remove_card())

    def player_turn(self):
        self.player.add_card(self.deck.remove_card())
        return self.player.calculate_hand_result() > 21

    def dealer_turn(self):
        self.dealer.add_card(self.deck.remove_card())
        return self.dealer.calculate_hand_result() > 21

    def check_dealer_beats_player(self):
        dealer_total = self.dealer.calculate_hand_result()
        return dealer_total >= self.player.calculate_hand_result() or dealer_total >= 17

    def check_winner(self):
        dealer_hand = self.dealer.calculate_hand_result()
        player_hand = self.player.calculate_hand_result()
        if dealer_hand > 21:
            self.player.add_balance(self.player.bet * 2)
        if dealer_hand == player_hand:
            self.player.add_balance(self.player.bet)
        elif dealer_hand < player_hand < 22:
            self.player.add_balance(self.player.bet * 2)

    def reset_hands(self):
        self.cards_played.extend(self.dealer.cards)
        self.cards_played.extend(self.player.cards)
        self.dealer.reset_hand()
        self.player.reset_hand()
        self.player.reset_bet()
