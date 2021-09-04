from typing import List

grid = [[1 for x in range(20)] for arr in range(20)]

def print2d(matrix):
    for vec in matrix: print(vec)
    print()

starting_coords = (6, 2)

print2d(grid)

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
    while len(queue) != 0:
        x, y = queue.pop()
        try:
            current_mag = matrix[y][x]
        except IndexError:
            continue
        try:
            matrix[y-1][x] = current_mag + 1
        except IndexError:
            pass
        try:
            matrix[y][x+1] = current_mag + 1
        except IndexError:
            pass
        try:
            matrix[y+1][x] = current_mag + 1
        except IndexError:
            pass
        try:
            matrix[y][x-1] = current_mag + 1
        except IndexError:
            pass
        queue.append((y-1, x))
        queue.append((y, x+1))
        queue.append((y+1, x))
        queue.append((y, x-1))
        print2d(rv)
    print2d(rv)
    return rv


plotmags(grid)