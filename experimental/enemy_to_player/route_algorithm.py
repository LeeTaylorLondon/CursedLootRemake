import time
import random
import pathfinding as path
from math import inf
from typing import List, NoReturn, Tuple, Dict


class PseudoPlayer:
    def __init__(self, lvl_ref, x=13, y=13, random_point=False):
        # x, y ptr coordinates in level
        self.x = x
        self.y = y
        # randomise x, y values
        self.r = random_point
        self.random_pos()
        # pathfinding attrs
        self.lvl_ref    = lvl_ref
        self.level_repr = self.init_level_repr()

    def __repr__(self):
        return f"<PseudoPlayer pos={self.x,self.y}>"

    def init_level_repr(self):
        rv = self.lvl_ref.copy()
        # rv[self.y][self.x] = 0
        

    def random_pos(self):
        # Randomises starting position => self.x, self.y : random.randint(...)
        if (self.r):
            raise NotImplemented


def read() -> List[List[str]]:
    '''
        Reads text file storing the level as characters
        :return: text file contents as a matrix of chars
    '''
    rv = []
    with open('level1.txt', 'r') as f: contents = f.read()
    for line in contents.split('\n') : rv.append(line)
    del rv[len(rv)-1]
    return rv

def return_boolean_matrix(level: List[List[str]]):
    '''
        Converts level data from a matrix of chars to booleans
        :return: matrix of booleans representing which tiles are walkable
    '''
    rv = []
    for line in level:
        arr = []
        for char in line:
            if   (char == '0') or (char == '2'): arr.append(0)
            elif (char == '1') or (char == '3'): arr.append(1)
        rv.append(arr)
    return rv


def main():
    bools = return_boolean_matrix(read())
    p = PseudoPlayer(lvl_ref=bools)

if __name__ == '__main__':
    # imports
    from pathfinding.core.diagonal_movement import DiagonalMovement
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    # init level as bools, grid, start, end, finder
    bools = return_boolean_matrix(read())
    grid  = Grid(matrix=bools)
    start = grid.node(13, 13)
    end   = grid.node(13, 15)
    finder= AStarFinder(diagonal_movement=0)
    # calc path
    path = finder.find_path(start, end, grid)
    print(path)
    grid  = Grid(matrix=bools)
    start = grid.node(13, 13)
    end   = grid.node(13, 15)
    path  = finder.find_path(start, end, grid)
    print(path)
    
    




    
