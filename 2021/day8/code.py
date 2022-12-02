from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
  
@dataclass
class Point:
    x: int=0
    y: int=0

@dataclass
class Line:
    a: Point()
    b: Point()

    def diag_up(self):
        return (self.b.x-self.a.x) == (self.b.y-self.a.y)

    def diag_down(self):
        return (self.b.x-self.a.x) == (self.a.y-self.b.y)

    def horizontal(self):
        return (self.a.y == self.b.y)

    def vertical(self):
        return (self.a.x == self.b.x)

    def fill(self):
        if self.horizontal():
            lst = sorted([self.a.x, self.b.x])
            return list(zip(list(range(lst[0],lst[-1]+1)), cycle([self.a.y])))
        elif self.vertical():
            lst = sorted([self.a.y, self.b.y])
            return list(zip(cycle([self.a.x]), list(range(lst[0],lst[-1]+1))))
        elif self.diag_up():
            lstx = sorted([self.a.x, self.b.x])
            lsty = sorted([self.a.y, self.b.y])
            return list(zip(list(range(lstx[0],lstx[-1]+1)), list(range(lsty[0],lsty[-1]+1))))
        elif self.diag_down():
            lstx = sorted([self.a.x, self.b.x])
            lsty = sorted([self.a.y, self.b.y])
            return list(zip(list(range(lstx[0],lstx[-1]+1)), list(range(lsty[-1],lsty[0]-1,-1))))

        else:
            return []

def find_digit(d, one, seven, four):
    # print('XXX',d)
    bars = set()
    for x in d: bars.add(x)
    cross = four - one
    if len(bars)==2: return 1
    if len(bars)==3: return 7
    if len(bars)==4: return 4
    if len(bars)==7: return 8
    if len(bars)==6:  # 0, 6, 9
        if len(cross - bars) > 0: return 0
        if len(one - bars) > 0: return 6
        return 9
    if len(bars)==5: # 2,3,5
        # print(f'{one=}')
        # print(f'{four=}')
        # print(f'{seven=}')
        # print(f'{cross=}')
        # cmb = cross-bars
        # print(f'{cmb=}')
        if len(cross-bars)==0: return 5
        if len(one-bars)==0: return 3
        return 2


# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    keys = range(10)
    segments = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
    digits = dict(zip(keys, segments))

    cnt = 0
    sum = 0
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            inp, output = line.strip().split('|')
            inp_digits = inp.strip().split(' ')
            out_digits = output.strip().split(' ')
            one = set()
            four = set()
            seven = set()
            for d in inp_digits + out_digits:
                if len(d)==2:
                    for x in d:
                        one.add(x)
                if len(d)==3:
                    for x in d:
                        seven.add(x)
                if len(d)==4:
                    for x in d:
                        four.add(x)
            N = 0
            for d in out_digits:
                N = 10*N + find_digit(d, one, seven, four)
            sum += N
        print(sum)