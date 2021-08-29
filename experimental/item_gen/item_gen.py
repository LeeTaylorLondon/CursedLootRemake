import random


FILE_DIR = 'item_data.txt'
ITEM_ID  = 0
TYPES_   = {0: 'weapon', 1: 'scroll', 2: 'armour', 3: 'potion'}


def write():
    with open(FILE_DIR, 'w') as f:
        f.write('test')

def plan():
    # >>> decide how many items per each level i.e (0, 2)
    #     generate item data => ID, TYPE, STATS, LEVEL/DEPTH/FLOOR

    # >>> STATS: include gro_x, gro_y, this cannot be known without level data
    #     therefore level data should be generated first THEN this reads only the
    #     necessary files to generate such attributes, furthermore no two items
    #     should have the same gro_x, gro_y attribute values!
    
    # >>> write each item data as a single line of text to FILE_DIR
    #     build something to unpack and construct items from this data
    #     such that the items are spawned in on the ground with their stats etc.etc
    # >>> ???
    # >>> $$$profit
    pass

def item_decider():
    pass

def item_generator():
    # TYPE = Scroll, Weapon, Armour, Potion, Ring, Necklace
    rv = ()
    item_type = 
    return rv
    
def main():
    pass

if __name__ == '__main__':
    main()
