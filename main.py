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
for _ in range(100):
    pos = get_random_location()

    if pos not in mountains_positions:
        mountains_positions.add(pos)
        mountains_sprites.add(Mountain(mountain_image, pos))

available_positions = set([(x//TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE) 
                           for x in range(0, SCREEN_WIDTH, TILE_SIZE) 
                           for y in range(0, SCREEN_HEIGHT, 20)]) - mountains_positions
positions = set()

def draw_grid(positions: set):
    for position in positions:
        col, row = position
        topleft = (col, row)
        pygame.draw.rect(screen, "#2792FF", (*topleft, TILE_SIZE, TILE_SIZE))


    for i in range(N_TILES):
        # vertical line
        pygame.draw.line(screen, (10, 10, 10), (TILE_SIZE*i, 0), (TILE_SIZE*i, SCREEN_HEIGHT), 2)
        # horizontal line
        pygame.draw.line(screen, (10, 10, 10), (0, TILE_SIZE*i), (SCREEN_WIDTH, TILE_SIZE*i), 2)


# Players
player1 = Player(base_image, get_random_location(available_positions))


def main():
    # game loop
    running = True
    while running:
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

        mountains_sprites.draw(screen)
        screen.blit(player1.image, player1.rect)
        draw_grid(positions)

        pygame.display.update()

main()
