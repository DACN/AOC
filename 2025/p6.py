import io
from aocd import get_data
import re
import itertools
import math

def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=6,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_string_numbers(s):
    return list(map(int, re.findall(r"[-+]?\d+", s)))


def parse_string_operators(s):
    return list(re.findall(r"\*\*|[+\-*/]", s))

def calc(numbers, operator):
    if operator == "+":
        return(sum(numbers))
    elif operator == "*":
        return math.prod(numbers)
    else:
        sys.exit(1)

test_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


if __name__=="__main__":

    text_file = read_data(test=False)
    lines = text_file.readlines()
    numbers = []
    for line in lines[:-1]:
        number_line = parse_string_numbers(line)
        numbers += [number_line]
    operators = parse_string_operators(lines[-1])

    numbersT = zip(*numbers) # transpose
    sum_part1 = 0
    for line, operator in zip(numbersT, operators):
        sum_part1 += calc(line, operator)
    print('part 1 = ', sum_part1)

    numbers = []
    for line in lines[:-1]:
        # numbers += list[line.strip('\n')]
        numbers += [[c for c in line.strip('\n')]]

    numbersT = zip(*numbers)
    data = ""
    for line in numbersT:
        data += ''.join(line) + ' '
        if set(line)==set([' ']):
            data += '\n'

    groups = data.strip().split("\n")
    numbers = []
    for line in groups:
        number_line = parse_string_numbers(line)
        numbers += [number_line]
    sum_part2 = 0
    for line, operator in zip(numbers, operators):
        sum_part2 += calc(line, operator)
    print('sum_part2 = ', sum_part2)