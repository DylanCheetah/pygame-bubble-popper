# Lesson 04: Game Screen

Now that our title screen is complete, let's start creating our game screen. The first thing we're going to implement is a bubble sprite. Our bubble sprite will need a popping animation. The bubble spritesheet we used for the title screen has exactly 8 32x32 animation frames. To simplify extracting all 8 frames from our spritesheet, we will add a new method to our resource manager. Open `bubble_popper/res_mgr.py` and modify it like this:
```python
"""Resource Manager

A caching resource management system.
"""

from pathlib import Path
from typing import Any, IO, List, Union

import pygame


# Classes
# =======
class ResourceManager(object):
    def __init__(self):
        self._fonts = {}
        self._images = {}
        self._spritesheets = {}

    def load_font(self, *args) -> pygame.font.Font:
        """Load a font.
        
        If the font wasn't previously loaded, cache it before returning it. If the font was previously
        loaded, return the cached font object. Takes the same parameters as `pygame.font.Font`.
        """
        # Load the font if it isn't cached already
        if args not in self._fonts:
            self._fonts[args] = pygame.font.Font(*args)

        # Return cached font
        return self._fonts[args]
    
    def load_image(self, *args) -> pygame.Surface:
        """Load an image.
        
        If the image wasn't previously loaded, cached it before returning it. If the image was 
        previously loaded, return the cached image object. Takes the same parameters as 
        `pygame.image.load`.
        """
        # Generate key name
        key = args[0] if isinstance(args[0], (str, Path)) else args[1]

        # Load the image if it isn't cached already
        if args not in self._images:
            self._images[key] = pygame.image.load(*args).convert_alpha()

        # Return cached image
        return self._images[key]
    
    def load_spritesheet(
        self, 
        file: Union[str, Path, IO[Any]], 
        frame_size: Union[tuple, list, pygame.Vector2], 
        namehint: str = ""
    ) -> List[pygame.Surface]:
        """Load a spritesheet.
        
        The frame size determines the size of each frame. The returned list will contain one 
        `pygame.Surface` object per frame.
        """
        # Generate key name
        key = file if isinstance(file, (str, Path)) else namehint

        # Load the spritesheet if it isn't cached already
        if key not in self._spritesheets:
            # Load spritesheet image
            image = self.load_image(file, namehint)

            # Generate one sub-surface per frame
            frames = []

            for y in range(0, image.get_height(), frame_size[1]):
                for x in range(0, image.get_width(), frame_size[0]):
                    frames.append(image.subsurface((x, y), frame_size))

            # Cache the frames
            self._spritesheets[key] = frames

        # Return cached frames
        return self._spritesheets[key]
    

# Create resource manager instance
_res_mgr = ResourceManager()


# Functions
# =========
load_font = _res_mgr.load_font
load_image = _res_mgr.load_image
load_spritesheet = _res_mgr.load_spritesheet
```

The new `load_spritesheet` method takes a spritesheet image file and frame size as well as an optional name hint as parameters. It then returns a list of frames as `pygame.Surface` objects. This will allow us to easily load the frames of any spritesheet. Next, we need to create a `bubble_popper/objects/` folder for our game objects. Then we can create `bubble_popper/objects/bubble.py` with the following content:
```python
"""Bubble Sprite

A bubble which bounces off other bubbles and pops when it touches a needle.
"""

import random

import pygame
from pygame.sprite import Sprite
import pymunk

import res_mgr


# Classes
# =======
class Bubble(Sprite):
    def __init__(self, space: pymunk.Space):
        # Call the base constructor
        Sprite.__init__(self)

        # Load bubble spritesheet
        self.spritesheet = res_mgr.load_spritesheet("images/Bubble.png", (32, 32))

        # Set bubble image and rect
        screen_rect = pygame.display.get_surface().get_rect()
        self.image = self.spritesheet[0]
        self.rect = self.spritesheet[0].get_rect()
        self.rect.topleft = (
            random.randint(0, screen_rect.right - self.rect.width // 2),
            random.randint(0, screen_rect.bottom - self.rect.height // 2)
        )

        # Create a rigid body for this bubble
        self.body = pymunk.Body()
        self.body.position = self.rect.center
        self.shape = pymunk.Circle(self.body, 16)
        self.shape.mass = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

        # Apply an impulse in a random direction
        self.body.apply_impulse_at_local_point(
            pymunk.Vec2d(100, 0).rotated_degrees(random.randint(0, 359)))

    def __del__(self):
        # Remove this bubble from the physcis simulation
        try:
            self.body.space.remove(self.body, self.shape)

        except:
            pass  # any exceptions here would occur on application exit

    def update(self):
        # Update the position of this bubble
        self.rect.center = self.body.position
```

