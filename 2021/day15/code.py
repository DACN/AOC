from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
import copy
  
from itertools import tee, islice, chain

def dfs(m,n, path, cst):
        if m==len(flows) and n==len(flow[0]):
            costs[tuple(path)] = cst
            return
        try:
            flows[m-1][n]
            if not (m-1,n) in path:
                path.append((m-1,n))
                cst += flows[m-1][n]
                dfs(m-1,n, path, cst)
                path.pop()
                cst -= flows[m-1][n]
        except:
            pass
        #
        try:
            flows[m+1][n]
            if not (m+1,n) in path:
                path.append((m+1,n))
                cst += flows[m+1][n]
                dfs(m-1,n, path, cst)
                path.pop()
                cst -= flows[m+1][n]
        except:
            pass
        #
        try:
            flows[m][n-1]
            if not (m,n-1) in path:
                path.append((m,n-1))
                cst += flows[m][n-1]
                dfs(m,n-1, path, cst)
                path.pop()
                cst -= flows[m][n-1]
        except:
            pass
        #
        try:
            flows[m][n+1]
            if not (m,n+1) in path:
                path.append((m,n+1))
                cst += flows[m][n+1]
                dfs(m,n+1, path, cst)
                path.pop()
                cst -= flows[m][n+1]
        except:
            pass


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

    path = [(0,0)]
    cst = 0
    costs = {}
    dfs(0,0,path,cst)
