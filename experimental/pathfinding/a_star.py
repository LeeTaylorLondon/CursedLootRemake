from typing import List

grid = [[1 for x in range(20)] for arr in range(20)]

def print2d(matrix):
    for vec in matrix: print(vec)
    print()

starting_coords = (6, 2)

# print2d(grid)

grid[6][2] = 0

print2d(grid)

def plotmags(matrix:List[List[int]], start_coords=None):
    rv = matrix.copy()
    if start_coords is None:
        for y,vec in enumerate(matrix):
            for x,n in enumerate(vec):
                if n == 0:
                    start_coords = (x,y)
    queue = [start_coords]
    while len(queue) > 0:
        x,y = queue.pop()
        print(x, y)
        mag = rv[y][x]
        try:
            if not y-1 < 0:
                rv[y-1][x] = mag + 1
                queue.append((x, y-1))
            print2d(rv)
        except IndexError:
            pass
    print2d(rv)


plotmags(grid)