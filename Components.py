import pygame
from constants import *

class Sprite_Object(pygame.sprite.Sprite):
    def __init__(self, image: pygame.image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class Player(Sprite_Object):
    def __init__(self, image: pygame.image, pos, color):
        super().__init__(image, pos)
        self.base = pos
        self.color = color
        self.tiles = set()


    def move(self, src_tile: "Tile", dest_tile: "Tile"):
        """Move army from a tile to another tile"""
        # Player should have more than 1 soldier in the source tile to move
        if src_tile.soldiers > 1:
            # Cost of move = 1 soldier
            # 1 soldier stays in the souce tile, the rest move to the destination
            dest_tile.soldiers = src_tile - 1 - dest_tile.soldiers
            src_tile.soldiers = 1

            if dest_tile.soldiers < 0:
                # If the subtraction is negative, that means this player failed
                # to defeat the other player in the destination tile. The destination
                # Tile stays with the enemy player.
                dest_tile.soldiers *= -1
            
            else:
                # Otherwise, this player conquers the tile even if the subtraction
                # result is 0.
                dest_tile.player = self


class Mountain(Sprite_Object):
    def __init__(self, image: pygame.image, pos):
        super().__init__(image, pos)


class Tile():
    def __init__(self, pos):
        self.pos = pos
        self.soldiers: int = 0
        self.player: Player = None

    
    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.pos == other.pos

        elif isinstance(other, tuple):
            return self.pos == other
        
        return NotImplemented
        

class Outpost(Tile):
    def __init__(self, pos):
        super().__init__(pos)

    
    