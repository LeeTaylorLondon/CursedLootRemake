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

    # up, right, left = [^ > <]
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
        # if not y-1 < 0: # up
        #     if rv[y-1][x] is None:
        #         queue.append((x, y-1))
        #         rv[y-1][x] = mag + 1
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


def astar():
    pass


grid = [[1 for x in range(20)] for arr in range(20)]

starting_coords = (2, 6)
x0, y0 = starting_coords

for y in range(3, 10):
    grid[y][11] = 0

grid[y0][x0] = 0
print2d(grid)

plotmags(grid, (x0, y0))

