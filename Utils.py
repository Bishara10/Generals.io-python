from constants import *
from random import randint, choice

def get_random_location(options: set=None):
    """ Returns a random location of a tile in the game grid. """
    
    if options:
        return choice(list(options))

    rand_x = randint(0, SCREEN_WIDTH)
    rand_y = randint(0, SCREEN_HEIGHT)
    col = rand_x // TILE_SIZE * TILE_SIZE
    row = rand_y // TILE_SIZE * TILE_SIZE
    
    return (col, row)