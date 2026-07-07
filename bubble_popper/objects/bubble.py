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
