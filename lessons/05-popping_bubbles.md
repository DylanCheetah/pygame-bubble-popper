# Lesson 05: Popping Bubbles

Now that we have bubbles spawning and bouncing around, we need to add a way to pop them. For this game we will create a needle sprite which follows the mouse that we can use to pop the bubbles. First we need to download https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/bubble_popper/images/Needle.png?raw=true and save it in `bubble_popper/images/`. We will also need a nice popping sound effect for our bubble, so we also need to create a `bubble_popper/sfx/` folder and download https://github.com/DylanCheetah/pygame-bubble-popper/raw/refs/heads/main/bubble_popper/sfx/Bubble-Pop.ogg into it. Our project structure should look like this now:
```
pygame-bubble-popper/
    bubble_popper/
        fonts/
            PixelOperatorMono.ttf
        images/
            Bubble.png
            Needle.png
        objects/
            bubble.py
        scenes/
            game.py
            title_screen.py
        sfx/
            Bubble-Pop.ogg
        main.py
        res_mgr.py
        scene.py
    requirements.txt
```

We're going to need some constants which will be used in multiple parts of our game. So let's put them in a file called `bubble_popper/constants.py`:
```python
"""Constants

A collection of constants used by multiple parts of the game.
"""

# Constants
# =========
OBJECT_TYPE_WALL   = 1
OBJECT_TYPE_BUBBLE = 2
OBJECT_TYPE_NEEDLE = 3
```

Now we need to create `bubble_popper/objects/needle.py` with the following content:
```python
"""Needle

A needle which follows the mouse and pops bubbles.
"""

import pygame
from pygame.sprite import Sprite
import pymunk

from constants import OBJECT_TYPE_NEEDLE
import res_mgr


# Classes
# =======
class Needle(Sprite):
    def __init__(self, space: pymunk.Space):
        # Call the base constructor
        Sprite.__init__(self)

        # Set image and rectangle
        self.image = res_mgr.load_image("images/Needle.png")
        self.rect = self.image.get_rect()

        # Create physics body
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, self.rect.size)
        self.shape.sensor = True
        self.shape.collision_type = OBJECT_TYPE_NEEDLE
        space.add(self.body, self.shape)

    def __del__(self):
        # Remove this needle from the physics simulation
        try:
            self.body.space.remove(self.body, self.shape)

        except:
            pass  # any exceptions here would occur on application exit

    def update(self):
        # Update the position of this bubble
        mouse_pos = pygame.mouse.get_pos()
        self.rect.midtop = mouse_pos
        self.body.position = self.rect.center
```

Our `Needle` class extends the `pygame.sprite.Sprite` class. The `__init__` method requires a `pymunk.Space` object as its first parameter. We must remember to call the base constructor before the rest of our code. Then we set the image and rectangle for our needle. The physics body for our needle is going to be a kinematic body. A kinematic body collides with other physics bodies, but it is moved via code instead of by the physics engine. The collision shape will be a box and it will be set to sensor mode. In sensor mode a collision shape will detect collisions, but it won't influence the velocity of other physics bodies. Also, notice that we set the collision type to `OBJECT_TYPE_NEEDLE`. This will be crucial for properly detecting collisions between our needle and our bubbles. Lastly, we need to add our physics body and shape to the physics space object. As with our bubble class, we must remove our needle from the pysics space in our `__del__` method. Our `update` method is a bit different though. Since we want the needle to follow the mouse, we first get the mouse position. Then we set the point of the needle to the mouse position. And we set the position of the physics body to the center of the rectangle. Rigid bodies are moved by the physics engine and their position gets assigned to the position of the object. However, kinematic bodies are moved via code by assigning the position of the object to them. Now that we have our needle, we need to add it to our game screen by modifying `bubble_popper/scenes/game.py` like this:
```python
"""Game Scene

This is the main scene for the bubble popping game.
"""

import pygame
from pygame import Rect
from pygame.sprite import Group, GroupSingle
import pymunk
from pymunk.pygame_util import DrawOptions

from objects.bubble import Bubble
from objects.needle import Needle
from scene import Scene

# Classes
# =======
class Game(Scene):
    def __init__(self):
        # Initialize variables
        self.spawn_timer = 0

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

        # Create needle
        self.needles.add(Needle(self.space))

        # Create debug draw interface
        self.debug_draw = DrawOptions(screen)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def __del__(self):
        # Show the mouse cursor
        try:
            pygame.mouse.set_visible(True)
        
        except:
            pass  # any exceptions here would occur on application exit

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
        self.needles.update()

    def render(self, screen):
        # Render sprites
        self.bubbles.draw(screen)
        self.needles.draw(screen)

        # Render physics debug overlay
        # self.space.debug_draw(self.debug_draw)
```

