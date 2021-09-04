from typing import List


def print2d(matrix):
    for vec in matrix: print(vec)
    print()


def plotmags(matrix:List[List[int]], start_coords=None):
    rv = matrix.copy()
    if start_coords is None:
        for y,vec in enumerate(matrix):
            for x,n in enumerate(vec):
                if n == 0:
                    start_coords = (x,y)
    for y,vec in enumerate(matrix):
        for x,n in enumerate(vec):
            if matrix[y][x] == 0: continue
            matrix[y][x] = None
    queue = [start_coords]
    d_counter = 0
    while len(queue) > 0:
        d_counter += 1
        x,y = queue.pop()
        # print(f"y:{y},x:{x}")
        mag = rv[y][x]
        if not x-1 < 0: # left
            if rv[y][x-1] is None:
                queue.append((x-1, y))
                rv[y][x-1] = mag + 1
        if not x+1 >= len(rv[y]): # right
            if rv[y][x+1] is None:
                queue.append((x+1, y))
                rv[y][x+1] = mag + 1
        if not y-1 < 0: # up
            if rv[y-1][x] is None:
                queue.append((x, y-1))
                rv[y-1][x] = mag + 1
        print2d(rv)

    queue = [start_coords]
    while len(queue) > 0:
        d_counter += 1
        x,y = queue.pop()
        # print(f"y:{y},x:{x}")
        mag = rv[y][x]
        if not x-1 < 0: # left
            if rv[y][x-1] is None:
                queue.append((x-1, y))
                rv[y][x-1] = mag + 1
        if not x+1 >= len(rv[y]): # right
            if rv[y][x+1] is None:
                queue.append((x+1, y))
                rv[y][x+1] = mag + 1
        if not y+1 >= len(rv): # down
            if rv[y+1][x] is None:
                queue.append((x, y+1))
                rv[y+1][x] = mag + 1

    print2d(rv)
    print(f"Actions: {d_counter}")

grid = [[1 for x in range(20)] for arr in range(20)]

starting_coords = (6, 2)

grid[6][2] = 0

print2d(grid)

plotmags(grid, (2,6))