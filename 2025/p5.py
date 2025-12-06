import io
from aocd import get_data
import re
import itertools
from range import Range, ComplexRange

def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=5,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_string_ranges(s):
    match = re.match(r"(\d*)-(\d*)$", s)
    if match:
        low, high = match.groups()
        return(int(low), int(high))
    else:
        print(f"{match=}")
        raise ValueError("String format not valid")

def parse_string_ingredients(s):
    match = re.match(r"(\d*)$", s)
    if match:
        ingredient = match.groups()[0]
        return(int(ingredient))
    else:
        print(f"{match=}")
        raise ValueError(f"String format not valid, line = !{line}!")

def in_ranges(x, ranges):
    for (r_low, r_high) in ranges:
        if x in range(r_low, r_high+1):
            return True
    return False

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


test_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


if __name__=="__main__":

    text_file = read_data(test=False)
    lines = text_file.readlines()
    ranges = []
    ingredients = []
    get_ranges = True
    for line in lines:
        if line.strip()=="":
            get_ranges = False
            continue
        if get_ranges:
            ranges += [parse_string_ranges(line.strip())]
        else:
            ingredients.append(parse_string_ingredients(line.strip()))

    fresh_count = 0
    for ingredient in ingredients:
        if in_ranges(ingredient, ranges):
            fresh_count += 1
    print('part 1 =', fresh_count)

    cr = ComplexRange()
    for range in ranges:
        cr.add(Range(range[0], d_to_closed=range[1]))
    print('part 2 = ', len(cr))