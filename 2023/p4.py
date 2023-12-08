import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())

def parse_line_1(line):
    card, line = line.split(':')
    winning_nos, your_nos = line.split("|")
    winning_nos = set(int(match.group()) for match in re.finditer(r'\d+', winning_nos))
    your_nos = set(int(match.group()) for match in re.finditer(r'\d+', your_nos))
    wins = len(winning_nos.intersection(your_nos))
    if wins>=1:
        return 2**(wins-1)
    else:
        return 0

def parse_line_2(line):
    card, line = line.split(':')
    winning_nos, your_nos = line.split("|")
    winning_nos = set(int(match.group()) for match in re.finditer(r'\d+', winning_nos))
    your_nos = set(int(match.group()) for match in re.finditer(r'\d+', your_nos))
    wins = len(winning_nos.intersection(your_nos))
    return wins

def puzzle1(x):
    return sum([parse_line_1(line) for line in input])


def puzzle2(x):
    total_cards = len(input)
    counts = defaultdict(int)
    for card, line in enumerate(input, start=1):
        counts[card] = counts[card] + 1
        for c in range(1, parse_line_2(line)+1):
            if card+c <= total_cards:
                counts[card+c] += counts[card]
    return sum(counts.values())



def get_puzzle_data(year, day, test):
    puzzle="""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    input = puzzle.split('\n')
    if not test:
        puzzle = Puzzle(year=2023, day=4)
        input = puzzle.input_data.split('\n')
    return input

if __name__=="__main__":
    test = False
    input = get_puzzle_data(2023, 4, test)

    print(f"{puzzle1(input)=}")
    print(f"{puzzle2(input)=}")