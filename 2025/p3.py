import io
from aocd import get_data
import re


def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=3,year=2025)
        text_file = io.StringIO(data)
    return text_file


def max_part1(line):
    line = line.strip()
    d1 = max([int(d) for d in line[:-1]])
    d2 = max([int(d) for d in line[line.find(str(d1))+1:]])
    return 10*d1+d2


def max_part(line, n_remain, num_sofar):
    if n_remain>0:
        d = max([int(d) for d in line[:-n_remain]])
    else:
        d = max([int(d) for d in line])
    pos_d = line.find(str(d))
    line_remain = line[pos_d+1:]
    # print('>', 10*num_sofar + d, line_remain)
    return 10*num_sofar + d, line_remain

test_data = """987654321111111
811111111111119
234234234234278
818181911112111"""

if __name__=="__main__":

    max_high = 0
    text_file = read_data(test=False)
    lines = text_file.readlines()

    sum = 0
    for line in lines:
        sum += max_part1(line)
    print("part1 = ",sum)
 
    sum = 0
    for line in lines:
        num_sofar, line_remain = max_part(line.strip(), 11, 0)
        num_sofar, line_remain = max_part(line_remain, 10, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 9, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 8, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 7, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 6, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 5, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 4, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 3, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 2, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 1, num_sofar)
        num_sofar, line_remain = max_part(line_remain, 0, num_sofar)
        sum += num_sofar
    print("part2 = ",sum)
