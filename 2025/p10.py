import io
from aocd import get_data
import re
import itertools
import math
from collections import defaultdict
from collections import Counter
import time
from shapely import Polygon, Point, box
from scipy.optimize import linprog
import pulp


def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=10,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_string(s):
    idx = s.find(']')
    s1 = s[:idx+1]
    s  = s[idx+1:].strip()
    idx = s.find('{')
    s2 = s[:idx].strip(' ')
    s3  = s[idx:].strip(' {}')
    match = re.match(r"(\[[.#]+\])", s1)
    if match:
        text = match.groups()[0].strip(" []")
        # Convert to tuple of 0 and 1
        lights = [1 if c == "#" else 0 for c in text]
    # second part
    tuple_pattern = r"\(\d+(?:,\d+)*\)"
    matches = re.findall(tuple_pattern, s2)
    # Convert matches from strings to actual tuples of integers
    tuples = [tuple(map(int, m.strip("()").split(","))) for m in matches]
    tuples2 = []
    for tup in tuples:
        tuples2 += [[1 if i in tup else 0 for i in range(len(lights))]]
    #
    curly_bracket = list(map(int, re.findall(r"[-+]?\d+", s3)))
    return lights, tuples, tuples2, curly_bracket

def is_solution(numbers, tuples, lights):
    off_on = len(lights)*[0]
    N = 0
    # print("----")
    # print("----")
    L = len(tuples)
    # print(f"{L=}, {numbers=}, {tuples=}, {lights=}")
    for n,t in zip(numbers,tuples):
        if n==1:
            N +=1
            # print(">", n, t)
            for s in t:
                off_on[s] = 1 - off_on[s]
            # print(n, off_on)
            # print(f"{L=}, {off_on=}, {lights=}")
    if off_on==lights:
        return N
    else:
        return math.inf

def best_solution(L, tuples, lights):
    N = math.inf
    L = len(tuples)
    for numbers in itertools.product([0, 1], repeat=L):
        # print()
        # print(f"{numbers=}")
        N = min(is_solution(numbers, tuples, lights), N)
    return N

def part1(lines):
    sum = 0
    for line in lines:
        lights, tuples, tuples2, curly_bracket = parse_string(line)
        # print(lights, tuples, curly_bracket)
        # print('--')

        L = len(lights)
        # print(best_solution(L, tuples, lights))
        sum += best_solution(L, tuples, lights)
        # break
    return sum

def part2(lines):

    sum = 0
    for line in lines:
        lights, tuples, tuples2, curly_bracket = parse_string(line)
        # print(lights, tuples, tuples2, curly_bracket)
        tuples2T = list(map(list, zip(*tuples2)))
        c = [1]*len(tuples2T[0])  # minimize sum of x

        # Create problem
        prob = pulp.LpProblem("MinimizeX", pulp.LpMinimize)
                # Integer variables
        x = [pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(len(tuples2T[0]))]
                # Objective
        prob += pulp.lpDot(c, x)
                # Constraints: tuples2T * x = lights
        for row, target in zip(tuples2T, curly_bracket):
            prob += pulp.lpDot(row, x) == target
                # Solve
        # status = prob.solve()
        # Solve quietly
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        print("Objective =", pulp.value(prob.objective))
        sum += pulp.value(prob.objective)
    return sum

test_data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


if __name__=="__main__":

    test = False
    text_file = read_data(test=test)
    lines = [line.rstrip() for line in text_file.readlines()]

    print("part 1 = ",part1(lines))
    print("part 2 = ",part2(lines))