Our `Bubble` class extends the `pygame.sprite.Sprite` class which we imported at the top of this script. The `__init__` method of our bubble class requires a `pymunk.Space` object as its first parameter. We must remember to call the base constructor before the rest of the code in our `__init__` method. Afterwards, we will load the spritesheet for our bubble. Next we need to set the image and rectangle for our bubble. As with the title screen, we can make good use of rectangle objects here. But notice that this time we set the position of our bubble rectangle to a random value which lies within the screen bounds. The next thing we do is create a physics body for our bubble. Since pymunk treats the center as the origin of every physics body, we will need to set the position of the physics body for our bubble to the center of the rectangle for our bubble. Next we create a collision shape for our physics body. Since our bubble is round, we can use a circle. Then we set the mass and elasticity of our bubble. Afterwards, we can add the physics body and collision shape to our space object. We also need to apply a local impulse pointing in a random direction to set our bubble in motion. The `__del__` method of our bubble class removes the physics body and collision shape for our bubble from our space object. The `try` block catches exceptions which can occur based on garbage collection order. And the `update` method of our bubble class simply syncs the position of our bubble with the position of our physics body. Next we need to create our game screen. Create `bubble_popper/scenes/game.py` with the following content:
```python
"""Game Scene

This is the main scene for the bubble popping game.
"""

import pygame
from pygame import Rect
from pygame.sprite import Group
import pymunk
from pymunk.pygame_util import DrawOptions

from objects.bubble import Bubble
from scene import Scene

# Classes
# =======
class Game(Scene):
    def __init__(self):
        # Initialize variables
        self.spawn_timer = 0

        # Initialize sprite groups
        self.bubbles = Group()

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
        self.space.add(left_wall, left_wall_shape)

        right_wall_rect = Rect(screen_rect.topright, (16, screen_rect.height))
        right_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        right_wall.position = right_wall_rect.center
        right_wall_shape = pymunk.Poly.create_box(right_wall, right_wall_rect.size)
        right_wall_shape.elasticity = 1
        self.space.add(right_wall, right_wall_shape)

        top_wall_rect = Rect(screen_rect.topleft, (screen_rect.width, 16))
        top_wall_rect.bottom = -1
        top_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        top_wall.position = top_wall_rect.center
        top_wall_shape = pymunk.Poly.create_box(top_wall, top_wall_rect.size)
        top_wall_shape.elasticity = 1
        self.space.add(top_wall, top_wall_shape)

        bottom_wall_rect = Rect(screen_rect.bottomleft, (screen_rect.width, 16))
        bottom_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        bottom_wall.position = bottom_wall_rect.center
        bottom_wall_shape = pymunk.Poly.create_box(bottom_wall, bottom_wall_rect.size)
        bottom_wall_shape.elasticity = 1
        self.space.add(bottom_wall, bottom_wall_shape)

        # Create debug draw interface
        self.debug_draw = DrawOptions(screen)

    def on_event(self, event):
        pass

    def update(self, dt):
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
        self.bubbles.update()

    def render(self, screen):
        # Render sprites
        self.bubbles.draw(screen)

        # Render physics debug overlay
        # self.space.debug_draw(self.debug_draw)
```

Our `Game` class extends our `Scene` class. In the `__init__` method we first create a variable we will use to determine when to spawn a bubble. Next we create a sprite group for our bubbles. pygame provides multiple types of sprite groups. `pygame.sprite.Group` is a general purpose sprite group which will be sufficient for updating and rendering multiple bubbles. The next thing we need is a `pymunk.Space` object. This object will manage the physics for our game. Now we need to add 4 walls which enclose the game screen. This will keep our bubbles confined to the visible part of the screen. To do this we will first get a reference to the display surface and then get its rectangle. To create each wall we need to create a rectangle for one of the walls, adjust its position as needed, create a static body by using the `pymunk.Body` class, set the position of the static body to the center of its rectangle, create a box shape, set the elasticity of the shape to 1, and add the static body as well as the shape to the physics space object. We will also create a draw options object for debugging purposes. For now our `on_event` method will be empty. Our `update` method will start by decrementing our spawn timer by the delta time. If it is less than or equal to 0, we will set the spawn timer to .25. If there are less than 20 bubbles in our bubble group we will create a new bubble and add it to our bubble group. Next we need to update our physics space by passing the delta time to its `step` method. Afterwards we will update our bubbles by calling the `update` method of our bubble group. And our `render` method will draw our bubbles by passing the display surface to the `draw` method of our bubble group. We can also draw a physics debug overlay by passing our draw options object to the `debug_draw` method of our physics space object if desired. Now we just need to add a way to transition from our title screen to our game screen. To do this we will need to modify `bubble_popper/scenes/title_screen.py` like this:
```python
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
```

In our `on_event` method we need to check if the event was a mouse button up event. If it was, we need to create an instance of our game screen class `Game` and call its `make_active` method. Notice that we have chosen to import our `Game` class inside our `on_event` method. This is to prevent circular imports in case two scenes need to refer to each other later.

If we run our game at this point we should be able to click to start the game. Afterwards, bubbles should spawn and bounce off the sides of the game screen as well as each other:
![game screen](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/03-game_screen.png?raw=true)
