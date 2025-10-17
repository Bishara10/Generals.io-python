import pygame
from random import randint
from Components import *
from constants import *
from Utils import *
import time

pygame.init()
pygame.display.set_caption("Generals")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("#DCDCDC")
clock = pygame.time.Clock()

# Load sprites
mountain_image = pygame.image.load("mountain.jpg").convert_alpha()
mountain_image = pygame.transform.scale(mountain_image, (TILE_SIZE, TILE_SIZE))
base_image = pygame.image.load("base.png").convert_alpha()
base_image = pygame.transform.scale(base_image, (TILE_SIZE, TILE_SIZE))


# Mountains
mountains_sprites = pygame.sprite.Group()
mountains_positions = set()
for _ in range(70):
    pos = get_random_location()

    if pos not in mountains_positions:
        mountains_positions.add(pos)
        mountains_sprites.add(Mountain(mountain_image, pos))

# Available positions are all tiles in the grid that are not mountains.
available_positions = set([(x//TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE) 
                           for x in range(0, SCREEN_WIDTH, TILE_SIZE) 
                           for y in range(0, SCREEN_HEIGHT, 20)]) - mountains_positions

positions = set()

def draw_tiles(positions):
    for position in positions:
        col, row = position
        topleft = (col+TILE_BORDER_SIZE, row+TILE_BORDER_SIZE)
        pygame.draw.rect(screen, "#2792FF", (*topleft, CONQUERED_TILE_SIZE, CONQUERED_TILE_SIZE))

def draw_grid():
    for i in range(N_TILES):
        # vertical line
        pygame.draw.line(screen, (10, 10, 10), (TILE_SIZE*i, 0), (TILE_SIZE*i, SCREEN_HEIGHT), TILE_BORDER_SIZE)
        # horizontal line
        pygame.draw.line(screen, (10, 10, 10), (0, TILE_SIZE*i), (SCREEN_WIDTH, TILE_SIZE*i), TILE_BORDER_SIZE)


# Players
player1 = Player(base_image, get_random_location(available_positions))
tiles = []

# keep track of information for available tiles
for pos in available_positions:
    tiles.append(Tile(pos))


mountains_sprites.draw(screen) 
screen.blit(player1.image, player1.rect)
draw_grid()
draw_tiles(positions)

def main():
    # game loop
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            row = y // TILE_SIZE * TILE_SIZE
            col = x // TILE_SIZE * TILE_SIZE
            pos = (col, row)
            if pos not in mountains_positions and pos != player1.rect.topleft:
                positions.add(pos)
                draw_tiles([pos])



        pygame.display.update()

main()
