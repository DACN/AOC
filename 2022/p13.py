import math
import re
from aocd.models import Puzzle
import timeit
from functools import cmp_to_key
from dataclasses import dataclass
import dataclasses
import sys
import timeit
import json

test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)


def compare_packets(left, right):
    # print(f'Comparing: {left=} {right=}')
    if isinstance(left, list) and isinstance(right, list):
        if not left and right:  # left is an empty list, right is not empty
            return True
        elif not right and left:  # right is an empty list, left not empty
            return False
        elif not left and not right:  # both empty, cant decide
            return None
        else:
            # both non-empty lists
            first_compare = compare_packets(left[0], right[0])
            if first_compare is None:
                return compare_packets(left[1:], right[1:])
            else:
                return first_compare
    else:
        # if we are both integersr
        if isinstance(left, int) and isinstance(right, int):
        # both instances are integers
            if left < right:
                return True
            elif right < left:
                return False
            else:
                return None
        elif isinstance(left, int) and isinstance(right, list):
            return compare_packets([left], right)
        elif isinstance(left, list) and isinstance(right, int):
            return compare_packets(left, [right])
        else:
            print(f"arg {left=} {right=}")
        sys.exit()

def cmp_sort(left, right):
    # Need for cmp_to_key to work. Needs a function returning +1,-1
    if compare_packets(left, right):
        return -1
    else:
        return 1


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=13)
    input = split_on_empty_lines(puzzle.input_data)
    # input = split_on_empty_lines(test_data)

    sum = 0
    for ind, packet_pair in enumerate(input, 1):
        packjson1, packjson2 = packet_pair.split('\n')
        pack1, pack2 = json.loads(packjson1), json.loads(packjson2)
        if compare_packets(pack1, pack2):
            sum += ind
    
    print("Problem 1:", sum)

    input = split_on_empty_lines(puzzle.input_data)
    # input = split_on_empty_lines(test_data)

    divider2 = [[2]]
    divider6 = [[6]]
    packets = [divider2, divider6]
    for packet_pair in input:
        packjson1, packjson2 = packet_pair.split('\n')
        pack1, pack2 = json.loads(packjson1), json.loads(packjson2)
        packets.append(pack1)
        packets.append(pack2)


    packets.sort(key=cmp_to_key(cmp_sort))
    # for e, line in enumerate(packets,1):
    #    print(e,line)
    print()
    ind2 = packets.index(divider2) + 1
    ind6 = packets.index(divider6) + 1
    print('Problem 2:', ind2*ind6)

    

