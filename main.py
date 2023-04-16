import sys

import pygame as pg
from pygame.event import Event

from commons import GameState
from dealer import Dealer
from deck import Deck
from game import Game
from player import Player
from settings import *
from table import Table


class BlackJack:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = None
        self.game = None
        self.table = Table(self.screen)
        self.player_name = ""
        self.player_balance = ""

        self.state = GameState.MAIN_MENU
        self.click_success = False
        self.dealer_show_card = False
        # Rect
        self.main_menu_event_rect = pg.Rect(100, 200, 80, 30)
        self.player_action_event_rect = {
            "bet": pg.Rect(482, 496, 30, 30),
            "hit": pg.Rect(482, 518, 28, 30),
            "stand": pg.Rect(520, 518, 60, 30),
        }

        self.player_name_input_box_rect = pg.Rect(225, 100, 140, 30)
        self.player_balance_input_box_rect = pg.Rect(225, 140, 140, 30)

        self.color_inactive = pg.Color(BLACK)
        self.color_active = pg.Color(YELLOW)

        self.is_player_name_input_box_active = False
        self.player_name_input_box_color = self.color_inactive
        self.player_name_input_box_text_color = self.color_active

        self.is_player_balance_input_box_active = False
        self.player_balance_input_box_color = self.color_inactive
        self.player_balance_input_box_text_color = self.color_active

    def new_game(self):
        self.deck.shuffle()
        self.player = Player(self.player_name, float(self.player_balance))
        self.game = Game(self.deck, self.dealer, self.player)
        self.screen.fill(BACKGROUND_COLOR)

    def update(self):
        pg.display.flip()

        if self.state == GameState.DEAL and self.click_success:
            self.table.deal_card_animation(self.deck.cards, 2)
            self.game.deal_card()
            self.state = GameState.PLAYER_TURN
            self.click_success = False
        elif self.state == GameState.PLAYER_TURN and self.click_success:
            self.table.player_hit_card_animation(self.deck.cards)
            busted = self.game.player_turn()
            if busted:
                self.state = GameState.ROUND_END
            self.click_success = False
        elif self.state == GameState.DEALER_TURN:
            if self.game.check_dealer_beats_player():
                self.state = GameState.ROUND_END
            else:
                self.table.dealer_hit_card_animation(self.deck.cards)
                busted = self.game.dealer_turn()
                if busted:
                    self.state = GameState.ROUND_END
        elif self.state == GameState.ROUND_END and self.click_success:
            self.game.reset_hands()
            self.dealer_show_card = False
            self.state = GameState.DEAL
            pass

    def draw(self):
        if self.state == GameState.MAIN_MENU:
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_start_screen()
        else:
            self.table.draw(self.dealer, self.player, self.dealer_show_card)

    def check_events(self):
        for event in pg.event.get():
            mouse_position = pg.mouse.get_pos()

            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                self.handle_keyboard_input(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_input(mouse_position)

            self.set_cursor_pointer()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def handle_keyboard_input(self, event):
        if self.state == GameState.MAIN_MENU:
            self.get_player_info(event)

    def handle_mouse_input(self, mouse_position):
        if self.state == GameState.MAIN_MENU:
            self.main_menu_screen_collision_check(mouse_position)
            if self.main_menu_event_rect.collidepoint(mouse_position) and len(self.player_name) > 0 and len(
                    self.player_balance) > 0:
                self.new_game()
                self.state = GameState.DEAL

        elif self.state == GameState.DEAL:
            if self.player_action_event_rect["bet"].collidepoint(mouse_position):
                self.click_success = True

        elif self.state == GameState.PLAYER_TURN:
            if self.player_action_event_rect["hit"].collidepoint(mouse_position):
                self.click_success = True
            elif self.player_action_event_rect["stand"].collidepoint(mouse_position):
                self.state = GameState.DEALER_TURN
                self.dealer_show_card = True
        elif self.state == GameState.DEALER_TURN:
            pass

        elif self.state == GameState.ROUND_END:
            if self.player_action_event_rect["bet"].collidepoint(mouse_position):
                self.click_success = True
            pass

    def draw_start_screen(self):
        self.draw_text("Player Name: ", FONT_MEDIUM, BLACK, 100, 100)
        self.draw_input_field(self.player_name_input_box_rect, self.player_name_input_box_color, self.player_name,
                              FONT_MEDIUM, self.player_name_input_box_text_color, 225, 100)

        self.draw_text("Player Balance: ", FONT_MEDIUM, BLACK, 100, 140)
        self.draw_input_field(self.player_balance_input_box_rect, self.player_balance_input_box_color,
                              self.player_balance, FONT_MEDIUM, self.player_balance_input_box_text_color, 225, 140)

        if len(self.player_name) > 0 and len(self.player_balance) > 0:
            self.draw_text("START", FONT_LARGE, YELLOW, 100, 200)

    def draw_text(self, text, font_size, text_color, x, y):
        font = pg.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, (x + 5, y + 5))

    def draw_input_field(self, input_box, input_box_color, text, font_size, text_color, x, y):
        pg.draw.rect(self.screen, input_box_color, input_box)
        font = pg.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, (x + 5, y + 5))

    def get_player_info(self, event: Event):
        if self.is_player_name_input_box_active and event.key == pg.K_RETURN or \
                event.key == pg.K_TAB:
            self.player_name = "" if len(self.player_name) == 0 else self.player_name.replace(" ", "")
        elif self.is_player_name_input_box_active and event.key == pg.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif self.is_player_name_input_box_active and len(self.player_name) < 8:
            self.player_name += event.unicode
        elif self.is_player_balance_input_box_active and event.key == pg.K_BACKSPACE:
            self.player_balance = self.player_balance[:-1]
        elif self.is_player_balance_input_box_active and event.unicode.isdigit() and len(self.player_balance) < 4:
            self.player_balance += event.unicode

    def main_menu_screen_collision_check(self, mouse_position):
        # player name input
        self.is_player_name_input_box_active = self.player_name_input_box_rect.collidepoint(mouse_position)
        self.player_name_input_box_color = self.color_active \
            if self.is_player_name_input_box_active else self.color_inactive
        self.player_name_input_box_text_color = self.color_inactive \
            if self.is_player_name_input_box_active else self.color_active

        # player balance input
        self.is_player_balance_input_box_active = self.player_balance_input_box_rect.collidepoint(mouse_position)
        self.player_balance_input_box_color = self.color_active \
            if self.is_player_balance_input_box_active else self.color_inactive
        self.player_balance_input_box_text_color = self.color_inactive \
            if self.is_player_balance_input_box_active else self.color_active

    def set_cursor_pointer(self):
        cursor_type = pg.SYSTEM_CURSOR_ARROW

        if self.state == GameState.MAIN_MENU and self.main_menu_event_rect.collidepoint(pg.mouse.get_pos()):
            cursor_type = pg.SYSTEM_CURSOR_HAND
        elif self.state == GameState.DEAL and self.player_action_event_rect["bet"].collidepoint(
                pg.mouse.get_pos()):
            cursor_type = pg.SYSTEM_CURSOR_HAND
        elif self.state == GameState.PLAYER_TURN and self.player_action_event_rect["hit"].collidepoint(
                pg.mouse.get_pos()):
            cursor_type = pg.SYSTEM_CURSOR_HAND
        elif self.state == GameState.PLAYER_TURN and self.player_action_event_rect["stand"].collidepoint(
                pg.mouse.get_pos()):
            cursor_type = pg.SYSTEM_CURSOR_HAND
        elif self.state == GameState.DEALER_TURN:
            cursor_type = pg.SYSTEM_CURSOR_HAND
        elif self.state == GameState.ROUND_END and self.player_action_event_rect["bet"].collidepoint(
                pg.mouse.get_pos()):
            cursor_type = pg.SYSTEM_CURSOR_HAND

        pg.mouse.set_cursor(pg.cursors.Cursor(cursor_type))


if __name__ == '__main__':
    blackjack = BlackJack()
    blackjack.run()
