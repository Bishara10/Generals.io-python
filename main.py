import pygame
from random import randint
from Components import *
from constants import *
from Utils import *

pygame.init()
pygame.display.set_caption("Generals")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("#DCDCDC")
clock = pygame.time.Clock()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

inputs = {pygame.K_UP: (0, -TILE_SIZE), 
          pygame.K_DOWN: (0, TILE_SIZE),
          pygame.K_LEFT: (-TILE_SIZE, 0), 
          pygame.K_RIGHT: (TILE_SIZE, 0)
        }

# Load sprites
mountain_sprite = pygame.image.load("assets/images/mountain.png").convert_alpha()
base_sprite = pygame.image.load("assets/images/crown.png").convert_alpha()
outpost_sprite = pygame.image.load("assets/images/outpost.png").convert_alpha()


positions = set()
available_tiles = {}


# Mountains
mountains_sprites = pygame.sprite.Group()
mountains_positions = set()
for _ in range(70):
    pos = get_random_location()

    if pos not in mountains_positions:
        make_outpost_chance = randint(1, 20)
        if make_outpost_chance < 3:
            available_tiles[pos] = Outpost(outpost_sprite, pos, randint(40, 50))
            available_tiles[pos].draw(screen)
        else:   
            mountains_positions.add(pos)
            mountains_sprites.add(Mountain(mountain_sprite, pos))


# Available positions are all tiles in the grid that are not mountains.
available_positions = set([(x//TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE) 
                           for x in range(0, SCREEN_WIDTH, TILE_SIZE) 
                           for y in range(0, SCREEN_HEIGHT, 20)]) - mountains_positions

for pos in available_positions:
    available_tiles[pos] = available_tiles.get(pos, Tile(pos))


def draw_tiles(positions: iter):
    for position in positions:
        available_tiles[position].draw(screen)
    

def draw_grid():
    for i in range(N_TILES):
        # vertical line
        pygame.draw.line(screen, (10, 10, 10), (TILE_SIZE*i, 0), (TILE_SIZE*i, SCREEN_HEIGHT), TILE_BORDER_SIZE)
        # horizontal line
        pygame.draw.line(screen, (10, 10, 10), (0, TILE_SIZE*i), (SCREEN_WIDTH, TILE_SIZE*i), TILE_BORDER_SIZE)


def select_next_tile(current_tile_pos, direction):
    # Choose the desired tile as long as it's not a mountain or beyond the grid boundaries.
    tile_to_choose_pos = current_tile_pos
    if direction != (0, 0):
        tile_to_choose_pos = (current_tile_pos[0] + direction[0], current_tile_pos[1] + direction[1])
    return tile_to_choose_pos if tile_to_choose_pos in available_positions else current_tile_pos


def highlight_tile(tile_pos: tuple):
    draw_grid()
    highlight_pos = (tile_pos[0]+1, tile_pos[1]+1)
    pygame.draw.rect(screen, (220, 220, 220), (*highlight_pos, TILE_SIZE, TILE_SIZE), 2)


player1 = Player(base_sprite, get_random_location(available_positions), "#2792FF")

# Draw mountains and grid

for spr in mountains_sprites:
    spr.draw(screen)
player1.draw_tiles(screen)
draw_grid()
available_tiles[player1.base].player = player1
available_tiles[player1.base].soldiers = 1
player1.tiles[player1.base] = available_tiles[player1.base]
screen.blit(player1.image, player1.rect)


def main():
    curr_chosen_tile_pos = player1.base
    queue = []

    # Debouncing input and tile-moving and other cooldown variables.
    last_press_time = 0
    last_move_time = 0
    last_regenerate_time = 0
    last_regenerate_all_time = 0
    cooldown_select = 50
    cooldown_move = 500
    cooldown_regenerate = 1000
    cooldown_regenerate_all = 20000
    

    # game loop
    running = True
    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                row = y // TILE_SIZE * TILE_SIZE
                col = x // TILE_SIZE * TILE_SIZE
                if (col, row) in available_tiles:
                    tile_to_highlight = select_next_tile((col, row), (0, 0))
                    highlight_tile(tile_to_highlight)
                    prev_chosen_tile_pos = curr_chosen_tile_pos = tile_to_highlight

            if event.type == pygame.KEYDOWN:
                if current_time - last_press_time > cooldown_select and event.key in inputs.keys():
                    prev_chosen_tile_pos = curr_chosen_tile_pos
                    direction = inputs[event.key]
                    curr_chosen_tile_pos = select_next_tile(curr_chosen_tile_pos, direction)
                    if prev_chosen_tile_pos != curr_chosen_tile_pos:
                        highlight_tile(curr_chosen_tile_pos)
                        queue.append((curr_chosen_tile_pos, prev_chosen_tile_pos))  # add this tile to the queue for tiles to conquer
                    last_press_time = current_time
                
                # Clear queue to stop conquering tiles
                if event.key == pygame.K_q:
                    queue.clear()

        if queue and current_time - last_move_time > cooldown_move:
            tile_to_conquer_pos, prev_tile_pos = queue.pop(0)
            if tile_to_conquer_pos not in player1.tiles and prev_tile_pos not in player1.tiles:
                queue.clear()

            elif player1.tiles.get(prev_tile_pos, None):
                if player1.move(available_tiles[prev_tile_pos], available_tiles[tile_to_conquer_pos]):
                    draw_tiles([tile_to_conquer_pos, prev_tile_pos])
            
            last_move_time = current_time
        
        
        if current_time - last_regenerate_time > cooldown_regenerate:
            player1.regenerate_bases()
            last_regenerate_time = current_time
        
        if current_time - last_regenerate_all_time > cooldown_regenerate_all:
            player1.regenerate_all()
            player1.draw_tiles(screen)

            last_regenerate_all_time = current_time
    
        draw_tiles([*player1.outposts.keys(), player1.base])
        draw_grid()
        highlight_tile(curr_chosen_tile_pos)

        pygame.display.update()

main()
