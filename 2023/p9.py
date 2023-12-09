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


def puzzle1(input):
    return sum([next_value(line) for line in input])


def puzzle2(input):
    return sum([prev_value(line) for line in input])


def next_value(sequence):
    s = sequence
    diffs = [s]
    while set(s) != set([0]):
       sd = dif_sequence(s)
       diffs.append(sd)
       s = sd
       if s==[]:
           halt()
    next_value = 0
    for line in diffs[::-1]:
        next_value += line[-1]
    return next_value


def prev_value(sequence):
    s = sequence
    diffs = [s]
    while set(s) != set([0]):
       sd = dif_sequence(s)
       diffs.append(sd)
       s = sd
       if s==[]:
           halt()
    prev_value = 0
    for line in diffs[::-1]:
        prev_value = line[0] - prev_value
    return prev_value


def dif_sequence(sequence):
    return [b-a for a,b in zip(sequence, sequence[1:])]


def get_puzzle_data(year, day, test):
    puzzle="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    if not test:
        puzzle = Puzzle(year=2023, day=9).input_data
    input = []
    for line in puzzle.split('\n'):
        input.append([int(i) for i in line.strip().split()])
    return input


if __name__=="__main__":
    test = False
    start = time.time()
    input = get_puzzle_data(2023, 9, test)
    print(f"{len(input)=}")

    print(f"{puzzle1(input)=}")
    print(f"{puzzle2(input)=}")

    print(time.time()-start)