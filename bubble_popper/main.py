"""Bubble Popper

A simple bubble popping game.
"""

import pygame

from scene import Scene
from scenes.title_screen import TitleScreen


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

    # Initialize title screen
    TitleScreen().make_active()

    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            # Quit?
            if event.type == pygame.QUIT:
                return
            
            # Pass event to active scene
            Scene.get_active().on_event(event)
            
        # Clear the screen
        screen.fill(CLEAR_COLOR)

        # Update and render the active scene
        Scene.get_active().update(dt)
        Scene.get_active().render(screen)

        # Flip the display
        pygame.display.flip()

        # Limit framerate
        dt = clock.tick(TARGET_FPS) / 1000


# Entrypoint
# ==========
if __name__ == "__main__":
    main()
