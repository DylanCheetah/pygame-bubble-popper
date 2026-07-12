Lesson 08: Game Over

Now that we our game ends once the game timer reaches 0, we need a way to restart the game. For this game we will add a game over screen which will return the player to the title screen when clicked. However, the game over screen will be overlaid over the paused game. To do this, we will first create `bubble_popper/scenes/game_over_screen.py` with the following content:
```python
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
```

In the `__init__` method we will load the font we need and render the game over label. In the `on_event` method we will switch to the title screen if the user clicked. In the `update` method we will show the mouse cursor if it is hidden. And in the `render` method we will draw the game over label in the center of the screen. Next we need to modify `bubble_popper/scenes/game.py` like this:
```python
"""Game Scene

This is the main scene for the bubble popping game.
"""

from typing import Any

import pygame
from pygame import Rect
from pygame.sprite import Group, GroupSingle
import pymunk
from pymunk.pygame_util import DrawOptions

from constants import OBJECT_TYPE_BUBBLE, OBJECT_TYPE_NEEDLE, OBJECT_TYPE_WALL
from objects.bubble import Bubble
from objects.needle import Needle
import res_mgr
from scene import Scene
from scenes.game_over_screen import GameOverScreen


# Constants
# =========
TEXT_COLOR = (255, 255, 255)


# Classes
# =======
class Game(Scene):
    def __init__(self):
        # Initialize variables
        self.spawn_timer = 0

        # Initialize sub-scenes
        self.game_over_screen = GameOverScreen()

        # Initialize sprite groups
        self.bubbles = Group()
        self.needles = GroupSingle()

        # Initialize physics
        self.space = pymunk.Space()

        # Create walls around the game area
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        left_wall_rect = Rect(screen_rect.topleft, (16, screen_rect.height))
        left_wall_rect.right = -1
        left_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        left_wall.position = left_wall_rect.center
        left_wall_shape = pymunk.Poly.create_box(left_wall, left_wall_rect.size)
        left_wall_shape.elasticity = 1
        left_wall_shape.collision_type = OBJECT_TYPE_WALL
        self.space.add(left_wall, left_wall_shape)

        right_wall_rect = Rect(screen_rect.topright, (16, screen_rect.height))
        right_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        right_wall.position = right_wall_rect.center
        right_wall_shape = pymunk.Poly.create_box(right_wall, right_wall_rect.size)
        right_wall_shape.elasticity = 1
        right_wall_shape.collision_type = OBJECT_TYPE_WALL
        self.space.add(right_wall, right_wall_shape)

        top_wall_rect = Rect(screen_rect.topleft, (screen_rect.width, 16))
        top_wall_rect.bottom = -1
        top_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        top_wall.position = top_wall_rect.center
        top_wall_shape = pymunk.Poly.create_box(top_wall, top_wall_rect.size)
        top_wall_shape.elasticity = 1
        top_wall_shape.collision_type = OBJECT_TYPE_WALL
        self.space.add(top_wall, top_wall_shape)

        bottom_wall_rect = Rect(screen_rect.bottomleft, (screen_rect.width, 16))
        bottom_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        bottom_wall.position = bottom_wall_rect.center
        bottom_wall_shape = pymunk.Poly.create_box(bottom_wall, bottom_wall_rect.size)
        bottom_wall_shape.elasticity = 1
        bottom_wall_shape.collision_type = OBJECT_TYPE_WALL
        self.space.add(bottom_wall, bottom_wall_shape)

        # Create needle
        self.needles.add(Needle(self.space))

        # Create debug draw interface
        self.debug_draw = DrawOptions(screen)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Configure collision detection callbacks
        self.space.on_collision(
            OBJECT_TYPE_BUBBLE, 
            OBJECT_TYPE_NEEDLE, 
            begin=self.on_bubble_hit_needle
        )

        # Load fonts
        self.hud_font = res_mgr.load_font("fonts/PixelOperatorMono.ttf", 32)

        # Reset score and game timer
        self.score = 0
        self.game_timer = 300

    def __del__(self):
        # Show the mouse cursor
        try:
            pygame.mouse.set_visible(True)
        
        except:
            pass  # any exceptions here would occur on application exit

    @property
    def score(self):
        # Return current score
        return self._score
    
    @score.setter
    def score(self, value):
        # Set current score and render score label
        self._score = value
        self.score_label = self.hud_font.render(
            f"Score: {self._score}", 
            False, 
            TEXT_COLOR
        )

    @property
    def game_timer(self):
        # Return current game timer
        return self._game_timer
    
    @game_timer.setter
    def game_timer(self, value):
        # Set current game timer and render game timer label
        self._game_timer = value
        self.game_timer_label = self.hud_font.render(
            f"{int(self._game_timer)}",
            False,
            TEXT_COLOR
        )

    def on_event(self, event):
        # If the game is over, pass the event to the game over screen
        if self.game_timer < 0:
            self.game_over_screen.on_event(event)

    def on_bubble_hit_needle(self, arbiter: pymunk.Arbiter, space: pymunk.Space, obj: Any):
        # Find the bubble which was hit by the needle
        hit_bubbles = filter(
            lambda bubble: bubble.body == arbiter.shapes[0].body, 
            self.bubbles
        )

        # Pop the bubble
        for bubble in hit_bubbles:
            bubble.pop()

        # Update the score
        self.score += 100

    def update(self, dt):
        # Update game timer
        if self.game_timer < 0:
            # Update game over screen
            self.game_over_screen.update(dt)
            return

        self.game_timer -= dt

        # Update spawn timer
        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            # Reset spawn timer
            self.spawn_timer = .25

            # Spawn a bubble
            if len(self.bubbles) < 20:
                self.bubbles.add(Bubble(self.space))

        # Update physics simulation
        self.space.step(dt)

        # Update sprites
        self.bubbles.update(dt)
        self.needles.update()

    def render(self, screen):
        # Render sprites
        self.bubbles.draw(screen)
        self.needles.draw(screen)

        # Render physics debug overlay
        # self.space.debug_draw(self.debug_draw)

        # Render HUD
        screen_rect = screen.get_rect()

        score_label_rect = self.score_label.get_rect()
        score_label_rect.topleft = (16, 16)
        screen.blit(self.score_label, score_label_rect)

        game_timer_label_rect = self.game_timer_label.get_rect()
        game_timer_label_rect.midtop = screen_rect.midtop
        game_timer_label_rect.y += 16
        screen.blit(self.game_timer_label, game_timer_label_rect)

        # If the game is over, render the game over screen
        if self.game_timer < 0:
            self.game_over_screen.render(screen)
```

In the `__init__` method we will create an instance of our game over screen. However, we will store it in a variable instead of making it the active scene. In our `on_event` method we will pass the event to the `on_event` method of the game over screen if the game timer is less than 0. In our `update` method we will pass the delta time to the `update` method of our game over screen if the game timer is less than 0. And in our `render` method we will pass the display surface to the `render` method of our game over screen if the game timer is less than 0. So we are essentially treating our game over screen as a sub-scene of our game screen.

If we run our game at this point you should see a game over message once the timer has reached 0 and you should be able to click to return to the title screen:
![game over screen](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/08-game_over_screen.png?raw=true)
