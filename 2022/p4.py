import re
import string
from aocd.models import Puzzle


def parse_line(line):
    a,b = line.split(',')
    a1,a2 = a.split('-')
    b1,b2 = b.split('-')
    return a1,a2,b1,b2


def puzzle1(x):
    a1,a2,b1,b2 = [int(n) for n in x]
    return ((a1<=b1) and (a2>=b2)) or ((b1<=a1) and (b2>=a2))


def puzzle2(x):
    a1,a2,b1,b2 = [int(n) for n in x]
    A = set(list(range(a1,a2+1)))
    B = set(list(range(b1,b2+1)))
    return len(A & B) > 0


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=4)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')

    
    # solutions to each of the puzzles
    print('Problem 1:  ',sum(map(puzzle1, [parse_line(line) for line in input])))
    print('Problem 2:  ',sum(map(puzzle2, [parse_line(line) for line in input])))
 