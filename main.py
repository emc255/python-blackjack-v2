import sys

import pygame as pg

from dealer import Dealer
from deck import Deck
from game import GameV2
from player import Player
from settings import *
from table import TableV2


class MainWindow:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = None
        self.game = None
        self.table = TableV2(self.screen)
        self.player_name = ""
        self.player_balance = ""

        self.is_start_screen_active = True
        self.is_table_screen_active = False
        self.deal_card = False

        # Rect
        self.start_event_rect = pg.Rect(100, 200, 80, 30)
        self.player_action_event_rect = {
            "bet": pg.Rect(482, 496, 60, 30),
            "hit": pg.Rect(320, 395, 60, 30),
            "stand": pg.Rect(320, 395, 60, 30),
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
        self.game = GameV2(self.deck, self.dealer, self.player)
        self.is_start_screen_active = False
        self.is_table_screen_active = True
        self.screen.fill(BACKGROUND_COLOR)
        print(self.player)

    def update(self):
        pg.display.flip()
        if self.deal_card:
            self.game.reset_hands()
            self.table.update(self.deck, self.deal_card)
            self.game.deal_card()
            self.deal_card = False

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.is_start_screen_active:
            self.draw_start_screen()

        if self.is_table_screen_active:
            self.table.draw(self.deck, self.dealer, self.player)

    def check_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.get_player_info(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self.start_screen_collision_check(event)
                if self.start_game(event):
                    self.new_game()
                elif self.player_action_event_rect["bet"].collidepoint(event.pos) and self.is_table_screen_active:
                    # trigger the custom event
                    self.deal_card = True
                print(event.pos)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

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

    def get_player_info(self, event):
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

    def start_screen_collision_check(self, event):
        # player name input
        self.is_player_name_input_box_active = self.player_name_input_box_rect.collidepoint(event.pos)
        self.player_name_input_box_color = self.color_active \
            if self.is_player_name_input_box_active else self.color_inactive
        self.player_name_input_box_text_color = self.color_inactive \
            if self.is_player_name_input_box_active else self.color_active

        # player balance input
        self.is_player_balance_input_box_active = self.player_balance_input_box_rect.collidepoint(event.pos)
        self.player_balance_input_box_color = self.color_active \
            if self.is_player_balance_input_box_active else self.color_inactive
        self.player_balance_input_box_text_color = self.color_inactive \
            if self.is_player_balance_input_box_active else self.color_active

    def start_game(self, event):
        return self.start_event_rect.collidepoint(event.pos) and self.is_start_screen_active \
            and len(self.player_name) > 0 and len(self.player_balance) > 0


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.run()
