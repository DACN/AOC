import re
import string
from aocd.models import Puzzle


def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)

def matrixT(A):
    return  [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def get_stacks(input):
    raw_boxes = input.splitlines()
    col_numbers = raw_boxes[-1].split()
    max_col = int(col_numbers[-1])
    boxesT = [[line[i+1:i+2] for i in range(0, max_col*4, 4)] for line in  input.splitlines()]
    boxes = matrixT(boxesT)
    clean_boxes = [[x for x in line if x != " "] for line in boxes]
    return clean_boxes

def move(m, n):
    # move a box from stack m to stack n
    old = stacks[m-1]
    new = stacks[n-1]
    box = old[0]
    old = old[1:]
    stacks[n-1] = [box] + new
    stacks[m-1] = old

def move_n(num, m, n):
    # move a stack of boxes, tower of babel style
    for i in range(num):
        move(m, n)

def move_multi(num, m, n):
    # move a stack of boxes in a oner from stack m to stack n
    old = stacks[m-1]
    new = stacks[n-1]
    boxes = old[0:num]
    old = old[num:]
    stacks[n-1] = boxes + new
    stacks[m-1] = old

if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=5)

    # input is an array, with each item being a string
    input = split_on_empty_lines(puzzle.input_data)
    # input[0] is boxes and pull out all the letters in a list of lists, needing to transpose to get stacks
    stacks = get_stacks(input[0])
    for line in input[1].splitlines():
        _, num, _, m, _, n = line.split(' ')
        num, m, n = int(num), int(m), int(n)
        move_n(num, m, n)
    top = [stacks[i][0] for i in range(len(stacks))]
    print('First part: ', ''.join(top))

    # input is an array, with each item being a string
    input = split_on_empty_lines(puzzle.input_data)
    # input[0] is boxes and pull out all the letters in a list of lists, needing to transpose to get stacks
    stacks = get_stacks(input[0])
    for line in input[1].splitlines():
        _, num, _, m, _, n = line.split(' ')
        num, m, n = int(num), int(m), int(n)
        move_multi(num, m, n)
    top = [stacks[i][0] for i in range(len(stacks))]
    print('Second part: ', ''.join(top))
