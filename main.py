import pygame
import colors
import enemy
import random
import time
import level_gen  as lg2  # lg2 -> 'level gen v2' -- Level gen needed rewrite
import inventory  as inv
from item   import Item
from enemy  import Enemy
from tile   import Tile
from typing import List, Tuple, Dict, NoReturn

p = 'assets/'

def null(*args, **kwargs):
    '''
        Used in handling player movement
    '''
    pass

def set_walkable(self, state: bool) -> NoReturn:
    '''
        Sets the walkable attr. of a tile to the passed state (T || F)
    '''
    self.bools[self.player.y][self.player.x] = state

def update_game_data(func):
    '''
        Prevents <enemy(s)> and the <player> from standing on the same tile.
        Sets the tile the player, was on, to <walkable> and the tile the
        player is, now on, to <not-walkable>

        On key press this function deletes a path that is stored within the enemy.
        A path from the enemy to the player - causing a recalculation of such a path
    '''
    def wrapper(self, *args, **kwargs):
        # for e in self.enemies.values(): e.path = []
        set_walkable(self, 1)
        rv = func(self, *args, **kwargs)
        set_walkable(self, 0)
        return rv
    return wrapper


class Player:
    def __init__(self):
        self.y   = 13
        self.x   = 13
        self.img = pygame.image.load(p+'player3.png').convert_alpha()
        self.mhp = 300  # 'mhp' -> max-hit-points
        self.hp  = 300  # 'hp'  -> hit-points
        # Combat data
        self.dmg   = 0
        self.defen = 0
        self.dex   = 0
        self.lck   = 0
        self.e     = None  # e: ptr => <enemy> in combat with player
        # inventory => (wep: weapon, arm: armour, nek: necklace, rng: ring)
        self.inv = inv.Inventory()

    """ Draw-methods -> player-model, health-bar, ... """
    
    def draw_model(self, screen):
        screen.blit(self.img, (400, 240))

    def draw_health(self, screen):
        red_width = int((self.hp/self.mhp)*720)  # red_width = 720
        pygame.draw.rect(screen, (25, 25, 25), [75, 475, 730, 30])
        pygame.draw.rect(screen, (200, 0, 0),  [80, 480, red_width, 20])

    def draw(self, screen):
        self.draw_health(screen)
        self.draw_model(screen)

    """ Combat method """
    
    def combat(self, hit: bool) -> NoReturn:
        if(hit):
            if(time.time() > self.hit + 0.5):
                self.e.hp     -= self.dmg
                self.hit       = time.time()
        else: self.hit = time.time()

    def pickup_item(self, items: Dict[Tuple, Item]) -> NoReturn:  # tuple(x, y) => ptr
        if ((itm := items.get((self.x, self.y))) == None): return
        del items[(self.x, self.y)]
        self.inv.add_item(itm)


