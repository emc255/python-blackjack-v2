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

    def new_game(self):
        pass

    def update(self):
        pg.display.flip()
        if self.deal_card:
            self.table.deal_card(2)
            self.deal_card = False

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.table.draw()

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
                self.deal_card = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
