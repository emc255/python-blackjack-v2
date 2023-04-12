import pygame

from card_elements import Deck


def card_testing(cards, window):
    going_down = True
    i = 0

    center_x = (window.get_width() - 80) // 2
    center_y = (window.get_height() - 100) // 2
    image_x = center_x - 10

    back_image = pygame.transform.scale(pygame.image.load("../resource/images/cards/back.png").convert(), (80, 100))
    window.blit(back_image, (center_x, center_y))

    for _ in range(4):
        image = pygame.transform.scale(pygame.image.load(cards[i].front_image_path).convert(),
                                       (cards[i].width, cards[i].height))
        image_y = center_y - 40
        if going_down:
            image_y += 100
            while image_y < 450:
                image_y += .1
                window.blit(back_image, (center_x, center_y))
                window.blit(image, (image_x, image_y))
                pygame.draw.rect(window, (66, 123, 184), (image_x, image_y, 80, 100), 1)
                window.blit(back_image, (center_x, center_y))
                pygame.display.flip()
        else:
            image_y -= 100
            while image_y > 50:
                image_y -= .1
                window.blit(back_image, (center_x, center_y))
                window.blit(image, (image_x, image_y))
                pygame.draw.rect(window, (66, 123, 184), (image_x, image_y, 80, 110), 1)
                window.blit(back_image, (center_x, center_y))
                pygame.display.flip()
            image_x += 20
        going_down = not going_down
        i += 1


def main():
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    window.fill((66, 123, 184))

    deck = Deck(1)
    card_testing(deck.cards, window)

    pygame.display.flip()
    while True:
        # Check for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user clicks the close button, quit Pygame and exit the program
                pygame.quit()
                quit()


if __name__ == '__main__':
    main()
