import re
import string
from aocd.models import Puzzle


def calc_value(x):
    lc = set(string.ascii_lowercase)
    uc = set(string.ascii_uppercase)
    if x in lc:
        return ord(x) - ord('a') + 1
    else:
        return ord(x) - ord('A') + 27

def divide_list_into_chunks(l, n):
    # split a list returning a generator yielding lists with chunksize n
    for i in range(0, len(l), n):
        yield l[i:i + n]


def calc_a_line(s):
    first, second = s[:len(s)//2], s[len(s)//2:]
    common_values = set(first) & set(second)
    v = list(common_values)[0]
    return calc_value(v)


def elf_badge(s):
    # input s: three lines of stuff, return common item
    s0 = set(s[0])
    s1 = set(s[1])
    s2 = set(s[2])
    common = s0 & s1 & s2
    return list(common)[0]

if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=3)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')

    # solutions to each of the puzzles
    print('Problem 1: ',sum(map(calc_a_line,input)))

    badges = [elf_badge(s) for s in divide_list_into_chunks(input,3)]
    print('Problem 2: ',sum(map(calc_value, badges)))