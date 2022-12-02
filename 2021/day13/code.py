from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
import copy
  
from itertools import tee, islice, chain

def foldy(page, Y):
    new_page = copy.deepcopy(page)
    for y in range(Y):
        for x in range(len(page[0])):
            new_page[y][x] = 'X' if page[y][x]=="X" else page[2*Y-y][x]
    return new_page[:Y]

def foldx(page, X):
    new_page = []
    for line in page:
        new_line = copy.deepcopy(line)
        # print()
        # print(new_line)
        for x in range( X):
            new_line[x] = 'X' if line[x]=="X" else line[2*X-x]
        # print(new_line[:X])
        new_page.append(new_line[:X])
        # print()
    return new_page


def how_many_dots(page):
    sumd = 0
    for line in page:
        sumd += sum([1 for q in line if q == "X"])
    return sumd


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

    dots = []
    with open(sys.argv[1]) as fin:
        lines =  fin.readlines()
    max_x, max_y = 0,0
    for line in lines:
        if len(line.strip()) == 0:
            break
        x,y = line.split(',')
        max_x = max(int(x),max_x)
        max_y = max(int(y),max_y)

    folds = []
    for line in lines:
        if line.startswith("fold along x"):
            fold,x = line.strip().split('=')
            folds.append(['x',int(x)])
        if line.startswith("fold along y"):
            fold,y = line.strip().split('=')
            folds.append(['y',int(y)])

    page = []
    for y in range(max_y+1):
        page.append((max_x+1)*['.'])
    for line in lines:
        if len(line.strip()) == 0:
            break
        x,y = line.split(',')
        page[int(y)][int(x)] = 'X'

    for instruction in folds:
        if instruction[0] == 'x':
            page = foldx(page, instruction[1])
        if instruction[0] == 'y':
            page = foldy(page, instruction[1])
        print(how_many_dots(page))
    for line in page:
        print(''.join(line))