import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def P1_process_line(line):
    # remove stuff before colone
    d = {'red':0, 'blue':0, 'green':0}
    game, line = line.split(":")
    game = int(''.join(c for c in game if c.isdigit()))
    line = line.replace(',','')
    line = line.replace(';','')
    ss = r'(\d+)[\s]+(red|blue|green)'
    nums = re.findall(ss, line)
    for v,colour in nums:
        d[colour] = max(d[colour], int(v))
    if d['red'] <= 12 and d['green']<=13 and d['blue'] <= 14:
        return game
    else:
        return 0

def P2_process_line(line):
    # remove stuff before colone
    d = {'red':0, 'blue':0, 'green':0}
    game, line = line.split(":")
    game = int(''.join(c for c in game if c.isdigit()))
    line = line.replace(',','')
    line = line.replace(';','')
    ss = r'(\d+)[\s]+(red|blue|green)'
    nums = re.findall(ss, line)
    for v,colour in nums:
        d[colour] = max(d[colour], int(v))
    return d['red'] * d['green'] * d['blue'] 


def puzzle1(x):
    return sum([P1_process_line(line) for line in input])


def puzzle2(x):
    return sum([P2_process_line(line) for line in input])


def get_puzzle_data(year, day, test):
    puzzle="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    input = puzzle.split('\n')
    if not test:
        puzzle = Puzzle(year=2023, day=2)
        input = puzzle.input_data.split('\n')
    return input

if __name__=="__main__":
    test = False
    input = get_puzzle_data(2023, 1, test)

    print(f"{puzzle1(input)=}")
    print(f"{puzzle2(input)=}")