import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle
import sys
import timeit
import time
from operator import itemgetter


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


def puzzle1(puzzle):
    lines = lines_to_list(puzzle)
    times = lines[0]
    distances = lines[1]
    product = 1
    for t,d in zip(times, distances):
        product = product*sum([v*(t-v)>d for v in range(t)])
    return product

def puzzle2(puzzle):
    tme, distance = lines_to_nums(puzzle)
    product = sum([v*(tme-v)>distance for v in range(tme)])
    return product
    # 15290096


def get_puzzle_data(year, day, test):
    puzzle="""Time:      7  15   30
Distance:  9  40  200"""
    if not test:
        puzzle = Puzzle(year=2023, day=6).input_data
    lines = lines_to_list(puzzle)
    return puzzle


if __name__=="__main__":
    test = False
    start = time.time()
    puzzle = get_puzzle_data(2023, 6, test)


    print(f"{puzzle1(puzzle)=}")
    # 1312850

    print(f"{puzzle2(puzzle)=}")
    # 15290096

    print(time.time()-start)