# enemy.py
import pygame
import random
import time
from typing import NoReturn, List, Tuple
# from pathfinding.core.diagonal_movement import DiagonalMovement
# from pathfinding.core.grid              import Grid
# from pathfinding.finder.a_star          import AStarFinder
from experimental.pathfinding import a_star_alt


p      = 'assets/'
ENEMY1 = pygame.image.load(p+'enemy2.png')


def update_walkable(func):
    def wrapper(self, *args, **kwargs):
        self.set_walkable(1)
        rv = func(self, *args, **kwargs)
        self.set_walkable(0)
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
        self.interval = random.randint(1, 4) / 5
        self.steps    = {'n': self.step_n, 'e': self.step_e,
                         's': self.step_s, 'w': self.step_w,
                         '' : self.null}
        self.player = None  # set when near player
        self.level  = lvl
        # self.grid   = Grid(matrix=self.level)
        # self.finder = AStarFinder(diagonal_movement=0)
        self.clock  = time.time()
        self.path   = []
        self.idle   = False
        self.face   = None

    def __repr__(self) -> str:
        return f"<Enemy {self.ptr[0], self.ptr[1]}, {self.y+self.yos, self.x+self.xos}>"

    def null(self, *args, **kwargs) -> NoReturn:
        pass

    """ Set methods for direction and walkable """

    def set_direction(self, face: str) -> NoReturn:
        self.face = face

    def set_walkable(self, state: bool) -> NoReturn:
        self.level[self.ptr[0]][self.ptr[1]] = state

    """ Step methods for horizontal and vertical directions """

    @update_walkable
    def step_n(self) -> NoReturn:
        self.ptr[0] -= 1  # decrement y
        if (len(self.path) > 0): del self.path[0]

    @update_walkable
    def step_e(self) -> NoReturn:
        self.ptr[1] += 1  # increment x
        if (len(self.path) > 0): del self.path[0]

    @update_walkable
    def step_s(self) -> NoReturn:
        self.ptr[0] += 1  # increment y
        if (len(self.path) > 0): del self.path[0]

    @update_walkable
    def step_w(self) -> NoReturn:
        self.ptr[1] -= 1  # decrement x
        if (len(self.path) > 0): del self.path[0]

    """ Methods for movement, check_tile, idle_movement, pathfind, ... """

    def check_tile(self) -> NoReturn:
        tiles = {'n': self.level[self.ptr[0]-1][self.ptr[1]],
                 'e': self.level[self.ptr[0]][self.ptr[1]+1],
                 's': self.level[self.ptr[0]+1][self.ptr[1]],
                 'w': self.level[self.ptr[0]][self.ptr[1]-1]}
        if (not tiles.get(self.face)): self.face = ''

    def movement_behaviour(self) -> NoReturn:
        # # If there is 'no' player in sight: ...
        # if (self.player == None):
        #     if(time.time() > self.clock + (self.interval * 2)):
        #         self.set_direction(self.faces.get(random.randint(0,3)))
        #         self.clock = time.time()
        #         self.check_tile()
        #         self.steps.get(self.face)()
        # # If there 'is a' player in sight: ...
        # elif (self.player != None):
        #     if (self.path == []):  # Calculate + init. path
        #         self.path = self.pathfind()
        #         if (len(self.path) > 0): del self.path[0]
        #     if (time.time() > self.clock + self.interval) and (len(self.path) > 0):  # Step for each interval
        #         self.clock = time.time()
        #         if   (self.ptr[1] - self.path[0][0] == 1) : self.set_direction('w')
        #         elif (self.ptr[1] - self.path[0][0] == -1): self.set_direction('e')
        #         elif (self.ptr[0] - self.path[0][1] == 1) : self.set_direction('n')
        #         elif (self.ptr[0] - self.path[0][1] == -1): self.set_direction('s')
        #         self.check_tile()
        #         self.steps.get(self.face)()
        # # handle x-axis movement | x = matrix_ptr_x, vx = visual_x_coordinate
        # if ((x:=self.ptr[1]) != (vx:=int((self.xos + self.x)) / 80)):
        #     if   (x > vx): self.xos += 4
        #     elif (x < vx): self.xos -= 4
        # # handle y-axis movement | y = matrix_ptr_y, vy = visual_y_coordinate
        # if ((y:=self.ptr[0]) != (vy:=int((self.yos + self.y)) / 80)):
        #     if   (y > vy): self.yos += 4
        #     elif (y < vy): self.yos -= 4
        pass

    def pathfind(self): # -> List[Tuple[int, int]]:
        # '''
        #     Returns list of coordinates from enemy to player
        # '''
        # self.grid.cleanup()  # Resets <Grid Object> for recalculation (necessary)
        # start     = self.grid.node(self.ptr[1], self.ptr[0])
        # end       = self.grid.node(self.player.x, self.player.y)
        # path, run = self.finder.find_path(start, end, self.grid)
        # return path
        return None

    def pathfind_alt(self):
        if self.player is not None:
            if time.time() > self.clock + self.interval:
            #     if (self.path == []):  # Calculate + init. path
            #         self.path = self.pathfind()
            #         if (len(self.path) > 0): del self.path[0]
            #     if (time.time() > self.clock + self.interval) and (len(self.path) > 0):  # Step for each interval
                self.clock = time.time()
                start = (self.ptr[0], self.ptr[1])
                end = (self.player.x, self.player.y)
                path = a_star_alt.astar(self.level, start, end)
                print(path)

    """ Health methods and main draw (render) method """

    def draw_health(self, screen: pygame.surface, xos: int, yos: int) -> NoReturn:
        x = self.x + self.xos + xos + 10
        y = self.y + self.yos + yos + 8
        w = int((self.hp/self.mhp) * 100 * 0.6)               # width
        pygame.draw.rect(screen, (200, 0, 0), [x, y, 60, 8])  # red background bar
        pygame.draw.rect(screen, (0, 200, 0), [x, y, w, 8])   # green health bar

    def check_health(self):
        '''
            Pseudo death function
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
        # self.movement_behaviour()
        self.pathfind_alt()
        self.draw_health(screen, xos, yos)
        self.check_health()

        
def main():
    pass

    
if __name__=='__main__':
    main()
   
