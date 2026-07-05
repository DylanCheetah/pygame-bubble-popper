# Lesson 03: Title Screen

Now that we have our basic project structure setup, we can create the title screen for our game. But first we need to download the font and images we will be using on our title screen. Create a `fonts` folder and an `images` folder inside the `bubble_popper` folder. Then download *font* and save it in `bubble_popper/fonts/`. Afterwards, download *image* and save it in `bubble_popper/images/`. Now your project structure should look like this:
```
pygame-bubble-popper/
    bubble_popper/
        fonts/
            PixelOperatorMono.ttf
        images/
            Bubble.png
        main.py
    venv/
    requirements.txt
```

Since our game assets will be used from multiple parts of our code, we will create a resource manager which will handle loading our game assets. Also, we will design it so that it caches resources so they only need to be loaded once. Create `bubble_popper/res_mgr.py` with the following code:
```python
"""Resource Manager

A caching resource management system.
"""

import pygame


# Classes
# =======
class ResourceManager(object):
    def __init__(self):
        self.fonts = {}
        self.images = {}

    def load_font(self, *args) -> pygame.font.Font:
        """Load a font.
        
        If the font wasn't previously loaded, cache it before returning it. If the font was previously
        loaded, return the cached font object. Takes the same parameters as `pygame.font.Font`.
        """
        # Load the font if it isn't cached already
        if args not in self.fonts:
            self.fonts[args] = pygame.font.Font(*args)

        # Return cached font
        return self.fonts[args]
    
    def load_image(self, *args) -> pygame.Surface:
        """Load an image.
        
        If the image wasn't previously loaded, cached it before returning it. If the image was 
        previously loaded, return the cached image object. Takes the same parameters as 
        `pygame.image.load`.
        """
        # Generate key name
        key = args[0] if isinstance(args[0], str) else args[1]

        # Load the image if it isn't cached already
        if args not in self.images:
            self.images[key] = pygame.image.load(*args).convert_alpha()

        # Return cached image
        return self.images[key]
    

# Create resource manager instance
_res_mgr = ResourceManager()


# Functions
# =========
load_font = _res_mgr.load_font
load_image = _res_mgr.load_image
```

The general idea is to use one dictionary per resources type to cache whatever resources we load. If a resource isn't in the cache it will be loaded into the cache before returning it. Next, we will structure our game so that it consists of a series of scenes. Before we create our title screen, we will need to create a base class for our scenes. Create `bubble_popper/scene.py` with the following content:
```python
"""Scene

Base class for a scene.
"""

import pygame


# Classes
# =======
class Scene(object):
    """Base class for a scene.
    
    To create a scene class, extend this class. Then define a constructor which loads resources needed
    by the scene. If the scene changes any global game states, you may also need to define a destructor
    which restores the previous game states. The `on_event`, `update`, and `render` methods need to be
    overidden in derived classes.
    """
    _active = None

    def on_event(self, event: pygame.event.Event) -> None:
        """Handle a pygame event.
        
        Parameters:
        event - the pygame event to handle
        """
        pass

    def update(self, dt: float) -> None:
        """Execute per-frame scene logic.
        
        Parameters:
        dt - the delta time in seconds
        """
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render the scene.
        
        Parameters:
        screen - the display surface
        """
        pass

    def make_active(self) -> None:
        """Make this scene active.
        
        Only one scene can be active at a time. Calling this will make the active scene inactive. If
        you need to have multiple active scenes for purposes such as rendering a pause menu over the
        game scene, then you need to create a sub-scene within the constructor of your main scene and
        manually call the `on_event`, `update`, and `render` methods of the sub-scene as needed.
        """
        Scene._active = self

    @staticmethod
    def get_active() -> "Scene":
        """Get the active scene.
        
        Returns:
        the active scene object
        """
        return Scene._active
```

The concept of a scene is pretty simple. Each scene will have a constructor which loads any resources it needs when it is created. The `on_event` method will be called to handle each pygame event, the `update` method will be called to update the objects in the scene based on the given delta time, and the `render` method will render the scene to the given display surface. Only one scene can be active at a time, but we can have sub-scenes to implement things such as pause screens when necessary. Now that we have our scene base class, let's implement our title screen class. First we need to create a `bubble_popper/scenes/` folder for our scene class files. Then we need to create `bubble_popper/scenes/title_screen.py` with the following content:
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
        pass

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

Since our title screen will need the resource manager and scene base class we previously defined, we will first need to import them in addition to pygame. Afterwards we define constants for the path to our font file as well as the color of the text on the title screen. Our `TitleScreen` class needs to extend our `Scene` class. The `__init__` method of our title screen class needs to set the alpha increment used for fading the hint text in/out, load the fonts and images we need, and pre-render the text we will need. Since the image for our bubble is a spritesheet, we will need to extract the subsurface which corresponds to the animation frame we need to render. Additionally, we need to scale the the first frame of the bubble image up to 128x128. Then we need to render the text we will be using on the title screen. For now our `on_event` method will be empty. The `update` method will get the current alpha value of the hint text, increment the current alpha value by the alpha increment multiplied by the delta time, invert the alpha increment when the alpha value lies outside the 0 to 255 range, and set the current alpha value of the hint text. Our `render` method will draw the title text at the top center of the window, draw the bubble in the center of the window, and draw the hint text at the bottom center of the window. Notice how we can make good use of rectangle objects to help us calculate the correct location for each part of the title screen. Next we need to modify `bubble_popper/main.py` like this:
```python
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
```

The first thing we changed was adding a line to import our title screen class. Before our main loop we need to create an instance of our title screen class and call its `make_active` method. Notice that we don't need to store a reference to it. This is because the scene base class stores a reference to the active scene for us. In our event handling loop we need to pass the event object to the `on_event` method of the active scene. And last but not least, we need to call the `update` method of the active scene followed by the `render` method of the active scene after we clear the screen each frame.

If we run our code at this point, we should see our title screen and the hint text should slowly fade in and out:
*screenshot*
