from dataclasses import dataclass, field
import sys
from collections import defaultdict, Counter
from itertools import cycle
import re
import copy

from itertools import tee, islice, chain


def update_template(template):
    new_template = template[0]
    for l,r in zip(template, template[1:]):
        new_template += maps[l+r] + r
    return new_template

def most_minus_least(template):
    c = Counter(template)
    mx = max(c, key=c.get)
    mn = min(c, key=c.get)
    return c[mx] - c[mn]

def most_minus_least_pairs(pairs, last_letter):
    counts = defaultdict(int)
    counts[last_letter] = 1
    for k in pairs.keys():
        counts[k[0]] += pairs[k]
    mx = max(counts, key=counts.get)
    mn = min(counts, key=counts.get)
    return counts[mx] - counts[mn]

# @dataclass
# class Template:
#     pairs: dict = field(default_factory=lambda: defaultdict(int))
#     last_letter: str = field(default="")

# def template_from_string(s):
#     t = Template()
#     for l,r in zip(template, template[1:]):
#         t.pairs[l+r] += 1
#     t.last_letter = s[-1]
#     return t

# def update_template_2(t):
#     new_t = Template()
#     for p in t.pairs.keys():
#         if p in maps:
#             L = p[0] + maps[p]
#             R = maps[p] + p[1]
#             new_t.pairs[L] += t.pairs[L]
#             new_t.pairs[R] += t.pairs[R]
#         else:
#             new_t.pairs[p] += t.pairs[p]
#     new_t.last_letter = t.last_letter
#     return new_t

def update_pairs(pairs):
    new_pairs = defaultdict(int)
    for p in list(pairs.keys()):
        # print(p,pairs)
        if p in maps:
            L = p[0] + maps[p]
            R = maps[p] + p[1]
            new_pairs[L] += pairs[p]
            new_pairs[R] += pairs[p]
        else:
            new_pairs[p] += pairs[p]
    return new_pairs


# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()


    nsteps = 40
    maps = defaultdict(str)
    with open(sys.argv[1]) as fin:
        template =  next(fin).strip()
        for line in fin:
            if len(line.strip()) == 0:
                continue
            pair, to = line.split('->')
            pair, to = pair.strip(), to.strip()
            maps[pair] = to

    # t = template_from_string(template)
    # print(t)

    pairs = defaultdict(int)
    last_letter = template[-1]

    for l,r in zip(template, template[1:]):
        pairs[l+r] += 1

    for n in range(nsteps):
        # template = update_template(template)
        pairs = update_pairs(pairs)

    # print(most_minus_least(template))
    print(most_minus_least_pairs(pairs, last_letter))




