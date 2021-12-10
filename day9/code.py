from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
  
from itertools import tee, islice, chain

def sizeof(name,array):
    print(name,' is ',len(array),",",len(array[0]))
    print()

def previous_and_next_list(some_list):
    peek = some_list[0]
    L = len(peek)

    prevs, items, nexts = tee(some_list, 3)
    prevs = chain([L*[None]], prevs)
    nexts = chain(islice(nexts, 1, None), [L*[None]])
    return zip(prevs, items, nexts)

def previous_and_next_item(iter1, iter2, iter3):
    prevs1, items1, nexts1 = tee(iter1, 3)
    prevs1 = chain([None], prevs1)
    nexts1 = chain(islice(nexts1, 1, None), [None])

    prevs2, items2, nexts2 = tee(iter2, 3)
    prevs2 = chain([None], prevs2)
    nexts2 = chain(islice(nexts2, 1, None), [None])

    prevs3, items3, nexts3 = tee(iter3, 3)
    prevs3 = chain([None], prevs3)
    nexts3 = chain(islice(nexts3, 1, None), [None])

    return zip(items1, prevs2, nexts2, items3, items2)

def lt(a, b):
    if b is None:
        return True
    else:
        return a<b

def risk(item1, prev2, next2, item3, item2):
    if (lt(item2,item1) and lt(item2,prev2) and lt(item2,next2) and lt(item2,item3)):
        return(item2+1)
    else:
        return 0

def dfs(m,n):
        cnt = 0
        if not visited[m-1][n]:
            # print(m-1,n)
            visited[m-1][n] = True
            cnt += 1
            cnt += dfs(m-1,n)
        if not visited[m][n-1]:
            # print(m,n-1)
            visited[m][n-1] = True
            cnt += 1
            cnt += dfs(m,n-1)
        if not visited[m][n+1]:
            # print(m,n+1)
            visited[m][n+1] = True
            cnt += 1
            cnt += dfs(m,n+1)
        if not visited[m+1][n]:
            # print(m+1,n)
            visited[m+1][n] = True
            cnt += 1
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