In our `__init__` method we need to create a new group for our needle. However, we only ever have one needle. So we use `pygame.sprite.GroupSingle` for this purpose. Then we create our needle and add it to our needle group. Since we are essentially using our needle as a cursor, we will hide the mouse cursor as well. We also need to create a `__del__` method which shows the mouse cursor. In our `update` method we must call the `update` method of our needle group after we update our bubble group. And in our `render` method we need to pass the display surface to the `draw` method of our needle group after we have drawn our bubbles. Remember, the last sprites we draw will appear on top.

If we run our game at this point, you will be able to move the needle by moving the mouse. However, you will also notice that the bubbles don't pop when touched by the needle:
![needle](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/04-needle.png?raw=true)

To fix this, we will need to do a few more things. First we need to modify `bubble_popper/objects/bubble.py` like this:
```python
"""Bubble Sprite

A bubble which bounces off other bubbles and pops when it touches a needle.
"""

import random

import pygame
from pygame.sprite import Sprite
import pymunk

from constants import OBJECT_TYPE_BUBBLE
import res_mgr


# Classes
# =======
class Bubble(Sprite):
    def __init__(self, space: pymunk.Space):
        # Call the base constructor
        Sprite.__init__(self)

        # Initialize variables
        self.anim_speed = 0
        self.frame = 0

        # Load bubble spritesheet
        self.spritesheet = res_mgr.load_spritesheet("images/Bubble.png", (32, 32))

        # Set bubble image and rect
        screen_rect = pygame.display.get_surface().get_rect()
        self.image = self.spritesheet[self.frame]
        self.rect = self.spritesheet[self.frame].get_rect()
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
        self.shape.collision_type = OBJECT_TYPE_BUBBLE
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

    def update(self, dt):
        # Update the position of this bubble
        self.rect.center = self.body.position

        # Update bubble animation
        self.frame += self.anim_speed * dt

        if int(self.frame) >= len(self.spritesheet):
            # Dispose of this bubble
            self.kill()
            return

        self.image = self.spritesheet[int(self.frame)]

    def pop(self):
        # Disable physics for this bubble and start the popping animation
        self.body.space.remove(self.body, self.shape)
        self.anim_speed = 10
```

The new `anim_speed` and `frame` variables defined in our `__init__` method will be used to determine the speed and current frame of the popping animation. In our `update` method we will increment the current frame by the animation speed multiplied by the delta time which now must be passed as a parameter. If the current frame is greater than or equal to the total number of frames in our spritesheet, we will dispose of the bubble and return. Otherwise, we will set the bubble image to the current frame from the spritesheet. Don't forget to convert the frame number to an integer before using it as an index into the spritesheet. Our new `pop` method simply removes the bubble from the physics space and sets the animation speed to 10. Calling it will cause the bubble to stop moving and play its popping animation. Once the animation finishes it will be disposed of. Popping bubbles also won't collide with other objects anymore. Next we need to modify `bubble_popper/scenes/game.py` like this:
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
from scene import Scene

