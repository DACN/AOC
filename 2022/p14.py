import math
import re
from aocd.models import Puzzle
import timeit
from functools import cmp_to_key
from dataclasses import dataclass
import dataclasses
import sys
import timeit
import json

test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

class Abyss(Exception):
    # when we fall into the abyss
    pass

class Full(Exception):
    # when we cannot put in any more sand
    pass

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)


def erange(m, n):
    # automatically range up and down, and includes both end points
    if m <= n:
        return range(m,n+1)
    else:
        return range(m, n-1,-1)


def set_up_rocks():
    min_x = 1000
    max_x = 0
    max_y = 0
    # but we access rocks as rocks[y][x] - where y is the depth
    rocks= [ 1000*['.'] for i in range(501)]
    for line in input:
        points = [(int(m),int(n)) for m,n in [x.split(',') for x in line.split(' -> ')]]
        for p in points:
            max_x = max(max_x, p[0])
            min_x = min(min_x, p[0])
            max_y = max(max_y, p[1])
        for p1,p2 in zip(points, points[1:]):
            if p1[0]==p2[0]:
                for y in erange(p1[1], p2[1]):
                    rocks[y][p1[0]] = '#'
            elif p1[1]==p2[1]:
                for x in erange(p1[0], p2[0]):
                    rocks[p1[1]][x] = '#'
            else:
                print('unconsidered input')
    return rocks, min_x, max_x, max_y

def fall(rocks, p):
    px, py = p 
    while True:
        if rocks[py+1][px] == ".":
            py += 1
        elif rocks[py+1][px-1] == ".":
            py += 1
            px -= 1
        elif rocks[py+1][px+1] == ".":
            py += 1
            px += 1
        else:
            break
        if py > max_y:
            raise Abyss
    rocks[py][px] = 'o'
    return rocks

def show():
    for line in rocks[0:max_y+1]:
        print(''.join(line[min_x:max_x+1]))


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=14)
    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    rocks, min_x, max_x, max_y = set_up_rocks()
    show()
    n = 0
    while True:
        try:
            rocks = fall(rocks,(500,0))
            n += 1  # if we were success count one more grain
        except Abyss:
            print('Problem 1: ', n)
            break
    print()
    show()

    rocks, min_x, max_x, max_y = set_up_rocks()
    for x in range(1000):
        rocks[max_y+2][x] = "#"
    max_y += 2
    max_x += 2
    min_x -= 2
    show()
    n = 1
    while True:
        if (rocks[1][499] != ".") and (rocks[1][500] != ".") and (rocks[1][501] != "."):
                break
        rocks = fall(rocks,(500,0))
        n += 1  # if we were success count one more grain
    print('Problem 2: ', n)
    show()
