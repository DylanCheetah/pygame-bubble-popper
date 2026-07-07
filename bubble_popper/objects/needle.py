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
