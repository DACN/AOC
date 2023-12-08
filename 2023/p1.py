import re
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def find_integers(s):
    ints =  [c for c in s if c.isdigit()]
    return 10*int(ints[0]) + int(ints[-1])


def nums_to_int(s):
    ''' string integers to ints'''
    nums = dict((("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
        ("zero", 0)))
    if s.isdigit():
        return(int(s))
    else:
        return nums[s]


def find_extended_integers(s):
    ss = r'(?=(0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine))'
    nums = [m.group(1) for m in re.finditer(ss, s)]
    return 10*nums_to_int(nums[0]) + nums_to_int(nums[-1])


def puzzle1(x):
    return sum([find_integers(line) for line in input])



def puzzle2(x):
    return sum([find_extended_integers(line) for line in input])


def get_puzzle_data(year, day, test):
    puzzle="""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
eightwo"""
    input = puzzle.split('\n')
    if not test:
        puzzle = Puzzle(year=2023, day=1)
        input = puzzle.input_data.split('\n')
    return input

if __name__=="__main__":
    test = False
    input = get_puzzle_data(2023, 1, test)

    print(f"{puzzle1(input)=}")
    print(f"{puzzle2(input)=}")