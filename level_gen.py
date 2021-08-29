import random
import numpy as np
import tile
from tile import Tile
from typing import NoReturn, List


def write_level(level, file_name) -> NoReturn:
    ''' Writes matrix of 1's and 0's to specified text file '''
    formatted = ''
    for arr in level:
        for n in arr:
            formatted = formatted + str(n)
        formatted = formatted + '\n'
    with open(file_name, 'w') as f:
        f.write(formatted)

def read_level(file_name):
    ''' Returns string of text file contents '''
    with open(file_name, 'r') as f:
        rv = str(f.read())
    rv = rv.split('\n')
    for i,v in enumerate(rv): rv[i] = list(v)
    return rv


class Room:
    def __init__(self):
        # init height, width, x, and y 
        self.height  = random.randint(5, 9)
        self.width   = random.randint(5, 9)
        self.x       = -1
        self.y       = -1
        # tl, tr, bl, br -> top left, top right, bottom left, bottom right
        self.tl      = (self.y, self.x)
        self.tr      = (self.y, self.x + self.width - 1)
        self.bl      = (self.y + self.height - 1, self.x)
        self.br      = (self.y + self.height - 1, self.x + self.width - 1)
        self.points  = [self.tl, self.tr, self.bl, self.br]
        # faces data, None = no connecting room
        self.face_ints  = {1: 'n', 2: 'e', 3: 's', 4: 'w'}
        self.face_links = {'n': None, 'e': None, 's': None, 'w': None}

    def __repr__(self):
        return f"<Room {self.width}by{self.height} @ [{self.y}][{self.x}], {self.points}>"

    def update_points(self):
        ''' Update attributes containing coordinates of corners '''
        self.tl      = (self.y, self.x)
        self.tr      = (self.y, self.x + self.width - 1)
        self.bl      = (self.y + self.height - 1, self.x)
        self.br      = (self.y + self.height - 1, self.x + self.width - 1)
        self.points  = [self.tl, self.tr, self.bl, self.br]

    def gen_room_north(self, room, level: List[List[str]]) -> NoReturn:
        ''' Stiches a passed room to the 'north' face of itself (itself = room) '''
        room.y = self.y - room.height + 1
        room.x = random.randint(self.x, self.x + self.width - 3)
        room.update_points()
        room.write(level)
        upper_bound_x = min(room.bl[1], self.tr[1]) + 1  # pathway to room
        level[room.bl[0]][random.randint(room.bl[1] + 1, upper_bound_x)] = 1

    def gen_room_east(self, room, level: List[List[str]]) -> NoReturn:
        ''' Stiches a passed room to the 'east' face of itself (itself = room) '''
        room.y = random.randint(self.y, self.y + self.height - 3)
        room.x = self.x + self.width - 1
        room.update_points()
        room.write(level)
        y = random.randint(max(self.tr[0], room.tl[0]) + 1,
                           min(self.br[0], room.bl[0]) - 1)
        level[y][self.br[1]] = 1

    def gen_room_south(self, room, level: List[List[str]]) -> NoReturn:
        ''' Stiches a passed room to the 'south' face of itself (itself = room) '''
        room.y = self.br[0]
        room.x = self.br[1] - room.width
        room.update_points()
        room.write(level)
        x = random.randint(max(room.tr[1], self.bl[1]) - 1,
                           min(self.tr[1], self.br[1]) - 2)
        level[self.br[0]][x] = 1

    def gen_room_west(self, room, level: List[List[str]]) -> NoReturn:
        ''' Stiches a passed room to the 'west' face of itself (itself = room) '''
        if (room.height > self.height): room.y=self.y-abs(room.height-self.height)
        else: room.y = self.y
        room.x = self.x - room.width + 1
        room.update_points()
        room.write(level)
        x = self.bl[1]
        y = random.randint(self.y + 1, min(self.bl[0], room.bl[0]) - 1)
        level[y][x] = 1

    def write(self, level: List[List[str]]) -> NoReturn:
        ''' Given a matrix, itself the room is written to the
            level stored in the matrix.
        '''
        # overwrite area with a 'square' of 1's
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                level[y][x] = 1
        # top and bottom sides/lines of 'square' set to 2
        for x in range(self.x, self.x + self.width):
            level[self.y][x] = 2
            level[self.y + self.height - 1][x] = 2
        # left and right sides/lines of 'square' set to 2
        for y in range(self.y, self.y + self.height):
            level[y][self.x] = 2
            level[y][self.x + self.width - 1] = 2


STARTING_ROOM = Room()
STARTING_ROOM.x, STARTING_ROOM.y = 12, 12
STARTING_ROOM.update_points()


def gen_level_1() -> List[List[str]]:
    ''' Returns matrix of 0's, 1's, and 2's representing a level '''
    rv = np.zeros((30, 30), dtype=np.int8)
    STARTING_ROOM.write(rv)
    STARTING_ROOM.gen_room_north(Room(), rv)
    STARTING_ROOM.gen_room_east(Room(), rv)
    STARTING_ROOM.gen_room_south(Room(), rv)
    STARTING_ROOM.gen_room_west(Room(), rv)
    return rv

def load_level_tiles(level: List[List[str]]):
    ''' 
        Return -- vector of tiles
    '''
    vector = []
    x, y   = 0, -80
    for line in level:
        x  = 0
        y += 80
        for char in line:
            temp_tile = Tile(None, x, y)
            x += 80
            if   (char == '1'): temp_tile.image = tile.GROUNDTILE1
            elif (char == '2'): temp_tile.image, temp_tile.walkable = tile.WALLTILE1, False
            elif (char == '3'): temp_tile.image = tile.LADDERTILE
            elif (char == '0'): continue  # void tile
            vector.append(temp_tile)
    return vector

def load_level_bools(level: List[List[str]]):
    ''' Return -- matrix of bools '''
    matrix = level.copy()
    for y,arr in enumerate(matrix):
        for x,elm in enumerate(arr):
            # '1': Ground, '0': Void, '3': Ladder
            if   (elm == '1'): matrix[y][x] = 1
            elif (elm == '0'): matrix[y][x] = 0
            elif (elm == '3'): matrix[y][x] = 1
            else: matrix[y][x] = 0
    del matrix[len(matrix)-1]
    return matrix

def testing_enviroment():
    test_level = np.zeros((30, 30), dtype=np.int8)
    STARTING_ROOM.write(test_level)
    STARTING_ROOM.gen_room_north(Room(), test_level)
    STARTING_ROOM.gen_room_east(Room(), test_level)
    STARTING_ROOM.gen_room_south(Room(), test_level)
    STARTING_ROOM.gen_room_west(Room(), test_level)
    write_level(test_level, 'levels/level3.txt')
    print(test_level)

if __name__ == '__main__':
    testing_enviroment()






    
