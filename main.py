import pygame
from random import randint
from Components import *
from constants import *
from Utils import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("Generals")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("#DCDCDC")
font = pygame.font.SysFont('Consolas', 18)
clock = pygame.time.Clock()

inputs = {pygame.K_UP: (0, -TILE_SIZE), 
          pygame.K_DOWN: (0, TILE_SIZE),
          pygame.K_LEFT: (-TILE_SIZE, 0), 
          pygame.K_RIGHT: (TILE_SIZE, 0)
        }

# Load sprites
mountain_image = pygame.image.load("assets/mountain.png").convert_alpha()
mountain_image = pygame.transform.scale(mountain_image, (TILE_SIZE, TILE_SIZE))
base_image = pygame.image.load("assets/base.png").convert_alpha()
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

def draw_tiles(positions: iter):
    for position in positions:
        col, row = position
        topleft = (col+TILE_BORDER_SIZE, row+TILE_BORDER_SIZE)
        if tiles[position] != player1.base:
            pygame.draw.rect(screen, "#2792FF", (*topleft, TILE_BODY_SIZE, TILE_BODY_SIZE))

def draw_grid():
    for i in range(N_TILES):
        # vertical line
        pygame.draw.line(screen, (10, 10, 10), (TILE_SIZE*i, 0), (TILE_SIZE*i, SCREEN_HEIGHT), TILE_BORDER_SIZE)
        # horizontal line
        pygame.draw.line(screen, (10, 10, 10), (0, TILE_SIZE*i), (SCREEN_WIDTH, TILE_SIZE*i), TILE_BORDER_SIZE)


def select_next_tile(current_tile_pos, direction):
    # Choose the desired tile as long as it's not a mountain or beyond the grid boundaries.
    tile_to_choose_pos = (current_tile_pos[0] + direction[0], current_tile_pos[1] + direction[1])
    tile_to_choose = tiles.get(tile_to_choose_pos, None)
    
    return tile_to_choose.pos if tile_to_choose else current_tile_pos


def highlight_tile(tile_pos: tuple):
    draw_grid()
    highlight_pos = (tile_pos[0]+1, tile_pos[1]+1)
    pygame.draw.rect(screen, (220, 220, 220), (*highlight_pos, TILE_SIZE, TILE_SIZE), 2)



# Players
tiles = {}

# keep track of information for available tiles
for pos in available_positions:
    tiles[pos] = Tile(pos)


# Draw mountains and grid
mountains_sprites.draw(screen) 
draw_grid()
draw_tiles(positions)

player1 = Player(base_image, get_random_location(available_positions), "#2792FF")
tiles[player1.base].player = player1
tiles[player1.base].soldiers = 2
player1.tiles.add(tiles[player1.base])
screen.blit(player1.image, player1.rect)


# text_surface = font.render(str("tst"), True, (255, 255, 255))
# text_surface_rect = text_surface.get_rect(center=(player1.rect[0]+ TILE_SIZE // 2, player1.rect[1] + TILE_SIZE // 2))

def main():
    curr_chosen_tile_pos = player1.base
    queue = []

    # Debouncing input and tile-moving and other cooldown variables.
    last_press_time = 0
    last_move_time = 0
    last_regenerate_time = 0
    last_regenerate_all_time = 0
    cooldown_select = 150
    cooldown_move = 500
    cooldown_regenerate = 1000
    last_regenerate_all_time = 20000
    

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
                pos = (col, row)
                if pos not in mountains_positions and pos != player1.rect.topleft:
                    draw_tiles([pos])
            
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

        if current_time - last_move_time > cooldown_move:
            if queue:
                tile_to_conquer_pos, prev_tile_pos = queue.pop(0)
                if tiles[prev_chosen_tile_pos].player == player1:
                    if player1.move(tiles[prev_tile_pos], tiles[tile_to_conquer_pos]):
                        # print("Tile to conquer: " + str(tiles[tile_to_conquer_pos]))
                        # print("Tile was on: " + str(tiles[player1.base]))
                        # print()
                        draw_tiles([tile_to_conquer_pos])
            
            last_move_time = current_time
        
        if current_time - last_regenerate_time > cooldown_regenerate:
            tiles[player1.base].soldiers += 1
            cooldown_regenerate = current_time
    
        pygame.display.update()

main()
