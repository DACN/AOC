# import utils
from typing import NamedTuple
from collections import defaultdict
import re

SAMPLE = True
# inp = utils.get_input(day=16).strip()
if SAMPLE:
    inp = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

ptn = re.compile(r"Valve ([a-zA-Z]+) has flow rate=(\d+); (?:tunnels lead|tunnel leads) to valves? (.+)")

class State(NamedTuple):
    curr_pos: str
    m_left: int
    enabled: int
    elephant: bool = False

    def __str__(self):
        return f"State({self.curr_pos=}, {self.m_left=:02d}, enabled={bin(1<<17 ^ self.enabled)}), {self.elephant=}"


class CleanedValue(NamedTuple):
    frate: int
    valve_num: int
    neighbours: list[tuple[str, int]]


valves = {}
for i, row in enumerate(inp.split("\n")):
    valve, frate, connections = re.findall(ptn, row)[0]
    frate = int(frate)
    valves[valve] = (frate, connections.split(", "))
for v in valves:
    print(v, valves[v])
# Horrible O(n^3) step to find shortest distance to all nodes for nodes with frate > 0
D = defaultdict(lambda: float("inf"))
to_save = set()
for k, v in valves.items():
    if v[0] > 0:
        to_save.add(k)
    D[(k, k)] = 0
    for n in v[1]:
        D[(k, n)] = 1
        D[(n, k)] = 1
for k in valves:
    for b in valves:
        for c in valves:
            D[(b, c)] = min(D[(b, c)], D[(b, k)] + D[(k, c)])
print(D)

cvalves = {}
for i, k in enumerate(to_save):
    v = valves[k]
    neighbours = [(k2, D[k, k2]) for k2 in to_save if k2 != k]
    cvalves[k] = CleanedValue(frate=v[0], valve_num = 1<<i, neighbours=neighbours)

print(f"{to_save=}")
print(D)
for k in cvalves:
    print(k, cvalves[k])
halt()

if "AA" not in cvalves:
    # If the starting valve is 0 weight then add it as a dummy valve just so things work
    neighbours = [(k, D["AA", k]) for k in to_save]
    cvalves["AA"] = CleanedValue(frate=0, valve_num=0, neighbours=neighbours)

first_state = State(curr_pos="AA", m_left=30, enabled=0, elephant=False)
first_state_2 = State(curr_pos="AA", m_left=26, enabled=0, elephant=True)
# Horrible global memo because I hate good programming practice
MEMO: dict[State, int] = {}

def make_move(state: State, cvalves: dict[str, CleanedValue]) -> int:
    if state in MEMO:
        return MEMO[state]

    m_score = 0
    if state.m_left <= 0:
        MEMO[state] = m_score
        return m_score

    # Observation: The elephant can never do better than having 26 minutes active starting at the state you're leaving the valves
    if state.elephant:
        elephant_state = State(curr_pos="AA", m_left=26, enabled=state.enabled, elephant=False)
        e_score = make_move(elephant_state, cvalves)
    else:
        e_score = 0

    v = cvalves[state.curr_pos]
    if not (state.enabled & v.valve_num) and v.frate:
        new_state = State(curr_pos=state.curr_pos, m_left=state.m_left - 1, enabled=(state.enabled | v.valve_num), elephant=state.elephant)
        m_score = max(make_move(new_state, cvalves) + (v.frate * new_state.m_left), m_score)
    for v_, d in v.neighbours:
        if d < state.m_left:
            new_state = State(curr_pos=v_, m_left=state.m_left - d, enabled=state.enabled, elephant=state.elephant)
            m_score = max(make_move(new_state, cvalves), m_score)

    m_score = max(m_score, e_score)
    MEMO[state] = m_score
    return m_score

print(f"Part 1: {make_move(first_state, cvalves)}")
print(f"Part 2: {make_move(first_state_2, cvalves)}")