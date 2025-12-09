import io
from aocd import get_data
import re
import itertools
import math
from collections import defaultdict
from collections import Counter
import time
from shapely import Polygon, Point, box


def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=9,year=2025)
        text_file = io.StringIO(data)
    return text_file

def parse_string_numbers(s):
    return list(map(int, re.findall(r"[-+]?\d+", s)))


def part1(bricks):
    biggest_area = -math.inf
    area = {}
    for m,brick1 in enumerate(bricks):
        for n,brick2 in enumerate(bricks[m+1:],start=m+1):
            area[(m,n)] = (abs(brick1[0]-brick2[0])+1) * (abs(brick1[1]-brick2[1])+1)
            # print(m,n,brick1, brick2, area[(m,n)])
            biggest_area = max(biggest_area, area[(m,n)])
    return biggest_area


def y_part_from_x(bricks):
    d = defaultdict(list)
    for x,y in bricks:
        d[x] = d[x]+[y]
    return d

def x_part_from_y(bricks):
    d = defaultdict(list)
    for x,y in bricks:
        d[y] = d[y]+[x]
    return d


def part2(bricks):
    # dictionaries so we can find all horizonal and vertical pairs
    y_part_from_x_dict = y_part_from_x(bricks)
    x_part_from_y_dict = x_part_from_y(bricks)
    #
    # now we re-order the points so we get a proper bounding polygon rather
    # than something with criss-crossing lines
    brick = bricks[0]
    new_bricks = [brick]
    bricks.remove(brick)

    while bricks:
        x = brick[0]
        y = brick[1]
        y_parts = y_part_from_x_dict[x]
        other_y = y_parts[1] if y_parts[0]==y else y_parts[0]
        brick = [x,other_y]
        new_bricks = new_bricks + [brick]
        bricks.remove(brick)
    
        if bricks:
            y = brick[1]
            x = brick[0]
            x_parts = x_part_from_y_dict[y]
            other_x = x_parts[1] if x_parts[0]==x else x_parts[0]
            brick = [other_x, y]
            new_bricks = new_bricks + [brick]
            bricks.remove(brick)
    # 
    # so new_bricks continuously bounds the polygon
    polygon = Polygon(new_bricks)

    biggest_area = -math.inf
    # using new_bricks here just because we have removed all the info from bricks
    for m,brick1 in enumerate(new_bricks):
        for n,brick2 in enumerate(new_bricks[m+1:],start=m+1):
            inner_poly = box(min(brick1[0], brick2[0]), min(brick1[1], brick2[1]), 
                             max(brick1[0],brick2[0]), max(brick1[1], brick2[1]))
            area = (abs(brick1[0]-brick2[0])+1) * (abs(brick1[1]-brick2[1])+1)
            # limit the test to only candidate area, since area test is run first
            if area > biggest_area and polygon.covers(inner_poly):
                biggest_area = max(biggest_area, area)
    return biggest_area


test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


if __name__=="__main__":

    test = False
    text_file = read_data(test=test)
    lines = [line.rstrip() for line in text_file.readlines()]
    bricks = [parse_string_numbers(line) for line in lines]
    print(f"part 1 = ", part1(bricks))
    print(f"part 2 = ", part2(bricks))
