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
