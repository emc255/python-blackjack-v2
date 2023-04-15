import pygame as pg
from pygame import Vector2

from commons import Direction
from dealer import Dealer
from deck import Deck
from player import Player
from settings import *


class Table:
    def __init__(self, screen):
        self.screen = screen
        self.deck_back_image = "resources/images/cards/back.png"
        self.table_image = pg.transform.scale(pg.image.load("resources/images/misc/table.jpg").convert(),
                                              (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, deck: Deck, is_test):
        if is_test:
            self.draw_deal_card_animation(deck.cards, 2)

    def draw(self, deck: Deck, dealer: Dealer, player: Player):
        self.draw_table()
        self.draw_deck_card()
        self.draw_text(player.name, FONT_MEDIUM, RED, 482, 452)
        self.draw_text(f"${player.balance:.2f}", FONT_MEDIUM, LIGHT_GREEN, 482, 474)
        self.draw_text("Bet", FONT_MEDIUM, BLACK, 482, 496)
        self.draw_dealer_hand(dealer)
        self.draw_player_hand(player)

    def draw_table(self):
        self.screen.blit(self.table_image, (0, 0))

    def draw_deck_card(self):
        deck_back_image = pg.transform.scale(pg.image.load(self.deck_back_image).convert(),
                                             (CARD_WIDTH, CARD_HEIGHT))
        self.screen.blit(deck_back_image, (290, 34))

    def draw_dealer_hand(self, dealer: Dealer):
        starting_x = DEALER_CARD_X_POSITION
        if len(dealer.cards) > 0:
            for index, card in enumerate(dealer.cards):
                face_up = card.front_image_path if index == 0 else self.deck_back_image
                image = pg.transform.scale(pg.image.load(face_up).convert(),
                                           (CARD_WIDTH, CARD_HEIGHT))
                self.screen.blit(image, (starting_x, DEALER_CARD_Y_POSITION))
                starting_x += CARD_SPACING_X_POSITION

    def draw_player_hand(self, player: Player):
        starting_x = PLAYER_ONE_X_POSITION
        if len(player.cards) > 0:
            for index, card in enumerate(player.cards):
                image = pg.transform.scale(pg.image.load(card.front_image_path).convert(),
                                           (CARD_WIDTH, CARD_HEIGHT))
                self.screen.blit(image, (starting_x, PLAYER_ONE_Y_POSITION))
                starting_x += CARD_SPACING_X_POSITION

    def draw_text(self, text, font_size, text_color, x, y):
        font = pg.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, (x + 5, y + 5))

    def draw_deal_card_animation(self, cards, number_of_players: int):
        number_of_cards_to_deal = 2 * number_of_players
        player_turn = True

        for index in range(number_of_cards_to_deal):
            direction = Direction.PLAYER_ONE if player_turn else Direction.DEALER

            image_path = self.deck_back_image if index + 1 == number_of_cards_to_deal else cards[index].front_image_path
            image = pg.transform.scale(pg.image.load(image_path).convert(),
                                       (CARD_WIDTH, CARD_HEIGHT))

            first_round_end = index >= number_of_players
            self.deal_card_animation(direction, image, first_round_end)
            player_turn = not player_turn

    def deal_card_animation(self, direction: Direction, image, round_end):
        if direction == Direction.PLAYER_ONE:
            starting_x = 350
            starting_y = 124

            # Define the starting and ending points for the card
            start_pos = Vector2(starting_x, starting_y)
            end_pos = Vector2(480, 356)

            # Calculate the direction and distance between the starting and ending points
            direction = (end_pos - start_pos).normalize()
            card_pos = start_pos

            # Set the speed of the card movement
            speed = .5

            while starting_x < PLAYER_ONE_X_POSITION and starting_y < PLAYER_ONE_Y_POSITION:
                # Create a subsurface of the background image using the defined rect
                background_rect = pg.Rect(starting_x, starting_y, CARD_WIDTH, CARD_HEIGHT)
                background_surface = self.table_image.subsurface(background_rect)
                self.screen.blit(background_surface, (starting_x, starting_y))

                # Diagonal card movement
                card_pos += direction * speed
                starting_x, starting_y = card_pos
                self.screen.blit(image, (starting_x, starting_y))
                pg.display.flip()

        if direction == Direction.DEALER:
            starting_x = 353

            # Create a subsurface of the background image using the defined rect
            background_rect = pg.Rect(starting_x, DEALER_CARD_Y_POSITION, CARD_WIDTH, CARD_HEIGHT)
            background_surface = self.table_image.subsurface(background_rect)

            while starting_x < DEALER_CARD_X_POSITION:
                self.screen.blit(background_surface, (starting_x, DEALER_CARD_Y_POSITION))
                starting_x += .1
                self.screen.blit(image, (starting_x, DEALER_CARD_Y_POSITION))
                pg.display.flip()
