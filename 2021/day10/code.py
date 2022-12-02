from dataclasses import dataclass
import sys
from collections import defaultdict
from itertools import cycle
import re
import statistics
  
from itertools import tee, islice, chain


def stack_v(s):
    v = 0
    for c in s:
        v = 5*v
        v += points2[c]
    return v

# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    flows = []
    opening = ["(", "[", "{", "<"]
    closing = [")", "]", "}", ">"]
    c_points = [3, 57, 1197, 25137]
    d_points = [1, 2,3, 4]

    pairs = list(zip(opening,closing))
    points = dict(zip(closing, c_points))
    points2 = dict(zip(opening, d_points))

    total = 0
    completion = []
    with open(sys.argv[1]) as fin:
        for line in fin:
            if len(line.strip()) == 0:
                continue
            stack = []
            mismatched = False
            for c in line:
                if c in opening:
                    stack.append(c)
                elif c in closing:
                    b = stack.pop()
                    if (b,c) in pairs:
                        pass
                    else:
                        mismatched = True
                        # print(':',stack)
                        # print("mismatched", b)
                        # print("Found ", c, "should have been close to ", b)
                        total += points[c]
                        break

            if not mismatched and stack != []:
                print('>',''.join(reversed(stack)), stack_v(''.join(reversed(stack))))
                completion.append(stack_v(''.join(reversed(stack))))
        print(statistics.median(completion))
