import io
from aocd import get_data
import re
import itertools
import math
from collections import defaultdict
from collections import Counter
import time

def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=8,year=2025)
        text_file = io.StringIO(data)
    return text_file

def parse_string_numbers(s):
    return list(map(int, re.findall(r"[-+]?\d+", s)))

def replace_char(string, n, new_char):
    """Replace character at index n in string string with new_char."""
    if n < 0 or n >= len(string):
        pass
    return string[:n] + new_char + string[n+1:]


def part1(nodes, num_connections, p1):
    d2 = {}
    distance = {}
    # connected = defaultdict(lambda: False)
    connected = {}
    groups = defaultdict(int)
    max_group = 0
    for m,node1 in enumerate(nodes):
        connected[m] = False
        for n,node2 in enumerate(nodes[m+1:],start=m+1):
            d2[(m,n)] = (node1[0]-node2[0])**2+(node1[1]-node2[1])**2+(node1[2]-node2[2])**2 
            # print(m,n,nodes[m], nodes[n],d2[(m,n)])
            distance[d2[(m,n)]] = (m,n)
    distance_sorted = dict(sorted(d2.items(),key=lambda item: item[1]))

    # for k,item in distance_sorted.items():
    #     print(k, item)
    # print("------")
    for n,k in enumerate(distance_sorted.keys(), start=1):
        # print(k, distance_sorted[k])
        if connected[k[0]] and not connected[k[1]]:
            group = groups[k[0]]
            connected[k[1]] = True
            groups[k[1]] = group
            lastx_product = nodes[k[0]][0]*nodes[k[1]][0]
        elif connected[k[1]] and not connected[k[0]]:
            group = groups[k[1]]
            connected[k[0]] = True
            groups[k[0]] = group
            lastx_product = nodes[k[0]][0]*nodes[k[1]][0]
        elif not connected[k[0]] and not connected[k[1]]:
            max_group += 1
            connected[k[0]] = True
            connected[k[1]] = True
            groups[k[0]] = max_group
            groups[k[1]] = max_group
            lastx_product = nodes[k[0]][0]*nodes[k[1]][0]
        elif connected[k[0]] and connected[k[1]] and groups[k[0]]==groups[k[1]]:
            pass
            # print(k[0], nodes[k[0]], groups[k[0]])
            # print(k[1], nodes[k[1]], groups[k[1]])
        elif connected[k[0]] and connected[k[1]] and groups[k[0]]!=groups[k[1]]:
            old_group = groups[k[1]]
            new_group = groups[k[0]]
            # for kk in range(len(nodes)):
            #     print(kk, nodes[kk], groups[kk])
            # print('joining', nodes[k[0]][0], nodes[k[1]][0] )
            # print()
            lastx_product = nodes[k[0]][0]*nodes[k[1]][0]
            for m in range(len(nodes)):
                if connected[m] and old_group==groups[m]:
                    groups[m] = new_group
            # print('merging')
        if n==num_connections:
            # This is how we get out of the loop for part 1
            break
        if all(connected.values()):
            # print(connected)
            if len(set(groups.values()))==1:
                break
    # print('groups = ', max_group)
    # print()
    # for m,node in enumerate(nodes):
    #     if connected[m]:
    #         print(m, nodes[m], groups[m])
    #     else:
    #         print(m, '-') 
    if p1:
        return math.prod(sorted(Counter(list(groups.values())).values())[-3:])
    else:
        return lastx_product


test_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


if __name__=="__main__":

    test = False
    p1 = True
    text_file = read_data(test=test)
    lines = [line.rstrip() for line in text_file.readlines()]
    nodes = [parse_string_numbers(line) for line in lines]

    num_connections = 10 if test else 1000
    seconds = time.time()
    print("part 1 ", part1(nodes, num_connections, True))
    print(time.time()-seconds)

    num_connections = math.inf 
    seconds = time.time()
    print("part 2 ", part1(nodes, num_connections, False))
    print(time.time()-seconds)
