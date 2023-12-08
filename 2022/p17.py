import itertools
import functools
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

rocks = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

test_data=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)

def expand_rock(rock):
    rock_expanded = [7*[' '] for r in range(4)]
    rb = 4 # gives three blank lines
    rl = 2
    ru = 4
    for h,row in enumerate(reversed(rock)):
       rr = max(ru, 2+len(row))
       ru += 1
       line = 2*[" "] + [x if x!='.' else ' ' for x in row] + 5*[" "]
       line = line[:7]
       rock_expanded[h] = line
    return rock_expanded, (rl,rr,rb,ru)

def move_right(rock, bounds):
    (rl, rr, rb, ru) = bounds
    if rr ==7:
        return rock,(rl, rr, rb, ru)
    else: 
        return [[" "]+list(rock)[h][:6] for h in range(4)], (rl+1,rr+1,rb,ru)

def move_left(rock, bounds):
    (rl, rr, rb, ru) = bounds
    if rl ==0:
        return rock,(rl, rr, rb, ru)
    else: 
        return [rock[h][1:]+[' '] for h in range(4)], (rl-1,rr-1,rb,ru)

def left_right(wind, rock, bounds):
        left_right = next(wind)
        if left_right == ">":
            rock, bounds = move_right(rock, bounds)
        else:
            rock, bounds = move_left(rock, bounds)
        return rock, bounds

def show(rock, bounds):
        print('bounds :',bounds)
        for row in rock:
           print(row)
        print("\n============\n")
        print()

def overlap(chimney, rocks):
    return any(line_overlap(row_c, row_r) for row_c, row_r in zip(chimney, rocks))

def line_overlap(rowa, rowb):
    return any(x!=" " and y!=" " for x,y in zip(rowa, rowb))


def iter(wind, chimney, chimney_top, rock, bounds):
    #
    # First we move down the three spaces
    rl, rr, rb, ru = bounds
    for i in range(3):
        rock, bounds = left_right(wind, rock, bounds)
    rb = rb - 3
    ru = ru - 3
    # Then we see see if we have overlap at the top
    show(rock, bounds)
    for n in range(ru-rb):
        print('OVERLAP',n)
        rock, bounds = left_right(wind, rock, bounds)
        if overlap(chimney[chimney_top-n:chimney_top+1], rock[0:n+1]):
            print('found an overlap')
            chimney[chimney_top:chimney_top+ru-rb] = rock
            chimney_top = chimney_top + ru - rb
            break
        else:
            rb = rb -1
            ru = ru -1
    show(rock, bounds)
    print(chimney_top)
    halt()
            

if __name__=="__main__":

    EXAMPLE = True
    puzzle = Puzzle(year=2022, day=17)
    input = test_data.strip()
    if EXAMPLE:
        input = test_data.strip()
    else:
        input = puzzle_input.strip()


    wind = itertools.chain(input)
    rocks = [x.split('\n') for x in split_on_empty_lines(rocks)]
    rocks = [expand_rock(r) for r in rocks]
    rocks = itertools.cycle(rocks)
 

    chamber = [7*[''] for i in range(20000)]
    chamber[0] = 7*['-']
    chamber_top = 0
    highest_rock = 0
    n = 0

    rock, bounds = next(rocks)
    show(rock,bounds)
    iter(wind, chamber, chamber_top, rock, bounds)

  