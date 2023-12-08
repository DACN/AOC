import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle
import sys
import timeit
import time
from operator import itemgetter


def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def lines_to_list(s):
    lines = s.split('\n')
    fun_list = []
    for line in lines:
        fun_list.append(list(int(match.group()) for match in re.finditer(r'\d+', line)))
    return fun_list

def lines_to_nums(s):
    lines = s.split('\n')
    tme = int(''.join(c for c in lines[0] if c.isdigit()))
    distance = int(''.join(c for c in lines[1] if c.isdigit()))
    return tme, distance


def classify_hand_type(s):
    d = Counter(s).values()
    if 5 in d:
        value = '9'  #return 'five'
    elif 4 in d:
        value = '8'  #return 'four'
    elif 3 in d and 2 in d:
        value = '7'  #return 'full'
    elif 3 in d:
        value = '6'  #return 'three'
    elif 2 in d and 1 in d and len(d)==3:
        value = '5'  #return 'two_pair'
    elif 2 in d and 1 in d and len(d)==4:
        value = '4'  #return 'pair'
    elif 1 in d and len(d)==5:
        value = '3'  #return 'high'
    else:
        print('Error in classifying', s)
        sys.exit()
    for c in s:
        if c.isdigit():
            value = value + '0' + c
        elif c=='T':
            value = value + '10'
        elif c=='J':
            value = value + '11'
        elif c=='Q':
            value = value + '12'
        elif c=='K':
            value = value + '13'
        elif c=='A':
            value = value + '20'
    return int(value)

def classify_hand_type_2(s):
    jokers = s.count('J')
    s_orig = s
    s_minus = s.replace('J','')
    d = Counter(s_minus).values()
    if jokers == 0:
        if 5 in d:
            value = '9'  #return 'five'
        elif 4 in d:
            value = '8'  #return 'four'
        elif 3 in d and 2 in d:
            value = '7'  #return 'full'
        elif 3 in d:
            value = '6'  #return 'three'
        elif 2 in d and 1 in d and len(d)==3:
            value = '5'  #return 'two_pair'
        elif 2 in d and 1 in d and len(d)==4:
            value = '4'  #return 'pair'
        elif 1 in d and len(d)==5:
            value = '3'  #return 'high'
        else:
            print('Error in classifying', s)
            sys.exit()
        for c in s:
            if c.isdigit():
                value = value + '0' + c
            elif c=='T':
                value = value + '10'
            elif c=='J':
                value = value + '11'
            elif c=='Q':
                value = value + '12'
            elif c=='K':
                value = value + '13'
            elif c=='A':
                value = value + '20'
        return int(value)
    elif jokers == 1:
        if 4 in d:
            value = '9'  #return 'five'
        elif 3 in d:
            value = '8'  #return 'four'
        elif 2 in d and len(d)==2:  # two pairs upgrade to a full house
            value = '7'  # full house
        elif 2 in d:
            value = '6'  #return 'three'
        # dont think we can get to two pairs with a joker
        #    value = '5'  #return 'two_pair'
        elif 1 in d:
            value = '4'  #return 'pair'
        # we can always do better than a high
        #    value = '3'  #return 'high'
        else:
            print('Error in classifying', s)
            sys.exit()
        for c in s_orig:
            if c.isdigit():
                value = value + '0' + c
            elif c=='T':
                value = value + '10'
            elif c=='J':
                value = value + '00'
            elif c=='Q':
                value = value + '12'
            elif c=='K':
                value = value + '13'
            elif c=='A':
                value = value + '20'
        return int(value)
    elif jokers == 2:
        if 3 in d:
            value = '9'  #return 'five'
        elif 2 in d:
            value = '8'  #return 'four'
        else:
            value = '6'  #return 'three'
        for c in s_orig:
            if c.isdigit():
                value = value + '0' + c
            elif c=='T':
                value = value + '10'
            elif c=='J':
                value = value + '00'
            elif c=='Q':
                value = value + '12'
            elif c=='K':
                value = value + '13'
            elif c=='A':
                value = value + '20'
        return int(value)    
    elif jokers == 3:
        if 2 in d:
            value = '9'  #return 'five'
        else:
            value = '8'  #return 'four'
        for c in s_orig:
            if c.isdigit():
                value = value + '0' + c
            elif c=='T':
                value = value + '10'
            elif c=='J':
                value = value + '00'
            elif c=='Q':
                value = value + '12'
            elif c=='K':
                value = value + '13'
            elif c=='A':
                value = value + '20'
        return int(value)    
    elif jokers in [4,5]:
        value = '9'     # return 'five'    
        for c in s_orig:
            if c.isdigit():
                value = value + '0' + c
            elif c=='T':
                value = value + '10'
            elif c=='J':
                value = value + '00'
            elif c=='Q':
                value = value + '12'
            elif c=='K':
                value = value + '13'
            elif c=='A':
                value = value + '20'
        return int(value)    


def puzzle1(lines):
    extended_lines = []
    for line in lines:
        hand, bid = line.split(' ')
        extended_lines.append([classify_hand_type(hand), hand, int(bid)])
    extended_lines = sorted(extended_lines, key=itemgetter(0))
    value = 0
    for i, line in enumerate(extended_lines, start=1):
        value += i*line[2]
    return value

def puzzle2(lines):
    extended_lines = []
    for line in lines:
        hand, bid = line.split(' ')
        extended_lines.append([classify_hand_type_2(hand), hand, int(bid)])
    extended_lines = sorted(extended_lines, key=itemgetter(0))
    value = 0
    for i, line in enumerate(extended_lines, start=1):
        value += i*line[2]
    return value


def get_puzzle_data(year, day, test):
    puzzle="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    if not test:
        puzzle = Puzzle(year=2023, day=7).input_data
    lines = puzzle.split('\n')
    return lines


if __name__=="__main__":
    test = False
    start = time.time()
    puzzle = get_puzzle_data(2023, 7, test)


    print(f"{puzzle1(puzzle)=}")
    # 247961593
    print(f"{puzzle2(puzzle)=}")
    # 15290096

    print(time.time()-start)