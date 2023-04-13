import pygame as pg

from commons import Direction
from dealer import Dealer
from deck import Deck
from player import Player
from settings import *


class Table:
    def __init__(self, screen, deck: Deck, dealer: Dealer, player: Player):
        self.screen = screen
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self.deck_back_image = "resources/images/cards/back.png"

    def draw(self):
        self.draw_deck_card()
        self.draw_dealer_hand()
        self.draw_player_hand()

    def draw_centered_text(self, text, font_size, text_color, rect_color):
        font = pg.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.screen.get_rect().center
        rect_width = text_rect.width + 10
        rect_height = text_rect.height + 10
        rect_left = (self.screen.get_width() - rect_width) // 2
        rect_top = (self.screen.get_height() - rect_height) // 2
        rect = pg.Rect(rect_left, rect_top, rect_width, rect_height)
        pg.draw.rect(self.screen, rect_color, rect, 2)
        self.screen.blit(text_surface, text_rect)
        pg.display.flip()

    def draw_dealer_hand(self):
        starting_x = DEALER_CARD_X_POSITION
        if len(self.dealer.cards) > 0:
            for index, card in enumerate(self.dealer.cards):
                face_up = card.front_image_path if index == 0 else self.deck_back_image
                image = pg.transform.scale(pg.image.load(face_up).convert(),
                                           (CARD_WIDTH, CARD_HEIGHT))
                self.screen.blit(image, (starting_x, DEALER_CARD_Y_POSITION))
                starting_x += CARD_SPACING_X_POSITION

    def draw_player_hand(self):
        starting_x = PLAYER_ONE_X_POSITION
        if len(self.player.cards) > 0:
            for index, card in enumerate(self.player.cards):
                image = pg.transform.scale(pg.image.load(card.front_image_path).convert(),
                                           (CARD_WIDTH, CARD_HEIGHT))
                self.screen.blit(image, (starting_x, PLAYER_ONE_Y_POSITION))
                starting_x += CARD_SPACING_X_POSITION

    def draw_deck_card(self):
        center_x = (SCREEN_WIDTH - CARD_WIDTH) // 2
        center_y = (SCREEN_HEIGHT - CARD_HEIGHT) // 2
        deck_back_image = pg.transform.scale(pg.image.load(self.deck_back_image).convert(),
                                             (CARD_WIDTH, CARD_HEIGHT))
        self.screen.blit(deck_back_image, (center_x, center_y))

    def deal_card(self, number_of_players: int):
        number_of_cards_to_deal = 2 * number_of_players
        player_turn = True

        for index in range(number_of_cards_to_deal):
            direction = Direction.DOWN if player_turn else Direction.UP
            card = self.deck.remove_card()

            if player_turn:
                self.player.add_card(card)

            if not player_turn:
                self.dealer.add_card(card)

            image_path = self.deck_back_image if index + 1 == number_of_cards_to_deal else card.front_image_path
            image = pg.transform.scale(pg.image.load(image_path).convert(),
                                       (CARD_WIDTH, CARD_HEIGHT))

            first_round_end = index >= number_of_players
            self.deal_card_animation(direction, image, first_round_end)
            player_turn = not player_turn

    def deal_card_animation(self, direction: Direction, image, round_end):
        if direction == Direction.UP:
            starting_x = DEALER_CARD_X_POSITION + CARD_SPACING_X_POSITION if round_end else DEALER_CARD_X_POSITION
            starting_y = 150
            while starting_y > DEALER_CARD_Y_POSITION:
                # clearing the path which the card takes
                clear_rect = pg.Rect(starting_x, starting_y, CARD_WIDTH, CARD_HEIGHT)
                self.screen.fill(BACKGROUND_COLOR, clear_rect)
                starting_y -= 1
                self.screen.blit(image, (starting_x, starting_y))
                pg.display.flip()

        if direction == Direction.DOWN:
            starting_x = PLAYER_ONE_X_POSITION + CARD_SPACING_X_POSITION if round_end else PLAYER_ONE_X_POSITION
            starting_y = 350
            while starting_y < PLAYER_ONE_Y_POSITION:
                # clearing the path which the card takes
                clear_rect = pg.Rect(starting_x, starting_y, CARD_WIDTH, CARD_HEIGHT)
                self.screen.fill(BACKGROUND_COLOR, clear_rect)
                starting_y += 1
                self.screen.blit(image, (starting_x, starting_y))
                pg.display.flip()
