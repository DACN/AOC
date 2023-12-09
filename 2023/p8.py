import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle
import sys
import timeit
import time
from operator import itemgetter
import itertools
import math


def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def lines_to_list(s):
    lines = s.split('\n')
    fun_list = []
    for line in lines:
        fun_list.append(list(int(match.group()) for match in re.finditer(r'\d+', line)))
    return fun_list

def lines_to_nums(s):
    lines = s.split('\n')
    tme = int(''.join(c for c in lines[0] if c.isdigit()))
    distance = int(''.join(c for c in lines[1] if c.isdigit()))
    return tme, distance

def move_pos(pos, move):
    if move=="L":
        pos = map_d[pos][0]
    elif move=="R":
        pos = map_d[pos][1]
    else:
        print(f"{instructions=},{move=}")
        print("error")
        sys.exit()
    return pos

def puzzle1(instructions, map_d):
    pos = "AAA"
    for step, move in enumerate(itertools.cycle(instructions), start=1):
        pos = move_pos(pos, move)
        if pos=="ZZZ":
            break
    return step


def puzzle2(instructions, map_d):
    posns = list(m for m in map_d.keys() if m[-1]=="A")
    for pos in posns:
        print(pos)
        for step, move in enumerate(itertools.cycle(instructions), start=1):
            pos = move_pos(pos, move)
            if pos[-1]=='Z':
                break
        print(pos, step)
        for step, move in enumerate(itertools.cycle(instructions), start=1):
            pos = move_pos(pos, move)
            if pos[-1]=='Z':
                break
        print(pos, step)
        print("-----------")
    # numbers grabbed directly from running the above code and finding
    # the length of the loops
    return math.lcm(22199, 13207, 16579, 18827, 17141, 14893)


def get_puzzle_data(year, day, test):
    puzzle="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    if not test:
        puzzle = Puzzle(year=2023, day=8).input_data
    return split_on_empty_lines(puzzle)


if __name__=="__main__":
    test = False
    start = time.time()
    input = get_puzzle_data(2023, 9, test)
    instructions, map = input
    map = map.split('\n')
    map_d = {}
    for entry in map:
        here, there = entry.split(' = ')
        there = there.replace('(','').replace(')','')
        there_l, there_r = there.split(', ')
        map_d[here] = (there_l, there_r)

    print(f"{puzzle1(instructions, map_d)=}")
    # 22199
    print(f"{puzzle2(instructions, map_d)=}")

    print(time.time()-start)