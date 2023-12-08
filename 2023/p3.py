import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def find_symbs(input):
    symbol_set = []
    for line in input:
        for c in line:
            if c in '0123456789.':
                pass
            else:
                symbol_set.append(c)
    symbol_set = set(symbol_set)
    d = {}
    symbs = []
    for j, line in enumerate(input):
        for i,c in enumerate(line):
            if c in symbol_set:
                symbs.append((i,j))
                d[(i,j)] = c
    return symbs,d


def find_gears(input):
    cnt = {}
    gears = []
    gear_ratio = {}
    for j, line in enumerate(input):
        for i,c in enumerate(line):
            if c == '*':
                gears.append((i,j))
                cnt[(i,j)] = 0
                gear_ratio[(i,j)] = 0
    return gears,cnt,gear_ratio


def adjacent(span, row, symbs):
    adjacent = False
    span_l, span_h = span
    for i in range(span_l-1, span_h+1):
        for j in range(row-1,row+2):
        #   print("testing", i,j)
            if (i,j) in symbs:
                # print('found', i,j)
                return True
    return False


def adjacent_gears(number, span, row, gears):
    print(f"{number=}, {span=}, {row=}, {gears=}")
    span_l, span_h = span
    for i in range(span_l-1, span_h+1):
        for j in range(row-1,row+2):
        #   print("testing", i,j)
            if (i,j) in gears:
                cnt[(i,j)] += 1
                if cnt[(i,j)]==1:
                    gear_ratio[(i,j)]=int(number)
                elif cnt[(i,j)]==2:
                    gear_ratio[(i,j)]= gear_ratio[(i,j)]*int(number)
                else:
                    gear_ratio[(i,j)]=0
                print(f"{number=}")
                print(f"{i},{j},{cnt[(i,j)]=}")
                print(f"{gear_ratio[(i,j)]=}")
                print()


def puzzle1(x):
    total = 0
    for j,line in enumerate(x):
        nums = re.finditer(r'\d+', line)
        for match in nums:
            # print(int(match.group()), adjacent(match.span(),j,symbs))
            if adjacent(match.span(),j,symbs):
                total += int(match.group())
                # print(match.group())
    return total



def puzzle2(x):
    total = 0
    for j,line in enumerate(x):
        nums = re.finditer(r'\d+', line)
        for match in nums:
            # print(int(match.group()), adjacent(match.span(),j,symbs))
            adjacent_gears(match.group(),match.span(),j,gears)
    print(f"{gear_ratio=}")
    for (i,j) in gears:
        print(f"{i},{j},{cnt[(i,j)]=}, {gear_ratio[(i,j)]=}, {total=}")
        if cnt[(i,j)]==2:
            total += gear_ratio[(i,j)]
    return total



def get_puzzle_data(year, day, test):
    puzzle="""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    input = puzzle.split('\n')
    if not test:
        puzzle = Puzzle(year=2023, day=3)
        input = puzzle.input_data.split('\n')
    return input

if __name__=="__main__":
    test = False
    input = get_puzzle_data(2023, 1, test)

    symbs, d = find_symbs(input)
    print(f"{puzzle1(input)=}")
    gears,cnt,gear_ratio = find_gears(input)
    print(f"{gears=}")
    print(f"{gear_ratio=}")
    print(f"{cnt=}")
    print(f"{puzzle2(input)=}")