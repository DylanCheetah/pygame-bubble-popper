"""Title Screen

The title screen of our game.
"""

import pygame

import res_mgr
from scene import Scene

# Constants
# =========
MAIN_FONT = "fonts/PixelOperatorMono.ttf"
TEXT_COLOR = (255, 255, 255)


# Classes
# =======
class TitleScreen(Scene):
    def __init__(self):
        # Initialize variables
        self.alpha_inc = -200

        # Load fonts
        self.large_font = res_mgr.load_font(MAIN_FONT, 64)
        self.med_font = res_mgr.load_font(MAIN_FONT, 32)

        # Load images
        bubble = res_mgr.load_image("images/Bubble.png")
        bubble = bubble.subsurface(0, 0, 32, 32)
        self.bubble = pygame.transform.scale(bubble, (128, 128))

        # Pre-render text
        self.title = self.large_font.render("Bubble Popper", False, TEXT_COLOR)
        self.hint_text = self.med_font.render("Click to Start", False, TEXT_COLOR)

    def on_event(self, event):
        # Mouse button up?
        if event.type == pygame.MOUSEBUTTONUP:
            # Start the game
            from scenes.game import Game
            Game().make_active()

    def update(self, dt):
        # Fade hint text in/out
        hint_text_alpha = self.hint_text.get_alpha()
        hint_text_alpha = (hint_text_alpha if hint_text_alpha is not None else 255)
        hint_text_alpha += self.alpha_inc * dt

        if hint_text_alpha < 0 or hint_text_alpha >= 255:
            self.alpha_inc = -self.alpha_inc

        self.hint_text.set_alpha(hint_text_alpha)

    def render(self, screen):
        # Render title
        screen_rect = screen.get_rect()
        title_rect = self.title.get_rect()
        title_rect.midtop = screen_rect.midtop
        title_rect.y += 16
        screen.blit(self.title, title_rect)

        # Render bubble
        bubble_rect = self.bubble.get_rect()
        bubble_rect.center = screen_rect.center
        screen.blit(self.bubble, bubble_rect)

        # Render hint text
        hint_text_rect = self.hint_text.get_rect()
        hint_text_rect.midbottom = screen_rect.midbottom
        hint_text_rect.y -= 16
        screen.blit(self.hint_text, hint_text_rect)
