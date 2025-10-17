import pygame
from constants import *

class Sprite_Object(pygame.sprite.Sprite):
    def __init__(self, image: pygame.image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class Player(Sprite_Object):
    def __init__(self, image: pygame.image, pos):
        super().__init__(image, pos)


class Mountain(Sprite_Object):
    def __init__(self, image: pygame.image, pos):
        super().__init__(image, pos)


class Tile():
    def __init__(self, pos):
        self.pos = pos
        self.soldiers = 0
        self.player = None
    
    def conquer(self, player):
        """Set player that conquered this tile"""
        self.player = player
    
    def set_soldiers(self, soldiers):
        """Set number of soldiers in tile currently"""
        self.soldiers = soldiers
    
    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.pos == other.pos

        elif isinstance(other, tuple):
            return self.pos == other
        
        return NotImplemented
        

class Outpost(Tile):
    def __init__(self, pos):
        super().__init__(pos)

    
    