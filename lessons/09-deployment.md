# Lesson 09: Deployment

At this point our game is complete and ready for deployment. We have multiple options for deploying our game:
1. distribute the source code as-is (open-source project)
2. package our game using a tool such as `pyinstaller` (closed-source native app)
3. deploy our game as a web app using a tool such as `pygbag` (web app)

For this tutorial, we are going to go with option 3. `pygbag` is a Python package which can be used to deploy a pygame app as a web app. Please note that this only works with `pygame-ce`, not original `pygame` as of the time this tutorial was written. Before we proceed, we will also need to make a few adjustments to our game. Open `bubble_popper/main.py` and modify it like this:
```python
"""Bubble Popper

A simple bubble popping game.
"""

# /// script
# dependencies = [
#     "pygame-ce",
#     "pymunk"
# ]

import asyncio

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
async def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    dt = 0
    clock = pygame.time.Clock()

    # Initialize title screen
    TitleScreen().make_active()

    # Main loop
    while True:
        # Allow other tasks to run
        await asyncio.sleep(0)

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
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())

    except RuntimeError:
        asyncio.run(main())
```

pygbag expects our game to be async-aware. Therefore we must run our game as an asynchronous application. To do this we will make our `main` function async and at the beginning of the main loop we will call `asyncio.sleep`. We also need to run our main function in an asyncio event loop. After making these changes our game should run exactly the same as it did before. Notice that we also added a comment block near the top which lists the dependencies needed to run our game. This will be used by pygbag to determine which dependencies to download. Next we need to modify our `requirements.txt` file like this:
```
pygame-ce
pygbag
pymunk
setuptools
wheel
```

Then execute the following command from the root of your project folder:
```sh
pip install -r requirements.txt
```

Note: As of the timer this tutorial was written, pygbag only supports up to pymunk 6. Therefore we also need to modify the `__init__` method of our game screen in `bubble_popper/scenes/game.py` so it assigns our collision handler like this:
```python
# Configure collision detection callbacks
try:
    self.space.on_collision(
        OBJECT_TYPE_BUBBLE, 
        OBJECT_TYPE_NEEDLE, 
        begin=self.on_bubble_hit_needle
    )

except AttributeError:
    handler = self.space.add_collision_handler(
        OBJECT_TYPE_BUBBLE,
        OBJECT_TYPE_NEEDLE
    )
    handler.begin = self.on_bubble_hit_needle
```

Now we can deploy our game as a web app. Execute `pygbag --disable-sound-format-error bubble_popper` from the root of your project folder. Then visit http://localhost:8000/ in your web browser. You should see a loading message followed by a message saying to click. After clicking you should see your game. If your game crashes or freezes, try visiting http://localhost:8000/?-i to show a console with any error messages produced by Python:
![web app](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/09-web_app.png?raw=true)