class Scene:
    CURRENT_LEVEL_INT = 1
    CURRENT_LEVEL_STR = f"levels/level{str(CURRENT_LEVEL_INT)}.txt"
    
    def __init__(self):
        # Pygame values
        pygame.init()
        pygame.display.set_caption('FREEDOM.exe')
        self.display_w = 880
        self.display_h = 560
        self.screen    = pygame.display.set_mode((self.display_w, self.display_h))
        self.clock     = pygame.time.Clock()
        # Image assets
        self.back_ground = pygame.image.load(p+'background.png').convert()
        self.x_offset    = -640  # 'explanation' -> -640
        self.y_offset    = -800  # 'explanation' -> -800
        self.y_dir       = ''    # dir -> direction
        self.x_dir       = ''
        # Level data, level is stored as booleans and tiles
        self.bools   = lg2.load_level_bools(lg2.read_level(self.CURRENT_LEVEL_STR))
        self.tiles   = lg2.load_level_tiles(lg2.read_level(self.CURRENT_LEVEL_STR))
        
        # WIP - replace w/ automation {
        self.bools[13][13] = 1
        self.tiles[6].category = 'ladder_down'
        x, y, t, = self.init_ladder()
        # WIP - replace w/ automation }
        
        self.ladders = {(x, y): t}
        self.items   = None  # self.init_items()
        # Entities
        self.player  = Player()
        self.player.inv.player = self.player
        self.enemies = self.init_enemies_dev()
        self.items   = {}
        self.init_items_dev()
        self.combat  = False
        # Keyboard data
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.move_down  = {True: {True: self.move_south, False: self.handle_combat},
                          False: {False: null, True: null}}
        self.move_up    = {True: {True: self.move_north, False: self.handle_combat},
                          False: {False: null, True: null}}
        self.move_right = {True: {True: self.move_east, False: self.handle_combat},
                          False: {False: null, True: null}}
        self.move_left  = {True: {True: self.move_west, False: self.handle_combat},
                          False: {False: null, True: null}}
        # Render scene method
        self.render()

    """ initialization methods for: ladder, items, enemies, ... """

    def init_ladder(self) -> Tuple[int, int, Tile]:
        '''
            Performs a linear search for Tile object w/ specific attr
            :return: Tuple -> x: int, y: int (matrix_ptr), tile object : Tile 
        '''
        for tile in self.tiles:
            if (tile.category == 'ladder_down'):
                return int(tile.x/80), int(tile.y/80), tile

    def init_items_dev(self) -> NoReturn:
        '''
            Populates self.items dict with random items
        '''
        for i in range(10):
            item = Item()
            item.id = i
            rt   = self.tiles[random.randint(0, len(self.tiles) - 1)]
            while (rt.walkable == False):
                rt = self.tiles[random.randint(0, len(self.tiles))]
            item.gro_x, item.gro_y = rt.x + 15, rt.y + 15
            self.items.update({(int(item.gro_x / 80), int(item.gro_y / 80)) : item})

    def init_enemies_dev(self) -> Dict[Tuple[int, int], Enemy]:
        '''
            Returns hashmap of enemies and their locations in the level

            Rewrite: Optimize to remove 'random-loop' -> While True: ...
        '''
        rv = {}
        quan_enemies = 1 #random.randint(25, 26)  # random quantity of enemies
        for i in range(quan_enemies):
            while True:
                ri = random.randint(1, len(self.tiles)-2)
                rt = self.tiles[ri]                      # rt: random tile
                if (rt.walkable) and ((rt.x, rt.y) not in rv): # walkable not in use
                    e     = Enemy(rt.x, rt.y, self.bools)# Construct enemy
                    e.ptr = [int(e.y/80), int(e.x/80)]   # Init enemy ptr
                    e.image.convert_alpha()              # Run CA to reduce lag
                    e.player = self.player               # REPLACE: w/ player in range(enemy): e.player = self.player
                    self.bools[e.ptr[0]][e.ptr[1]] = 0   # Solidify it's tile
                    rv.update({tuple(e.ptr): e})         # Add enemy to return-value
                    break                                # Move onto next Enemy
        if(rv.get((self.player.y, self.player.x))!=None):# Prevents <enemy> on <player>
            del rv[(self.player.y, self.player.x)]
        return rv

    """ draw-methods -> background, tiles, enemies, ... """
    
    def draw_background(self) -> NoReturn:
        self.screen.blit(self.back_ground,(-240 + self.x_offset, -240 + self.y_offset))

    def draw_tiles(self) -> NoReturn:
        for t in self.tiles:
            self.screen.blit(t.image, (t.x + self.x_offset, t.y + self.y_offset))

    def draw_enemies(self) -> NoReturn:
        for enemy in list(self.enemies.values()): enemy.draw(self.screen, self.x_offset,
                                                             self.y_offset, self.bools)

    def draw_items(self) -> NoReturn:
        for item in self.items.values():
            self.screen.blit(item.img, (item.gro_x + self.x_offset,
                                        item.gro_y + self.y_offset))

    """ handle-methods -> input, scrolling-background, ... """

    def handle_level_load(self) -> NoReturn:
        '''
            Load level tiles and booleans used to change levels 
        '''
        self.bools, self.tiles = None, None
        self.CURRENT_LEVEL_STR = f"levels/level{str(self.CURRENT_LEVEL_INT)}.txt"
        self.bools = lg2.load_level_bools(lg2.read_level(self.CURRENT_LEVEL_STR))
        self.tiles = lg2.load_level_tiles(lg2.read_level(self.CURRENT_LEVEL_STR))
    
    def handle_input(self) -> NoReturn:
        self.move_down.get(self.s).get(
        	self.bools[self.player.y+1][self.player.x])(1, 0)
        self.move_up.get(self.w).get(
        	self.bools[self.player.y-1][self.player.x])(-1, 0)
        self.move_right.get(self.d).get(
        	self.bools[self.player.y][self.player.x+1])(0, 1)
        self.move_left.get(self.a).get(
        	self.bools[self.player.y][self.player.x-1])(0, -1)

    @update_game_data
    def move_north(self, *args):
        if(self.y_dir == ''):
            self.player.y -= 1
            self.y_offset += 4
            self.y_dir = 'n'

    @update_game_data
    def move_south(self, *args):
        if(self.y_dir == ''):
            self.player.y += 1
            self.y_offset -= 4
            self.y_dir = 's'

    @update_game_data
    def move_east(self, *args):
        if(self.x_dir == ''):
            self.player.x += 1
            self.x_offset -= 4
            self.x_dir = 'e'

    @update_game_data
    def move_west(self, *args):
        if(self.x_dir == ''):
            self.player.x -= 1
            self.x_offset += 4
            self.x_dir = 'w'

    def handle_scrolling_background(self):
        # x-axis
        if  (self.x_offset % 80 != 0 and self.x_dir == 'e'): self.x_offset -= 4
        elif(self.x_offset % 80 != 0 and self.x_dir == 'w'): self.x_offset += 4
        else:self.x_dir = ''
        # y-axis
        if  (self.y_offset % 80 != 0 and self.y_dir == 'n'): self.y_offset += 4
        elif(self.y_offset % 80 != 0 and self.y_dir == 's'): self.y_offset -= 4
        else:self.y_dir = ''

    def handle_tracking_enemies(self) -> NoReturn:
        '''
            Dict stores { <enemy.ptr>: <enemy>, ... }
            self.draw_enemies() draws from this dict's values 

           #PATCH: If two enemy possess the same key then one enemy will
                   naturally be deleted - pop out of existence
        '''
        self.enemies = {tuple(e.ptr): e for e in list(self.enemies.values())}

    def handle_combat(self, yval: int, xval: int) -> NoReturn:
        '''
            Sets attr: bool -> combat: True

            Stores the <Enemy> the <Player> is colliding with, within <Player>
        '''
        if((e:=self.enemies.get((self.player.y+yval, self.player.x+xval)))!=None):
            self.combat        = True
            self.player.e      = e

    def handle_cancel_combat(self) -> NoReturn:
        '''
            Sets attr 'combat': bool => False

            The <Enemy> the <Player> is colliding with, stored within <Player>
            is deleted.
        '''
        if(self.combat):
            self.combat        = False  # combat is no longer true
            self.player.e      = None   # del. enemy stored in player

    def handle_ladder_use(self):
        '''
            Method used to interact with ladders going up and down
            TODO: <read comments>
        '''
        if ((gt:=self.ladders.get((self.player.x, self.player.y))) != None):
            if (gt.category == 'ladder_down'):
                self.CURRENT_LEVEL_INT += 1
                # insert transition screen >here<
                self.handle_level_load()
            elif (gt.category == 'ladder_up'):
                self.CURRENT_LEVEL_INT -= 1
                # insert transition screen >here<
                self.handle_level_load()
        else: return

    def handle_enemy_vision(self):
        for x, y in self.enemies.keys():
            if (abs(self.player.x - x) <= 6) and (abs(self.player.y - y) <= 6):
                self.enemies.get((x, y)).player = self.player
            else:
                self.enemies.get((x, y)).player = None

    def on_press_e(self):
        # pickup item || use ladder (traverse to next/prev level)
        self.player.pickup_item(self.items)
        self.handle_ladder_use()

    def render(self):
        running = True
        while running:
            # events = key-pressed, key-released
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # R : <print: debug-info>
                    if event.key == pygame.K_r:
                        e = list(self.enemies.values())[0]
                        print(f"<player.ptr = {self.player.y, self.player.x}>")
                        print(f"<enemy_data = {self.enemies}>")
                        print(f"<enemy_d_xy = {e.x, e.y}>")
                        print(f"<enemy_d_os = {e.xos, e.yos}>")
                        print(f"<enemy_pptr = {e.player}>")
                        print(f"<enemy_path = {e.path}>")
                        print(f"<fps        = {self.clock.get_fps()}>")
                        print()
                    # E: Use  F: Open-Inv  Q: Quit
                    # W: Up   S: Down      A: Left  D: Right 
                    if event.key == pygame.K_e: self.on_press_e()
                    if event.key == pygame.K_f: self.player.inv.enable = True
                    if event.key == pygame.K_q: running = False
                    if event.key == pygame.K_w:
                        self.w = True
                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_s:
                        self.s = True
                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_a:
                        self.a = True
                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_d:
                        self.d = True
                        for e in self.enemies.values(): e.path = []
                # Key-released listener
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.w = False
                        self.handle_cancel_combat()
##                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_s:
                        self.s = False
                        self.handle_cancel_combat()
##                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_d:
                        self.d = False
                        self.handle_cancel_combat()
##                        for e in self.enemies.values(): e.path = []
                    if event.key == pygame.K_a:
                        self.a = False
                        self.handle_cancel_combat()
##                        for e in self.enemies.values(): e.path = []
            self.screen.fill(colors.white)
            # Draw & Handle objects <start>
            self.draw_background()
            self.draw_tiles()
            self.draw_items()
            self.draw_enemies()
            self.player.draw(self.screen)
            self.handle_input()
            self.handle_scrolling_background()
            self.handle_tracking_enemies()
            self.handle_enemy_vision()
            self.player.combat(self.combat)
            self.player.inv.handle_inventory(self.screen, self.clock)
            # Draw & Handle objects <end>
            pygame.display.update()
            self.clock.tick(144)
        pygame.quit()


def main():
    Scene()
    

if __name__ == '__main__':
    main()
