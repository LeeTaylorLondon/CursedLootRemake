import pygame
from random import randint


SWORD1_IMG = pygame.image.load('assets/items/sword1.png')
SWORD2_IMG = pygame.image.load('assets/items/sword2.png')
SWORD3_IMG = pygame.image.load('assets/items/sword3.png')
SWORD4_IMG = pygame.image.load('assets/items/sword4.png')
SWORD_IMGS = {1: SWORD1_IMG, 2: SWORD2_IMG, 3: SWORD3_IMG,
              4: SWORD4_IMG}


def gen_text_obj(text: str, font_size=20) -> pygame.surface:
    '''
        Returns renderable passed string to text object
        :param:  text      -- string message to be converted : str
                 font_size -- the size of the text : int
                 
        :return: text_surf -- this passed to screen.blit with
            coordinates is rendered useful : pygame.surface 
    '''
    large_text = pygame.font.Font('freesansbold.ttf', font_size)  # 20 => font_size
    text_surf  = large_text.render(text, True, (175, 175, 175))
    return text_surf


class Item:
    '''
        todo: attr's -> image, type/category, stats
                        might be a parent class
    '''
    def __init__(self, screen=None):
        self.id     = 0
        self.screen = screen
        # item stats => damage, defense, dexterity, luck
        self.dam     = randint(1, 9)
        self.defen   = randint(1, 30)
        self.dex     = randint(1, 30)
        self.luck    = randint(1, 30)
        self.type    = 'weapon'
        # visual attributes
        self.img   = SWORD_IMGS.get(randint(1, 4))
        self.inv_x = 0  # inventory x 
        self.inv_y = 0  # inventory y
        self.gro_x = 0  # ground (level) x 
        self.gro_y = 0  # ground (level) y
        # inv visual attributes
        self.dam_t  = None  # surf + rect
        self.defe_t = None
        self.dex_t  = None
        self.luck_t = None
        self.init_text_attrs()

    def __repr__(self):
        return f"<item id={self.id}, stats={self.dam, self.defen, self.dex, self.luck}>"

    def init_text_attrs(self):
        self.dam_t  = gen_text_obj('DMG: '+str(self.dam))
        self.defe_t = gen_text_obj('DEF: '+str(self.defen))
        self.dex_t  = gen_text_obj('DEX: ' +str(self.dex))
        self.luck_t = gen_text_obj('LCK: '+str(self.luck))

    def gro_draw(self, screen, xos, yos):
        screen.blit(self.img, (self.gro_x + xos, self.gro_y + yos))
        
    def inv_draw(self, screen):
        screen.blit(self.img, (self.inv_x, self.inv_y))

    def inv_hover(self, screen):
        pygame.draw.rect(screen, (20, 20, 105), [self.inv_x, self.inv_y + 45, 100, 110])
        screen.blit(self.dam_t,  (self.inv_x, self.inv_y + 50))
        screen.blit(self.defe_t, (self.inv_x, self.inv_y + 75))
        screen.blit(self.dex_t,  (self.inv_x, self.inv_y + 100))
        screen.blit(self.luck_t, (self.inv_x, self.inv_y + 125))
        
    def inv_click(self, screen):
        # small menu: options => [ 'Equip', 'Destory', 'Sort' ]
        pygame.draw.rect(screen, (20, 20, 105), [self.inv_x, self.inv_y + 45, 100, 110])
        pass


def main():
    pass

if __name__ == '__main__':
    main()
