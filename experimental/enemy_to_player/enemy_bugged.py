# enemy.py
import pygame
import random
import time
from typing import NoReturn, List
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid              import Grid
from pathfinding.finder.a_star          import AStarFinder


p      = 'assets/'
ENEMY1 = pygame.image.load(p+'enemy2.png')


def update_walkable(func):
    def wrapper(self, *args, **kwargs):
        self.set_walkable(True)
        rv = func(self, *args, **kwargs)
        self.set_walkable(False)
        return rv
    return wrapper


class Enemy:
    faces = {0: 'n', 1: 'e', 2: 's', 3: 'w'}

    def __init__(self, x: int, y: int, lvl: List[List[bool]]) -> NoReturn:
        self.mhp = 10  # mhp -> maximum health points (increases w/ level)
        self.hp  = 10  # hp  -> health points
        # Rendering
        self.image = ENEMY1
        self.x     = x
        self.y     = y
        self.xos   = 0
        self.yos   = 0
        self.ptr   = None  # [y, x] ptrs to level (matrix)
        # Movement
        self.interval = random.random() + 0.5 # random.randint(1, 2)
        self.steps    = {'n': self.step_n, 'e': self.step_e,
                         's': self.step_s, 'w': self.step_w,
                         '' : self.null}
        self.player = None  # set when near player
        self.level  = lvl
        self.grid   = Grid(matrix=self.level)
        self.finder = AStarFinder(diagonal_movement=0)
        self.clock  = time.time()
        self.path   = None
        self.idle   = False
        self.face   = None

    def __repr__(self) -> str:
        return f"<Enemy {self.ptr[0], self.ptr[1]}, {self.y+self.yos, self.x+self.xos}>"

    def null(self, *args, **kwargs) -> NoReturn:
        pass

    def set_walkable(self, state: bool) -> NoReturn:
        self.level[self.ptr[0]][self.ptr[1]] = state

    @update_walkable
    def step_n(self) -> NoReturn:
        self.yos    -= 2
        self.ptr[0] -= 1  # decrement y

    @update_walkable
    def step_e(self) -> NoReturn:
        self.xos    += 2
        self.ptr[1] += 1  # increment x

    @update_walkable
    def step_s(self) -> NoReturn:
        self.yos    += 2
        self.ptr[0] += 1  # increment y

    @update_walkable
    def step_w(self) -> NoReturn:
        self.xos    -= 2
        self.ptr[1] -= 1  # decrement x

    def set_direction(self, face: str) -> NoReturn:
        self.face = face

    def check_tile(self, level: List[List[bool]]) -> NoReturn:
        # n, e, s, w
        tiles = {
                 'n': level[self.ptr[0]-1][self.ptr[1]],
                 'e': level[self.ptr[0]][self.ptr[1]+1],
                 's': level[self.ptr[0]+1][self.ptr[1]],
                 'w': level[self.ptr[0]][self.ptr[1]-1]
                 }
        if (not tiles.get(self.face)): self.face = ''

    def idle_movement(self, level: List[List[bool]]) -> NoReturn:
        # every ~2 seconds movement might occur (will miss a move if direction @ wall)
        if (self.idle):
            if(time.time() > self.clock + self.interval):
                self.set_direction(self.faces.get(random.randint(0,3)))
                self.clock = time.time()
                self.check_tile(level)
                self.steps.get(self.face)()
        # Tracking player behaviour
        if (not self.idle):
            if (self.path == None) and (self.player != None):
                try:
                    self.path = self.pathfind()
                except ValueError:
                    return
            if (time.time() > self.clock + self.interval) and (self.path != None):
                self.clock = time.time()
                try:
                    if   (self.ptr[1] - self.path[1][0] > 0): self.set_direction('w')
                    elif (self.ptr[1] - self.path[1][0] < 0): self.set_direction('e')
                    elif (self.ptr[0] - self.path[1][1] > 0): self.set_direction('n')
                    elif (self.ptr[0] - self.path[1][1] < 0): self.set_direction('s')
                except IndexError:
                    return
                del self.path[1]
                self.check_tile(level)
                self.steps.get(self.face)()
            else:
                self.path = None
                self.idle = True
        # handle x-axis movement
        if (self.xos % 80):
            if   (self.face == 'e'): self.xos += 2
            elif (self.face == 'w'): self.xos -= 2
        # handle y-axis movement
        if (self.yos % 80):
            if   (self.face == 's'): self.yos += 2
            elif (self.face == 'n'): self.yos -= 2

    def pathfind(self):
        start = self.grid.node(self.ptr[1], self.ptr[0])
        end   = self.grid.node(self.player.x + 1, self.player.y)
        path, run = self.finder.find_path(start, end, self.grid)
        return path

    def draw_health(self, screen: pygame.surface, xos: int, yos: int) -> NoReturn:
        x = self.x + self.xos + xos + 10
        y = self.y + self.yos + yos + 8
        w = int((self.hp/self.mhp) * 100 * 0.6)               # width
        pygame.draw.rect(screen, (200, 0, 0), [x, y, 60, 8])  # red background bar
        pygame.draw.rect(screen, (0, 200, 0), [x, y, w, 8])   # green health bar

    def check_health(self):
        '''
            pseudo death function
        '''
        if(self.hp <= 0):
            self.set_walkable(True)
            self.draw = self.null
            self.ptr  = [1, 1]

    def draw(self, screen: pygame.surface, xos: int, yos: int, level: List[List[bool]]):
        '''
            (renders) Blit's image of enemy to screen, calls func idle-movement
        '''
        screen.blit(self.image, (self.x + self.xos + xos,
                                 self.y + self.yos + yos))
        self.idle_movement(self.level)
        self.draw_health(screen, xos, yos)
        self.check_health()

        
def main():
    pass

    
if __name__=='__main__':
    main()
   
