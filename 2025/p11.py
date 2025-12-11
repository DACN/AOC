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
from enum import Enum, auto

class State(Enum):
    PERMANENT = auto()
    TEMPORARY = auto()
    NONE = auto


def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=11,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_input(lines):
    tree = defaultdict(list)
    all_nodes = []
    for line in lines:
        nodes = line.split()
        node_from = nodes[0].strip(":")
        tree[node_from] = nodes[1:]
        all_nodes += nodes[1:]
        all_nodes.append(node_from)
    all_nodes = list(set(all_nodes))
    return tree, all_nodes


def topological_sort(tree, nodes):
    """
    graph: dict[node] = list of neighbors
    returns: list of nodes in topologically sorted order
    should check against circuits in graphs
    """
    mark = {}
    for node in nodes:
        mark[node] = State.NONE
    L = []
    def visit(node):
        if mark[node] == State.PERMANENT:
            return
        if mark[node] == State.TEMPORARY:
            sys.exit()  #  STOP if graph has at least one cycle)
        mark[node] = State.TEMPORARY

        for node_m in tree[node]:
            visit(node_m)
        mark[node] = State.PERMANENT
        L.append(node)

    while set(mark.values()) != {State.PERMANENT}:
        # while exists nodes without a permanent mark do
        # select an unmarked node
        node = next((k for k, v in mark.items() if v != State.PERMANENT))
        visit(node)
    L.reverse()
    return L


def count_paths(graph, order, start, end):
    # Initialize table
    paths = {u: 0 for u in order}
    paths[end] = 1     # exactly 1 path from end→end

    # process in reverse topological order
    for u in reversed(order):
        # print('Processing ',u)
        for v in graph.get(u, []):
            paths[u] += paths[v]
        # print(paths)
    return paths[start]

def part1(tree):
    return dfs_recursive(tree, 'you', 0, visited=None)

def part2(lines):
    pass

test_data = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

if __name__=="__main__":

    test = False
    text_file = read_data(test=test)
    lines = [line.rstrip() for line in text_file.readlines()]
    tree, nodes = parse_input(lines)

    order = topological_sort(tree, nodes)
    # print(f"{order=}")
    print(count_paths(tree, order, 'you', 'out'))

    print(count_paths(tree, order, 'svr', 'fft') 
          * count_paths(tree, order, 'fft', 'dac')
          * count_paths(tree, order, 'dac', 'out')
          + count_paths(tree, order, 'svr', 'dac') 
          * count_paths(tree, order, 'dac', 'fft')
          * count_paths(tree, order, 'fft', 'out'))



