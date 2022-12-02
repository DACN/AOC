import re
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def s_largest(a):
    # second largest of an array - has side effect of removing largest element
    # which we use to find the third largest
    l = max(a)
    a.remove(l)
    return max(a)

if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=1)

    # input is an array, with each item being a string of lines
    input = split_on_empty_lines(puzzle.input_data)
    # inputx is an array with each element being an array of integers
    inputx = []
    for x in input:
        inputx.append([int(l) for l in x.splitlines()])

    # and the sums for each of the elves
    sums = [sum(x) for x in inputx]
    e1 = max(sums)        # larges
    e2 = s_largest(sums)  # second largest
    e3 = s_largest(sums)  # third largest
    # and the answers
    print(e1)
    print(e1+e2+e3)
