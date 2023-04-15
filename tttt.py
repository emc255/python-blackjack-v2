import sys

import pygame as pg
from pygame.math import Vector2

# Define constants for the card dimensions
CARD_WIDTH = 72
CARD_HEIGHT = 96

# Initialize Pygame
pg.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Create the screen surface
screen = pg.display.set_mode((screen_width, screen_height))

# Load the card image onto the card surface
card_surface = pg.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pg.SRCALPHA)
card_image = pg.image.load("resources/images/cards/back.png")
card_surface.blit(card_image, (0, 0))

# Define the starting and ending points for the card
start_pos = Vector2(350, 124)
end_pos = Vector2(480, 356)

# Calculate the direction and distance between the starting and ending points
direction = (end_pos - start_pos).normalize()
distance = (end_pos - start_pos).length()

# Set the initial position of the card surface to the starting point
card_pos = start_pos

# Set the speed of the card movement
speed = .1

# Game loop
while True:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Update the position of the card surface based on the direction and speed
    card_pos += direction * speed
    print(card_pos)
    # If the card has reached the ending point, reset its position to the starting point
    if (card_pos - start_pos).length() >= distance:
        card_pos = start_pos

    # Blit the card surface onto the screen surface at the current position
    screen.blit(card_surface, card_pos)

    # Update the display
    pg.display.flip()