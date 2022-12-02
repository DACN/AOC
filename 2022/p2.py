import re
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())

# Rock A X
# Paper B Y
# Scissors C Z
def calc1(s):
    match s[:3]:
        case "A X":
           return 1 + 3
        case "A Y":
            return 2 + 6
        case "A Z":
            return 3 + 0
        case "B X":
            return 1 + 0
        case "B Y":
            return 2 + 3
        case "B Z":
            return 3 + 6
        case "C X":
            return 1 + 6
        case "C Y":
            return 2 + 0
        case "C Z":
            return 3 + 3

# Rock A 
# Paper B
# Scissors C

# X loose
# Y draw
# Z win
def calc2(s):
    match s[:3]:
        case "A X":
           return 3 + 0
        case "A Y":
            return 1 + 3
        case "A Z":
            return 2 + 6
        case "B X":
            return 1 + 0
        case "B Y":
            return 2 + 3
        case "B Z":
            return 3 + 6
        case "C X":
            return 2 + 0
        case "C Y":
            return 3 + 3
        case "C Z":
            return 1 + 6


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=2)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')

    # solutions to each of the puzzles
    print(sum(map(calc1, input)))
    print(sum(map(calc2, input)))
    