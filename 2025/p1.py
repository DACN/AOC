import io
from aocd import get_data
import re


def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=1,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_string(s):
    match = re.match(r"([A-Za-z])(\d*)$", s)
    if match:
        letter, number = match.groups()
        return letter, int(number)
    else:
        print(f"{match=}")
        raise ValueError("String format not valid")

count = 0
def add(pos, command, part1):
    global count
    com, turn = command
    pos_start = pos
    if com=="R":
        pos += turn
    elif com=="L":
        pos -= turn
    # PART 1
    if part1:
        pos = (pos + 100)%100
        if pos == 0:
            count +=1
    # PART 2
    else:
        if com=="R":
            count += pos // 100
            pos = pos % 100
        else:
            # pos_start_h = pos_start // 100
            # pos_finish_h = pos // 100
            # count += (pos_start_h-pos_finish_h)
            # if pos_start % 100==0: count -= 1
            # if pos % 100==0: count += 1
            # pos = pos % 100

            count += (pos_start-1)//100 - (pos-1)//100
            pos = pos % 100
    return pos


test_data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

if __name__=="__main__":
#   import os
#   print(os.environ["AOC_SESSION"])
    pos = 50
    part1 = False
    lines = read_data(False)
    for line in lines:
        command = parse_string(line)
        pos = add(pos, command, part1)
    print(count)

    # clockwise
    # 0 -> 750  7
    # 0 -> 700  7

    # widdershins
    # 370 -> 200  2  = (3-2)+1 finishing on 0
    # 370 -> 201  1  = (3-2) (
    # 470 -> 299  2  = (4-2)
    # 470 -> 200  3  = (4-2)+1
    # 300 -> 280  0  =3-2)-1 starting on 0