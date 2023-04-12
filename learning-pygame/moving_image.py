import pygame

from card_elements import Deck


def window():
    # Initialize Pygame
    pygame.init()

    # Create a display surface of size 600x600 pixels and fill it with blue
    surface = pygame.display.set_mode((600, 600))
    surface.fill((66, 123, 184))

    # Create a deck of cards and load the 12th card's image
    deck = Deck(1)
    image = pygame.transform.scale(pygame.image.load(deck.cards[1].front_image_path), (80, 100))

    # Set the initial position of the card to (10, 10)
    image_x = 10
    image_y = 10

    # Blit the card onto the main surface at its initial position
    surface.blit(image, (image_x, image_y))
    pygame.display.flip()

    # Enter the game loop
    while True:
        # Check for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user clicks the close button, quit Pygame and exit the program
                pygame.quit()
                quit()

        # Get the currently pressed keyboard keys
        keys = pygame.key.get_pressed()

        # If the left arrow key is pressed, move the card left by 0.25 pixels
        if keys[pygame.K_LEFT]:
            image_x -= .25
        # If the right arrow key is pressed, move the card right by 0.25 pixels
        if keys[pygame.K_RIGHT]:
            image_x += .25
        # If the up arrow key is pressed, move the card up by 0.25 pixels
        if keys[pygame.K_UP]:
            image_y -= .25
        # If the down arrow key is pressed, move the card down by 0.25 pixels
        if keys[pygame.K_DOWN]:
            image_y += .25

        # Fill the display surface with blue
        surface.fill((66, 123, 184))

        # Blit the card onto the main surface at its updated position
        surface.blit(image, (image_x, image_y))

        # Flip the display buffers to make the changes visible on the screen
        pygame.display.flip()


if __name__ == '__main__':
    window()
