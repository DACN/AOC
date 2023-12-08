import math
import re
from aocd.models import Puzzle
import timeit
from dataclasses import dataclass
import dataclasses
import sys
import timeit

test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

def find_coords(x, array):
    for row, line in enumerate(array):
        if x in line:
            break
    return row, line.index(x)

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)


def neighbours(point, heights):
    x,y = point
    cand_adjacent_points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    can_visit = []
    for (cx,cy) in cand_adjacent_points:
        try:
            if (cx>=0) and (cy>=0) and (heights[cx][cy] <= heights[x][y] + 1):
                can_visit.append((cx,cy))
        except:
            pass
    return can_visit

def min_in_array(tentative_distanceS, visited):
    BIG = 1_000_000_000

    for row, (line, visits) in enumerate(zip(tentative_distances, visited)):
        for col,(td,v) in enumerate(zip(line, visits)):
            if td < BIG and v=="U":
                cand = (row, col)
                BIG = td
    return cand 

def show(visited, tentative_distances, heights):
    for line in visited:
        print(line[82:89])
    print()
    for line in tentative_distances:
        print(line[82:89])
    print()
    for line in heights:
        print(line[82:89])

def solve():
    n = 0
    while True:
        n += 1
        cx, cy = min_in_array(tentative_distances, visited)
        nbrs = neighbours((cx, cy), heights)
        if nbrs == []:
            # print("stuck")
            show(visited[5:10], tentative_distances[5:10], heights[5:10])
            print(cx, cy)
            halt()
            visited[cx][cy] = "S"
            # halt()
        for px,py in neighbours((cx, cy), heights):
            if visited[px][py] == "U":
                if tentative_distances[cx][cy] + 1 <= tentative_distances[px][py]:
                    tentative_distances[px][py] = tentative_distances[cx][cy] + 1
            visited[cx][cy] = 'V'
        if visited[Ex][Ey] == "V":
            break


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=12)

    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    # get an array of heights and the starting / ending co-ordinates
    Sx, Sy = find_coords('S',input)
    Ex, Ey = find_coords('E',input)
    heights = [[ord(x) for x in line] for line in input]
    heights[Sx][Sy] = ord('a')
    heights[Ex][Ey] = ord('z')

 
    visited = [['U' for i in heights[0]] for line in heights]
    BIG = 1_000_000_000
    tentative_distances = [[BIG for i in line] for line in heights] 
    tentative_distances[Sx][Sy] = 0
    solve()


    print("Problem 1:", tentative_distances[Ex][Ey])

    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    # get an array of heights and the starting / ending co-ordinates
    Sx, Sy = find_coords('S',input)
    Ex, Ey = find_coords('E',input)
    heights = [[ord(x) for x in line] for line in input]
    heights[Sx][Sy] = ord('a')
    heights[Ex][Ey] = ord('z')
    visited = [['U' for i in heights[0]] for line in heights]
    BIG = 1_000_000_000
    tentative_distances = [[BIG if i > ord('a') else 0 for i in line] for line in heights] 
    # show()
    tentative_distances[Sx][Sy] = 0
    solve()
    # show()
    print("Problem 2:", tentative_distances[Ex][Ey])


    

