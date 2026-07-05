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
