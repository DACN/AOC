from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
  
from itertools import tee, islice, chain



def dfs(nodefrom, stack):
        cnt = 0
        for nodeto in links[nodefrom]:
            if nodeto=="end":
                cnt += 1
                stack.append('end')
                print('Found', stack)
                stack.pop()
            else:
                lowers = [x for x in set(stack) if x.islower()]
                if (nodeto.islower() and
                    ((nodeto in stack) and (2 in [stack.count(x) for x in lowers])
                     or stack.count(nodeto)==2)):
                    pass
                else:
                    stack.append(nodeto)
                    # print(f"Examining {stack}")
                    cnt += dfs(nodeto, stack)
                    stack.pop()
        return cnt

# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    nodes = []
    links = defaultdict(list)
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            ndfrom,ndto = line.strip().split('-')
            nodes.append(ndfrom)
            nodes.append(ndto)
            if not ndfrom in {'end'} and not ndto in {'start'}:
                links[ndfrom].append(ndto)
            if not ndto in {'end'} and not ndfrom in {'start'}:
                links[ndto].append(ndfrom)
    for k,v in links.items():
        print(k,v)
    print()

    print(dfs('start', ['start']))

