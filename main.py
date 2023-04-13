import sys

import pygame as pg

from dealer import Dealer
from deck import Deck
from player import Player
from settings import *
from table import Table


class Game:
    """Main game class."""

    def __init__(self, number_of_deck: int = 1):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.deck = Deck(number_of_deck)
        self.dealer = Dealer()
        self.player = Player("jessica", 1200)
        self.table = Table(self.screen, self.deck, self.dealer, self.player)

        self.global_event = pg.USEREVENT + 0

        self.deal_card = False
        self.start_screen = True
        self.show_table = False

    def new_game(self):
        pass

    def update(self):
        pg.display.flip()
        if self.deal_card and self.show_table:
            self.table.deal_card(2)
            self.deal_card = False

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.show_table:
            self.table.draw()
        if self.start_screen:
            self.draw_start_screen()

    def check_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                pass

            elif event.type == pg.MOUSEBUTTONDOWN:
                # get the mouse position
                pos = pg.mouse.get_pos()
                print("Mouse clicked at", pos)
                if self.start_screen:
                    self.start_screen = False
                    self.show_table = True
                if self.show_table:
                    self.deal_card = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def draw_start_screen(self):
        print("RUNNING")
        self.draw_centered_text("START", 24, "black", "red")

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


if __name__ == '__main__':
    game = Game()
    game.run()
