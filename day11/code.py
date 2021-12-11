from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
import copy
  
from itertools import tee, islice, chain

def step(flows):
    flows2 = copy.deepcopy(flows)
    for m in range(1,M):
        for n in range (1,N):
            flows2[m][n] += 1
    return flows2

def fullstep(flows):
    flows = step(flows)
    flash = zero_flash()
    step_flashes = 0
    while True:
        flashes = 0
        for m in range(1,M):
            for n in range (1,N):
                if flows[m][n] >= 10 and not flash[m][n]:
                    flashes += 1
                    try:
                        flows[m-1][n-1] += 1
                    except:
                        pass
                    try:
                        flows[m-1][n] += 1
                    except:
                        pass
                    try:
                        flows[m-1][n+1] += 1
                    except:
                        pass
                    try:
                        flows[m][n-1] += 1
                    except:
                        pass
                    flash[m][n] = True
                    try:
                        flows[m][n+1] += 1
                    except:
                        pass
                    try:
                        flows[m+1][n-1] += 1
                    except:
                        pass
                    try:
                        flows[m+1][n] += 1
                    except:
                        pass
                    try:
                        flows[m+1][n+1] += 1
                    except:
                        pass
        step_flashes += flashes
        if flashes == 0:
            break
    all_flash = all((flash[m][n] for n in range(1,N) for m in range(1,M)))
    if all_flash:
        print('all_flash at', stps)
        halt()
    for m in range(1,M):
        for n in range (1,N):
            if flows[m][n] >= 10:
                flows[m][n] = 0
    return flows, step_flashes


def aprint(flows):
    for line in flows:
        print(line)

def zero_flash():
    flash = copy.deepcopy(flows)
    for m in range(1,M):
        for n in range (1,N):
            flash[m][n] = False
    return flash

def pad(flows):
    flows2 = []
    flows2.append((len(flows[0])+2)*[None])
    for line in flows:
        flows2.append([None]+line+[None])
    flows2.append((len(flows[0])+2)*[None])
    M = len(flows2)-1
    N = len(flows2[0])-1
    return flows2, M, N

# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    flows = []
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            line_ints = []
            for x in line.strip():
                line_ints.append(int(x))
            flows.append(line_ints)

    flows, M, N = pad(flows)

    sum_flashes = 0
    for stps in range(1,1101):
        flows, n_flashes = fullstep(flows)
        sum_flashes += n_flashes
    aprint(flows)
    print(sum_flashes)

