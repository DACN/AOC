import functools
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
from typing import NamedTuple

test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

class Node(NamedTuple):
    valve: str
    visited: bool
    minutes: int

class Neighbour(NamedTuple):
    valve: str
    dist: int

class Valve(NamedTuple):
    flow: int
    neighbours: list[Neighbour]


def parse_input_line(line):
    return re.search(r'Valve ([A-Z]+).*?=(\d+).*valves? (.*)', line).groups()


def Floyd_Warshall(dist):
    # dist is a be a |V| × |V| array of minimum distances initialized to ∞ (infinity)
    # for each edge (u, v) do
    # dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
    # for each vertex v do
    # dist[v][v] ← 0
    for k in range(len(dist)):
        for i in range(len(dist)):
            for j in range(len(dist)):
                if dist[i][j] > dist[i][k] + dist[k][j]: 
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

if __name__=="__main__":

    EXAMPLE = True
    puzzle = Puzzle(year=2022, day=16)
    input = puzzle.input_data.split('\n')
    if EXAMPLE:
        input = test_data.split('\n')
    valves = {}
    for line in input:
        valve, flow, connections = parse_input_line(line)
        flow = int(flow)
        valves[valve] = (flow, connections.split(", "))

    non_zero = set()
    index = {}
    N = len(valves)
    for n,k in enumerate(valves.keys()):
        index[k] = n

    dist = [N*[math.inf] for i in range(N)]
    for i, (k,v) in enumerate(valves.items()):
        if k=="AA" or v[0] > 0:
            non_zero.add(k)
        dist[i][i] = 0
        for l in v[1]:
            dist[i][index[l]] = 1
            dist[index[l]][i] = 1

    dist = Floyd_Warshall(dist)
    cvalves = {}
    for k in non_zero:
        cvalves[k] = Valve(flow=valves[k][0], 
                           neighbours=[Neighbour(k2, dist[index[k]][index[k2]]) for k2 in non_zero if k2 != k])
        print(k, cvalves[k])

first_node = Node(valve="AA", visited=True, minutes=30)

