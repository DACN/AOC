import functools
import math
import re
from aocd.models import Puzzle
import timeit
from functools import cmp_to_key
from dataclasses import dataclass
import dataclasses
import sys
import timeit
import json

test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

@functools.total_ordering
class Range:
    ''' a finite interval '''
    def __init__(self, d_from, d_to_closed=None):
        self.d_from = d_from
        self.d_to_closed = d_to_closed
        self.d_to = None
        #         
        if self.d_to_closed is not None:
            self.d_to = self.d_to_closed + 1

    def __key(self):
        return (self.d_from, self.d_to, self.d_to_closed)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "[{0},{1})".format(self.d_from, self.d_to)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()

    def __lt__(self, other):
        '''sort based on lower then upper bound, empty interval at top'''
        def key(x, y):
            ''' key allows sorting of empty intervals'''
            import math
            return (x if x is not None else math.inf, y)
        return key(self.d_from, self.d_to) < key(other.d_from, other.d_to)

    def __mul__(self, y):
        '''Range intersection - deals with empty Periods'''
        # first if there is an empty Period, checking None at the lower end
        if (self.d_from is None) or (y.d_from is None):
            return Range(None, None)
        else:
            m = max([self.d_from, y.d_from])
            n = min([self.d_to_closed, y.d_to_closed])
            return Range(m, n)

    @classmethod
    def empty(cls):
        """returns an empty Range"""
        return Range(None, None)

    def len(self):
        ''' Returns length of an Range''' 
        if self.d_from is None:
            return 0
        else:
            return self.d_to - self.d_from

    def overlaps(self, second_Period):
        ''' lets us see if there is an overlap
            EMPTY Period does not overlap'''
        z = self * second_Period
        return z.len() > 0

    def adjoins(self, second_Period):
        ''' lets us see if the Periods adjoin one another
            OVERLAP gives a False
            The EMPTY Period adjoins EVERYTHING (convention chosen to allow join of an empty period)'''
        return ((self.d_to == second_Period.d_from) or
                (self.d_from == second_Period.d_to) or
                (self.d_from is None) or
                (second_Period.d_from is None))

    def join(self, y):
        ''' join two overlapping or adjoint Periods'''
        # first check the Periods are overlapping or adjoing
        if not (self.overlaps(y) or self.adjoins(y)):
            raise PeriodError('Periods are totally disjoint')
        #
        # one or two of the periods are empty, return the other periods
        if self.d_from is None:
            return y
        elif y.d_from is None:
            return self
        # we have a substantive join/overlap    
        else:
            m = min(a for a in [self.d_from, y.d_from])
            n = max(a for a in [self.d_to_closed, y.d_to_closed])
            return Range(m, n)


class RangeSet:
    '''Class for a list or Ranges - an list of Ranges'''
    empty = Range(None, None)

    def __init__(self, items):
        """Initializes a RangeSet"""
        self._Ranges = []
        for i in items:
            self._add(i)
        self._Ranges.sort()

    def _add(self, r):
        """Adds a Range to a RangeSet"""
        assert isinstance(r, Range), 'we must be adding an Range: ' + str(r)
        #
        #   xxxxxxxxx  xxxxxx   xxxxx
        #         xxxxxxxxxxxxxxxxxxxxxx
        if r != Range.empty():  # Don't bother appending an empty Range
            newRanges = []
            for i in self._Ranges:
                if i.overlaps(r) or i.adjoins(r):
                    r = r.join(i)
                else:
                    newRanges.append(i)
            newRanges.append(r)
            self._Ranges = newRanges
            self._Ranges.sort()

    def len(self):
        if self._Ranges != []:
            return sum(r.len() for r in self._Ranges)
        else:
            return 0 

    def parts(self):
        return len(self._Ranges)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        """Returns the number of Ranges contained in the object        """
        return len(self._Ranges)

    def __str__(self):
        """Returns a string representation of the object"""
        if len(self._Ranges) == 0:
            rangeStr = "<Empty>"
        else:
            rangeStr = "(" + ",".join([r.__str__() for r in self._Ranges]) + ")"
        return rangeStr

    def __getitem__(self, index):
        """Gets the Range at the given index
        RangeSets have a natural ordering.
        """
        try:
            return self._Ranges[index]
        except IndexError:
            raise IndexError("Index is out of range")


def parse_input_line(line):
    return [int(m) for m in re.search(r'\bx=(-?\d+).*?y=(-?\d+).*?(-?\d+).*?y=(-?\d+)', line).groups()]


def array_size(input):
    minx =  1_000_000
    maxx = -1_000_000
    miny =  1_000_000
    maxy = -1_000_000
    for line in input:
        sx,sy, bx,by = parse_input_line(line)
        minx = min(minx, sx, bx)
        maxx = max(maxx, sx, bx)
        miny = min(miny, sy, by) 
        maxy = max(maxy, sy, by)
    return (minx,maxx),(miny,maxy)

def manhattan(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

if __name__=="__main__":

    look_at_row = 2000000
    # look_at_row = 10
    beacons = []
    puzzle = Puzzle(year=2022, day=15)
    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    rows = []
    (minx,maxx),(miny,maxy) = array_size(input)
    for line in input:
        sx,sy, bx,by = parse_input_line(line)
        dist = manhattan((sx, sy), (bx, by))
        beacons.append((bx,by))
        up = abs(look_at_row - sy)
        if up<dist:
            r = Range(sx-(dist-up), sx+(dist-up))
            rows.append(r)
        else:
            r = None
        beacons_in_row = len([(bx, by) for (bx, by) in set(beacons) if by==look_at_row])
    print('Part 1:',RangeSet(rows).len()-beacons_in_row)
 
    start = timeit.default_timer()
    rows = [[] for y in range(4000001)]
    for line in input:
        sx,sy, bx,by = parse_input_line(line)
        dist = manhattan((sx, sy), (bx, by))
        beacons.append((bx,by))
        for look_at_row in range(4000001):
        # for look_at_row in range(21):
            up = abs(look_at_row - sy)
            if up<dist:
                r = Range(sx-(dist-up), sx+(dist-up))
                rows[look_at_row].append(r)
            else:
                r = None
        beacons_in_row = len([(bx, by) for (bx, by) in set(beacons) if by==look_at_row])
    for n in range(4000001):
    # for n in range(21):
        if RangeSet(rows[n]).parts() > 1:
            y = n
            x = RangeSet(rows[n])._Ranges[0].d_to
            print('Part 2',4000000*x+y)
    print("Time=", timeit.default_timer()-start)
