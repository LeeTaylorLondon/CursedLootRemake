import pygame
from item import Item
from item import gen_text_obj as Text
from typing import List, Tuple, Dict, NoReturn


class Inventory:
    def __init__(self, player=None, screen=None, clock=None):
        self.screen = screen
        self.clock  = clock
        self.enable = False
        self.player = player
        # self.points = {tuple(x, y) : <item-obj> || None}
        self.points = {(x, y): None for y in range(120, 320, 60)
                       for x in range(300, 760, 60)}
        self.locate = lambda x, y : (x - (x % 60), y - (y % 60))
        # player slots
        self.wep_slot = None
        self.arm_slot = None
        self.nek_slot = None
        self.rng_slot = None
        self.player_slots = {(120, 120): self.wep_slot, (120, 180): self.arm_slot,
                             (120, 240): self.nek_slot, (120, 300): self.rng_slot}
        # mouse_stream used to handle clicks
        self.mouse_stream = []
        self.text_elms    = {'inventory' :(Text('INVENTORY', 40), (360, 65)),
                             'help_equip':(Text('E: EQUIP/USE', 25), (360, 365)),
                             'stat_dam'  :(Text('DMG: 0'), (180, 140)),
                             'stat_def'  :(Text('DEF: 0'), (180, 200)),
                             'stat_dex'  :(Text('DEX: 0'), (180, 255)),
                             'stat_lck'  :(Text('LCK: 0'), (180, 310))}

    def handle_inventory(self, screen=None, clock=None):
        '''
            Entry-point method to inventory object 
            
            Renders interactable inventory whilst self.enable is True
        '''
        while(self.enable):
            self.screen, self.clock = screen, clock
            self.draw()
            d, de, dx, l = self.calculate_stats()
            self.player.dmg, self.player.defen, self.player.dex, self.lck = d, de, dx, l

    def add_item(self, item) -> NoReturn:
        '''
            Adds passed item to empty inventory slot
        '''
        for slot_xy in list(self.points.keys()):
            in_slot = self.points.get(slot_xy)
            if (in_slot == None):
                item.inv_x, item.inv_y = slot_xy[0], slot_xy[1]
                self.points.update({slot_xy: item})
                return

    def equip(self, mp):
        '''
            Equips the item if possible otherwise uses the item
            If item is equipped the item is swapped with corresponding equipment

            :param: mp -- mouse_position x, y : tuple
        '''
        if ((itm := self.points.get(self.locate(mp[0], mp[1]))) == None): return
        if (itm.type == 'weapon'):
            try:  # swap out item already in weapon slot
                self.add_item(self.wep_slot)
            except AttributeError:
                pass
            # weapon slot contains item, item.xy updated, slots updated
            self.wep_slot = itm
            itm.inv_x, itm.inv_y = 120, 120
            self.points.update({self.locate(mp[0], mp[1]): None})
            self.player_slots.update({(120, 120): self.wep_slot})
            self.update_text_stats()

    def calculate_stats(self) -> Tuple[int]:
        '''
            Calculates the sum of all stats given by all equipped items
            
            :return: sum of each stat (dam, def, dex, lck) : tuple
        '''
        dam, defen, dex, lck = 0, 0, 0, 0
        for item in self.player_slots.values():
            if (item == None): continue
            dam   += item.dam
            defen += item.defen
            dex   += item.dex
            lck   += item.luck
        return dam, defen, dex, lck

    def update_text_stats(self) -> NoReturn:
        '''
            Updates the player's stats visually displayed to the user
        '''
        dam, defen, dex, lck = self.calculate_stats()
        self.text_elms.update({'stat_dam': (Text('DMG: '+str(dam)), (180, 140))})
        self.text_elms.update({'stat_def': (Text('DEF: '+str(defen)),(180, 200))})
        self.text_elms.update({'stat_dex': (Text('DEX: '+str(dex)), (180, 255))})
        self.text_elms.update({'stat_lck': (Text('LCK: '+str(lck)), (180, 310))})

    """
        Draw methods -- on_hover -> stats of items in inventory on mouse hover
                     -- on_hover_equipped -> stats of equipped items on mouse hover
                     -- draw -> main method
    """
    
    def draw_on_hover(self, mp):
        '''
            Draw box displaying all stats of an item
            :param: mp -- mouse_position: tuple(x, y)
        '''
        if((itm := self.points.get(self.locate(mp[0], mp[1]))) == None):return
        itm.inv_hover(self.screen)

    def draw_on_hover_equipped(self, mp):
        '''
            Draw box displaying all stats of an item in the equipped section
            :param: mp -- mouse_position: tuple(x, y)
        '''
        if((itm := self.player_slots.get(self.locate(mp[0], mp[1]))) == None):return
        itm.inv_hover(self.screen)
                           
    def draw(self) -> NoReturn:
        '''
            Renders all elements/objects representing the player's inventory

            Draws -- empty slots for player equipment and inventory 
            Draws -- item images in player equipment and inventory
            Draws -- item stats on mouse hover over item
        '''
        # render visuals: <squares of w, h = 50, 50> <starting@ x, y = 300, 120>
        self.screen.fill((40, 40, 40))
        for x, y in self.points.keys():
            pygame.draw.rect(self.screen, (204, 156, 127), [x, y, 50, 50])
            
        # draw items in inventory
        for itm in self.points.values():
            if (itm != None): itm.inv_draw(self.screen)
            
        # draw squares for player slots
        for x, y in self.player_slots.keys():
            pygame.draw.rect(self.screen, (204, 156, 127), [x, y, 50, 50])
            
        # draw items for player slots
        for itm in self.player_slots.values():
            if (itm != None): itm.inv_draw(self.screen)

        # draw text
        for txt, xy in self.text_elms.values():
            self.screen.blit(txt, xy)
            
        # handle mouse-stream
        mouse_pos, mouse_click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        self.mouse_stream.append(mouse_click[0])
        if (len(self.mouse_stream) >= 3): del self.mouse_stream[0]
        
        # handle mouse-hover
        self.draw_on_hover(mouse_pos)
        self.draw_on_hover_equipped(mouse_pos)
        
        # handle key-presses
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: self.enable = False
                if event.key == pygame.K_e: self.equip(mouse_pos)
                if event.key == pygame.K_d:
                    print(f"<debug {self.points}>")
                    print(f"<debug {self.player_slots}>")
        # refresh screen <end>
        pygame.display.update()
        self.clock.tick(144)