# Classes
# =======
class Game(Scene):
    def __init__(self):
        # Initialize variables
        self.spawn_timer = 0

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

    def __del__(self):
        # Show the mouse cursor
        try:
            pygame.mouse.set_visible(True)
        
        except:
            pass  # any exceptions here would occur on application exit

    def on_event(self, event):
        pass

    def on_bubble_hit_needle(self, arbiter: pymunk.Arbiter, space: pymunk.Space, obj: Any):
        # Find the bubble which was hit by the needle
        hit_bubbles = filter(
            lambda bubble: bubble.body == arbiter.shapes[0].body, 
            self.bubbles
        )

        # Pop the bubble
        for bubble in hit_bubbles:
            bubble.pop()

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
        self.bubbles.update(dt)
        self.needles.update()

    def render(self, screen):
        # Render sprites
        self.bubbles.draw(screen)
        self.needles.draw(screen)

        # Render physics debug overlay
        # self.space.debug_draw(self.debug_draw)
```

Our new `on_bubble_hit_needle` method will be called whenever a bubble hits the needle. We can determine which bubble hit the needle by filtering our bubble group by the first physics body in the arbitor object. Then we just need to call its `pop` method.

If we run our game now, you should be able to pop bubbles by moving the needle with the mouse:
![popping bubbles](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/05-popping_bubbles.png?raw=true)

However, there isn't any popping sound effect yet. To fix this, we first need to add support for loading sound effects to our resource manager by modifying `bubble_popper/res_mgr.py` like this:
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
        self._sfx = {}

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
    
    def load_sfx(self, 
            file: Union[str, Path, IO[Any]], 
            namehint: str = ""
        ) -> pygame.mixer.Sound:
        """Load a sound effect.
        
        If the sound effect wasn't previously loaded, cache it before returning 
        it. If the sound effect was previously loaded, return the cached sound 
        effect. Takes the same parameters as `pygame.mixer.Sound`.
        """
        # Generate key name
        key = file if isinstance(file, (str, Path)) else namehint

        # Load the sound effect if it isn't cached already
        if key not in self._sfx:
            self._sfx[key] = pygame.mixer.Sound(file)

        # Return cached sound effect
        return self._sfx[key]
    

# Create resource manager instance
_res_mgr = ResourceManager()


# Functions
# =========
load_font = _res_mgr.load_font
load_image = _res_mgr.load_image
load_spritesheet = _res_mgr.load_spritesheet
load_sfx = _res_mgr.load_sfx
```

And now we can just modify `bubble_popper/objects/bubble.py` slightly:
```python
"""Bubble Sprite

A bubble which bounces off other bubbles and pops when it touches a needle.
"""

import random

import pygame
from pygame.sprite import Sprite
import pymunk

from constants import OBJECT_TYPE_BUBBLE
import res_mgr


# Classes
# =======
class Bubble(Sprite):
    def __init__(self, space: pymunk.Space):
        # Call the base constructor
        Sprite.__init__(self)

        # Initialize variables
        self.anim_speed = 0
        self.frame = 0

        # Load bubble spritesheet
        self.spritesheet = res_mgr.load_spritesheet("images/Bubble.png", (32, 32))

        # Set bubble image and rect
        screen_rect = pygame.display.get_surface().get_rect()
        self.image = self.spritesheet[self.frame]
        self.rect = self.spritesheet[self.frame].get_rect()
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
        self.shape.collision_type = OBJECT_TYPE_BUBBLE
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

    def update(self, dt):
        # Update the position of this bubble
        self.rect.center = self.body.position

        # Update bubble animation
        self.frame += self.anim_speed * dt

        if int(self.frame) >= len(self.spritesheet):
            # Dispose of this bubble
            self.kill()
            return

        self.image = self.spritesheet[int(self.frame)]

    def pop(self):
        # Disable physics for this bubble and start the popping animation
        self.body.space.remove(self.body, self.shape)
        self.anim_speed = 10
        res_mgr.load_sfx("sfx/Bubble-Pop.ogg").play()
```

And now our game should have audio when we run it.
