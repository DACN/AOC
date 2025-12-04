import io
from aocd import get_data
import re
import itertools

def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=4,year=2025)
        text_file = io.StringIO(data)
    return text_file


def expand(lines):
    # add lines before & after
    # add buffer before & after each line
    L = len(lines[0].strip())
    top = (L+2)*'.'
    expanded_lines = [top]
    for line in lines:
        expanded_lines += ['.'+line.strip()+'.']
    expanded_lines += [top]
    return expanded_lines


def sliding_window(iterable):
    # iterate over three lines at once
    it1, it2, it3 = itertools.tee(iterable, 3)
    next(it2, None)
    next(it3, None); next(it3, None)
    return zip(it1, it2, it3)


def count(lines):
    total = 0
    new_lines = []
    for lineb, line, linea in sliding_window(expand(lines)):
        roll_total = 0
        new_line = ""
        for m in range(1,len(line)-1):
            roll_total = 0
            if line[m] == "@":
                roll_total += (lineb[m-1]=="@") + (lineb[m]=="@" ) + (lineb[m+1]=="@")
                roll_total += (line[m-1]=="@" ) + (line[m+1]=="@")
                roll_total += (linea[m-1]=="@") + (linea[m]=="@" ) + (linea[m+1]=="@")
                if roll_total < 4:
                    total += 1
                    new_line += "."
                else:
                    new_line += "@"
            else:
                new_line += "."
        new_lines += [new_line]
    return total, new_lines


test_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


if __name__=="__main__":

    text_file = read_data(test=False)
    lines = text_file.readlines()

    print('part 1 = ',count(lines)[0])

    grand_total = 0
    while True:
        cnt, new_lines = count(lines)
        grand_total += cnt
        if cnt==0:
            break
        lines = new_lines
    print('part 2 = ', grand_total)
