from card_elements import Deck


def moving_window():
    import pygame

    # Initialize Pygame
    pygame.init()

    # Set up the window
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Image")
    deck = Deck(1)

    # Load the image
    image = pygame.image.load(deck.cards[12].back_image_path)
    image_width = image.get_width()
    image_height = image.get_height()

    # Set the initial position of the image
    x = 0
    y = 0

    # Set the speed at which the image moves
    speed = .2

    # Create a loop that will run until the user quits
    running = True
    while running:

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the image
        x += speed
        if x > WINDOW_WIDTH:
            x = 0 - image_width

        # Draw the image on the screen
        window.fill((255, 255, 255))
        window.blit(image, (x, y))
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


moving_window()
