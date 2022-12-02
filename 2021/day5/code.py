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


# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    Cnt = defaultdict(int)
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            ab = line.strip().split('->')
            a = list(map(int,ab[0].split(',')))
            b = list(map(int,ab[1].split(',')))
            L = Line(Point(*a), Point(*b))
            for p in L.fill():
                Cnt[p] += 1
    dups = [k for k,v in Cnt.items() if v > 1]
    print(len(dups))