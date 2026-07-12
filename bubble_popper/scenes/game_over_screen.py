"""Game Over Screen

The screen which will be displayed once the game has ended.
"""

import pygame

import res_mgr
from scene import Scene


# Constants
# =========
TEXT_COLOR = (255, 255, 255)


# Classes
# =======
class GameOverScreen(Scene):
    def __init__(self):
        # Load fonts
        self.font = res_mgr.load_font("fonts/PixelOperatorMono.ttf", 64)

        # Render the game over label
        self.game_over_label = self.font.render(
            "Game Over",
            False,
            TEXT_COLOR
        )

    def on_event(self, event):
        # Switch to the title screen when the user clicks
        if event.type == pygame.MOUSEBUTTONUP:
            from scenes.title_screen import TitleScreen
            TitleScreen().make_active()

    def update(self, dt):
        # Show mouse cursor
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

    def render(self, screen):
        # Render the game over label
        screen_rect = screen.get_rect()

        game_over_label_rect = self.game_over_label.get_rect()
        game_over_label_rect.center = screen_rect.center
        screen.blit(self.game_over_label, game_over_label_rect)
