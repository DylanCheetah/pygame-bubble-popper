# Lesson 02: Project Setup

Now that we have installed the tools we will need, the next step is to setup our basic project structure. The first thing we need to do is create a folder for our project. Afterwards, open the project folder in Visual Studio Code. Before we continue, we will need to install the Python packages we will need for our project. However, it's a good idea to isolate them from our system-wide packages. To do this we will create a virtual environment. Click Terminal > New Terminal. Then execute the following command:
```sh
python -m venv venv
```

When prompted, select the virtual environment for the current project. Then close the terminal and open a new one to activate the virtual environment. Next, create `requirements.txt` with the following content:
```
pygame-ce
pymunk
setuptools
wheel
```

To install the packages, execute the following command:
```sh
pip install -r requirements.txt
```

Now we need to create a folder for our code. Create a folder called `bubble_popper`. Afterwards, your project structure should look like this:
```
pygame-bubble-popper/
    bubble_popper/
    venv/
    requirements.txt
```

Next we need to create `bubble_popper/main.py` with the following content:
```python
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

        # Update and render the active scene
        # TODO

        # Flip the display
        pygame.display.flip()

        # Limit framerate
        dt = clock.tick(TARGET_FPS) / 1000


# Entrypoint
# ==========
if __name__ == "__main__":
    main()
```

First, it will import pygame. Then it will set the constants we will need for the window title, window size, clear color, and target FPS. Next it will define a main function. And the entry point will call the main function. Inside the main function we will first call the `pygame.init` method to initialize pygame. Then we will set the window title by calling `pygame.display.set_caption` with the window title as the first parameter. Next we will set the display mode by calling `pygame.display.set_mode` with the window size as the first parameter. This method will return the display surface for our window. We will then set `dt` to 0. It will be used to store the delta time of each frame. Afterwards we will create a `pygame.Clock` object. The main loop will first loop over all pending events. If a `pygame.QUIT` event is found, we will return from the main function to end the application. Otherwise, we will pass the event to the active scene for further processing. Next, we will clear the screen by calling the `fill` method of the display surface with the clear color as the first parameter. Then we will update the active scene and render all existing scenes. Afterwards, we need to call `pygame.display.flip` to swap the front and back buffers for the display surface. Then we need to call the `tick` method of our clock object with the target FPS as the first parameter to limit the framerate. The return value will be the delta time in milliseconds. So we will need to divide it by 1000 and store it as the new delta time.

Now let's try running our code. Click Terminal > New Terminal to open a new terminal. Then execute the following commands:
```sh
cd bubble-popper
python main.py
```

You should see the following:
![game window](https://github.com/DylanCheetah/pygame-bubble-popper/blob/main/lessons/screenshots/01-game_window.png?raw=true)
