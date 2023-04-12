import pygame

from game_logic import GameLogic


class Animation(GameLogic):

    def __init__(self, screen: pygame, screen_width: int, screen_height: int,
                 screen_background_color: tuple, deck_back_image_path: str):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_background_color = screen_background_color
        self.deck_back_image_path = deck_back_image_path
        self.card_width = 80
        self.card_height = 100
        self.center_x = (screen_width - 80) // 2
        self.center_y = (screen_height - 100) // 2 - 5

    def start(self):
        self.screen.fill(self.screen_background_color)
        pass

    def text_start(self):

        font = pygame.font.SysFont('Arial', 24)
        text_start = font.render('Game Start!!', True, (255, 255, 255))
        text_start_rect = text_start.get_rect()
        print(text_start_rect)
        self.screen.blit(text_start, (self.center_x, self.center_y))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.center_x, self.center_y, 137, 27), 2)
        pygame.display.flip()
        return text_start_rect

    def deal_card(self, cards, number_of_players: int):
        is_player_receive_card = True
        number_of_cards_to_deal = 2 * number_of_players

        card_position_x = self.center_x - 10

        for index in range(number_of_cards_to_deal):
            if index == number_of_cards_to_deal - 1:
                image = pygame.transform.scale(pygame.image.load(self.deck_back_image_path).convert(),
                                               (self.card_width, self.card_height))
            else:
                image = pygame.transform.scale(pygame.image.load(cards[index].front_image_path).convert(),
                                               (self.card_width, self.card_height))
            card_position_y = self.center_y - 40

            if is_player_receive_card:
                card_position_y += 140
                while card_position_y < 450:
                    self.fill_background_card_path(card_position_x, card_position_y)
                    card_position_y += 2
                    self.screen.blit(image, (card_position_x, card_position_y))
                    pygame.display.flip()

            else:
                card_position_y -= 60
                while card_position_y > 50:
                    self.fill_background_card_path(card_position_x, card_position_y)
                    card_position_y -= 2
                    self.screen.blit(image, (card_position_x, card_position_y))
                    pygame.display.flip()

                card_position_x += 20
            is_player_receive_card = not is_player_receive_card

    def card_shuffle(self):
        self.screen.fill(self.screen_background_color)
        deck_back_image = pygame.transform.scale(pygame.image.load(self.deck_back_image_path).convert(),
                                                 (self.card_width, self.card_height))
        self.screen.blit(deck_back_image, (self.center_x, self.center_y))
        pygame.display.flip()

    def fill_background_card_path(self, card_position_x: int, card_position_y: int):
        clear_rect = pygame.Rect(card_position_x, card_position_y, self.card_width, self.card_height)
        self.screen.fill(self.screen_background_color, clear_rect)
