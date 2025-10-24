import pygame
from constants import *

pygame.font.init()
def_font = pygame.font.Font('./assets/fonts/Quicksand-Medium.ttf', 20)

class Sprite_Object(pygame.sprite.Sprite):
    def __init__(self, image: pygame.image, pos):
        super().__init__()
        self.image = image
        image_pos = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2)
        self.rect = self.image.get_rect(center=image_pos)


class Label(pygame.sprite.Sprite):
    def __init__(self, text, position, font=def_font, anchor='center'):
        super().__init__()
        self._font = font
        self._text = text
        self._color = (255, 255, 255)
        self._anchor = anchor
        self._position = position
        self._render()

    def _render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def clip(self, rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.rect)

    def set_text(self, text: str):
        self._text = text
        self._render()

    def set_font(self, font: pygame.font.Font):
        self._font = font
        self._render()

    def set_color(self, color):
        self._color = color
        self._render()

    def set_position(self, position, anchor=None):
        self._position = position
        if anchor:
            self._anchor = anchor

        self.rect = self.image.get_rect(**{self._anchor: self._position})



class Player(Sprite_Object):
    def __init__(self, image: pygame.image, pos, color):
        super().__init__(image, pos)
        self.color = color
        self.base = pos
        self.tiles: dict[tuple: "Tile"] = {}
        self.outposts: dict[tuple: "Outpost"] = {}


    def move(self, src_tile: "Tile", dest_tile: "Tile") -> bool:
        """Move army from a tile to another tile"""
        # Player should have more than 1 soldier in the source tile to move
        if src_tile.soldiers > 1:
            # Cost of move = 1 soldier
            # 1 soldier stays in the souce tile, the rest move to the destination
            # friendly_tile helps to know if the destination tile is friendly or not to not kill own soldiers.
            friendly_tile: bool = dest_tile.player == self if dest_tile.player else -1
            dest_tile.soldiers = src_tile.soldiers - 1 + (friendly_tile * dest_tile.soldiers)
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
                self.tiles[dest_tile.pos] = dest_tile
                if isinstance(dest_tile, Outpost):
                    self.outposts[dest_tile.pos] = dest_tile
            
            return True
        
        return False
    

    def draw_tiles(self, surface):
        for tile in self.tiles.values():
            tile.draw(surface)
    
    def regenerate_bases(self):
        """Spawns a soldier in the player's base and outposts"""
        self.tiles[self.base].soldiers += 1
        for outpost in self.outposts.values():
            outpost.soldiers += 1


    def regenerate_all(self):
        for tile in self.tiles.values():
            tile.soldiers += 1


class Mountain(Sprite_Object):
    def __init__(self, image: pygame.image, pos):
        super().__init__(image, pos)
        self.pos = pos
        

    def draw(self, surface):
        topleft = (self.pos[0] +TILE_BORDER_SIZE, self.pos[1]+TILE_BORDER_SIZE)
        pygame.draw.rect(surface, "#BBBBBB", (*topleft, TILE_SIZE, TILE_SIZE))
        surface.blit(self.image, self.rect)


class Tile():
    """A tile in the grid"""
    def __init__(self, pos, soldiers=0):
        self.pos = pos
        self.soldiers: int = soldiers
        self.player: Player = None
        label_position = (self.pos[0] + TILE_SIZE // 2, self.pos[1] + TILE_SIZE // 2)
        self.label = Label("", label_position)
        self.default_tile_color = "#DCDCDC"

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.pos == other.pos
        elif isinstance(other, tuple):
            return self.pos == other
        return NotImplemented
    
    def __str__(self):
        return f"Tile at {self.pos}, with {self.soldiers} soldiers of {self.player}"
    
    def __hash__(self):
        return hash(self.pos)

    def _draw_player_tile(self, screen, topleft):
        pygame.draw.rect(screen, self.player.color, (*topleft, TILE_BODY_SIZE, TILE_BODY_SIZE))
        screen.blit(self.player.image, self.player.rect)
        self.label.set_text(str(self.soldiers) if self.soldiers > 0 else "")
        self.label.draw(screen)

    def _draw_non_player_tile(self, screen, topleft):
        pygame.draw.rect(screen, self.default_tile_color, (*topleft, TILE_BODY_SIZE, TILE_BODY_SIZE))

    def draw(self, screen: pygame.surface.Surface):
        topleft = (self.pos[0] +TILE_BORDER_SIZE, self.pos[1]+TILE_BORDER_SIZE)
        if self.player:
            self._draw_player_tile(screen, topleft)
        else:
            self._draw_non_player_tile(screen, topleft)


class Outpost(Tile, Sprite_Object):
    def __init__(self, image, pos, soldiers):
        Tile.__init__(self, pos, soldiers)
        Sprite_Object.__init__(self, image, pos)
        self.default_tile_color = "#808080"


    def _draw_player_tile(self, screen, topleft):
        pygame.draw.rect(screen, self.player.color, (*topleft, TILE_BODY_SIZE, TILE_BODY_SIZE))
        screen.blit(self.image, self.rect)
        self.label.set_text(str(self.soldiers) if self.soldiers > 0 else "")
        self.label.draw(screen)

    def _draw_non_player_tile(self, screen, topleft):
        pygame.draw.rect(screen, self.default_tile_color, (*topleft, TILE_BODY_SIZE, TILE_BODY_SIZE))
        screen.blit(self.image, self.rect)
        self.label.set_text(str(self.soldiers) if self.soldiers > 0 else "")
        self.label.draw(screen)






    
    