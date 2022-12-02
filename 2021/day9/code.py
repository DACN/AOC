from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
  
from itertools import tee, islice, chain


def dfs(m,n):
        if m = len(visited) and n==len(visited[0]):
            return 0
        cnt = flows[m][n]
        if not visited[m-1][n]:
            # print(m-1,n)
            visited[m-1][n] = True
            cnt += dfs(m-1,n)
        if not visited[m][n-1]:
            # print(m,n-1)
            visited[m][n-1] = True
            cnt += dfs(m,n-1)
        if not visited[m][n+1]:
            # print(m,n+1)
            visited[m][n+1] = True
            cnt += dfs(m,n+1)
        if not visited[m+1][n]:
            # print(m+1,n)
            visited[m+1][n] = True
            cnt += dfs(m+1,n)
        return cnt

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

    sum = 0
    for prev_line, line, nxt_line in previous_and_next_list(flows):
        for item1, prev2, next2, item3, item2 in previous_and_next_item(prev_line, line, nxt_line):
            sum +=  risk(item1, prev2, next2, item3, item2)
    print(sum)


    flows = []
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            line_ints = []
            for x in line.strip():
                line_ints.append(int(x))
            flows.append(line_ints)
    flows2 = []
    flows2.append((len(flows[0])+2)*[None])
    for line in flows:
        flows2.append([None]+line+[None])
    flows2.append((len(flows[0])+2)*[None])
    M = len(flows2)-1
    N = len(flows2[0])-1
    sum = 0
    for m in range(1,M):
        for n in range(1,N):
            sum += risk(flows2[m-1][n], flows2[m][n-1], flows2[m][n+1], flows2[m+1][n], flows2[m][n],)
    print(sum)

    visited = []
    visited.append((len(flows[0])+2)*[True])
    for M in range(1,M):
        visited.append([True]+len(flows[0])*[False]+[True])
    visited.append((len(flows[0])+2)*[True])
    for m in range(len(visited)):
        for n in range(len(visited[0])):
            if flows2[m][n]==9:
                visited[m][n] = True

    sizes = []
    for m in range(len(visited)):
        for n in range(len(visited)):
            if not visited[m][n]:
                sizes.append(dfs(m,n))
    sizes.sort(reverse=True)
    print(sizes)
    print(sizes[0]*sizes[1]*sizes[2])


