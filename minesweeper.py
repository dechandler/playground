#!/usr/bin/env python3

import curses
import random
import sys

HEIGHT = 15
WIDTH = 40
NUM_MINES = 100

def get_surrounding(x, y):
    surrounding = {
        'tt': (x,     y - 1),
        'tr': (x + 1, y - 1),
        'rr': (x + 1, y    ),
        'br': (x + 1, y + 1),
        'bb': (x,     y + 1),
        'bl': (x - 1, y + 1),
        'll': (x - 1, y    ),
        'tl': (x - 1, y - 1)
    }
    to_del = []
    for k, v in surrounding.items():
        x, y = v
        if x in [-1, WIDTH] or y in [-1, HEIGHT]:
            to_del.append(k)
    for grid in to_del:
        del surrounding[grid]

    return surrounding.values()


def generate_minefield():
    """
    unexplored and safe: [None, #adj/diag]
    unexplored mine: [None, False]
    suspected mine: [False, ?]
    explored and safe: [True, #adj/diag]

    """
    minefield = []
    for row_num in range(0, HEIGHT):
        minefield.append([[None, 0] for grid in range(0, WIDTH)])

    for i in range(0, NUM_MINES):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if minefield[y][x][1] is not False:
            minefield[y][x][1] = False
            for gx, gy in get_surrounding(x, y):
                if minefield[gy][gx][1] is not False:
                    minefield[gy][gx][1] += 1

    return minefield

def draw_minefield(minefield):
    """
    unexplored fill: ■
    explored and 0: ' '
    explored and adj/diag: integer
    suspected mines: #
    """

    for y, row in enumerate(minefield):
        for x, col in enumerate(row):
            if col[0] is None:
                out = "■"
            elif col[0] is False:
                out = "#"
            else:
                out = ' ' if col[1] == 0 else str(col[1])
            screen.addstr(y + 1, x + 1, out)


def venture_to(x, y, minefield):
    grid = minefield[y][x]
    if grid[0] is True:
        return
    if grid[1] is False:
        sys.exit(0)
    else:
        grid[0] = True

    if grid[1] == 0:
        for gx, gy in get_surrounding(x, y):
            venture_to(gx, gy, minefield)


def cursor_bounds(cursor):
    if cursor[0] < 1:
        cursor[0] = 1
    elif cursor[0] > HEIGHT:
        cursor[0] = HEIGHT

    if cursor[1] < 1:
        cursor[1] = 1
    elif cursor[1] > WIDTH:
        cursor[1] = WIDTH

    return cursor

def main(stdscr):

    global screen
    screen = stdscr.subwin(HEIGHT + 2, WIDTH + 2, 0, 0)
    screen.box()

    cursor = [1, 1]

    minefield = generate_minefield()

    while True:
        draw_minefield(minefield)
        screen.refresh()
        stdscr.move(*cursor)

        k = stdscr.getkey()
        if k == "KEY_UP":
            cursor[0] -= 1
        elif k == "KEY_DOWN":
            cursor[0] += 1
        elif k == "KEY_LEFT":
            cursor[1] -= 1
        elif k == "KEY_RIGHT":
            cursor[1] += 1
        elif k == " ":
            venture_to(cursor[1] - 1, cursor[0] - 1, minefield)
        elif k == "x":
            minefield[cursor[0] - 1][cursor[1] - 1][0] = False
        elif k == 'q':
            break

        cursor = cursor_bounds(cursor)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)

