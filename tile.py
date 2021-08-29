import pygame
from typing import List, NoReturn

# image assets
p           = 'assets/'
VOIDTILE2   = pygame.image.load(p+'VoidTile2.png')
GROUNDTILE1 = pygame.image.load(p+'groundTile4.png')
WALLTILE1   = pygame.image.load(p+'wallTile1.png')
LADDERTILE  = pygame.image.load(p+'ladder.png')

class Tile:
    def __init__(self, image, x, y, category=None):
        self.image      = image
        self.walkable   = True
        self.category   = category
        self.x          = x
        self.y          = y
            
    def draw(self, screen, xos, yos):
        """ Render tile object using pygame.blit... """
        screen.blit(screen, self.image, (self.x + xos, self.y + yos))

    def __repr__(self):
        # Tile xy={self.x,self.y}, 
        return f"<Tile, {self.x}, {self.y}, {self.walkable}>"

def void_tile_obj():
    return Tile(VOIDTILE2, None, None)

def wall_tile_obj():
    return Tile(WALLTILE1, None, None)

def ground_tile_obj():
    return Tile(GROUNDTILE1, None, None)

def level_repr(matrix: List[List[Tile]]) -> NoReturn:
    for vector in matrix:
        print(vector)


        
