"""Bubble Popper

A simple bubble popping game.
"""

import pygame


# Constants
# =========
WINDOW_TITLE = "Bubble Popper"
WINDOW_SIZE = (800, 600)
CLEAR_COLOR = (0, 0, 0)
TARGET_FPS = 60


# Functions
# =========
def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    dt = 0
    clock = pygame.Clock()

    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            # Quit?
            if event.type == pygame.QUIT:
                return
            
            # Pass event to active scene
            # TODO
            
        # Clear the screen
        screen.fill(CLEAR_COLOR)

        # Update active scene
        # TODO

        # Render existing scenes
        # TODO

        # Flip the display
        pygame.display.flip()

        # Limit framerate
        dt = clock.tick(TARGET_FPS) / 1000


# Entrypoint
# ==========
if __name__ == "__main__":
    main()
