import re
from aocd.models import Puzzle
import timeit
from dataclasses import dataclass
import dataclasses
import sys


test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

@dataclass
class Point:
    x: int 
    y: int 

def tail_follow(head, tail, debug=None):
    if (abs(head.y-tail.y)+abs(head.x-tail.x)==1):  # one apart
        pass
    elif (abs(head.y-tail.y)==1) and (abs(head.x-tail.x)==1):  # diagonal
        pass
    elif head.x==tail.x:  # same vertical
        tail.y = (head.y+tail.y)//2
    elif head.y==tail.y:  # same horizontal
        tail.x = (head.x + tail.x) // 2
    elif (abs(head.y-tail.y)==1) and (abs(head.x-tail.x)==2):
        tail.y = head.y 
        tail.x = (head.x + tail.x) // 2
    elif (abs(head.y-tail.y)==2) and (abs(head.x-tail.x)==1):
        tail.x = head.x 
        tail.y = (head.y + tail.y) // 2
    elif (abs(head.y-tail.y)==2) and (abs(head.x-tail.x)==2):  # THIS NEEDED FOR MOVE10!
        tail.x = (head.x + tail.x) // 2
        tail.y = (head.y + tail.y) // 2
    else:
        print('ARGH')
        if debug:
            print(debug)
        print(head)
        print(tail)
        sys.exit()


def visualise(head, tail):
    # used for checking against test examples
    line = 6*['.']
    grid = []
    for i in range(5):
        grid.append(line.copy())
    grid[0][0]='s'
    grid[tail.y][tail.x] = 'T'
    grid[head.y][head.x] = 'H'
    for line in grid[::-1]:
        print(''.join(line))
    print()

def visualise10(head, tail1, tail2, tail3, tail4, tail5, tail6, tail7, tail8, tail9):
    # used for checking against test examples
    line = 6*['.']
    grid = []
    for i in range(5):
        grid.append(line.copy())
    grid[0][0]='s'
    grid[tail9.y][tail9.x] = '9'
    grid[tail8.y][tail8.x] = '8'
    grid[tail7.y][tail7.x] = '7'
    grid[tail6.y][tail6.x] = '6'
    grid[tail5.y][tail5.x] = '5'
    grid[tail4.y][tail4.x] = '4'
    grid[tail3.y][tail3.x] = '3'
    grid[tail2.y][tail2.x] = '2'
    grid[tail1.y][tail1.x] = '1'
    grid[head.y][head.x] = 'H'
    for line in grid[::-1]:
        print(''.join(line))
    print()


def move_one(point, direction):
    match direction:
        case "R":
           point.x +=1
        case "L":
           point.x -=1
        case "U":
           point.y +=1
        case "D":
           point.y -=1
    return
 
def move(head, tail, direction, number, covered):
    if visual:
        print("==",direction,number,"==\n")
    for i in range(number):
        move_one(head, direction)
        tail_follow(head, tail)
        if visual:  # global variable about visualising
            visualise(head, tail)
        covered.append(dataclasses.replace(tail))
 
def move10(head, tail1, tail2, tail3, tail4, tail5, tail6, tail7, tail8, tail9, direction, number,covered):
    if visual:
        print("==",direction,number,"==\n")
    for i in range(number):
        move_one(head, direction)
        tail_follow(head, tail1, 'H1')
        tail_follow(tail1, tail2, '12')
        tail_follow(tail2, tail3, '23')
        tail_follow(tail3, tail4, '34')
        tail_follow(tail4, tail5, '45')
        tail_follow(tail5, tail6, '56')
        tail_follow(tail6, tail7, '67')
        tail_follow(tail7, tail8, '78')
        tail_follow(tail8, tail9, '89')
        if visual:  
            visualise10(head, tail1, tail2, tail3, tail4, tail5, tail6, tail7, tail8, tail9)
        covered.append(dataclasses.replace(tail9))


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=9)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    visual = False

    head = Point(0,0)
    tail = Point(0,0)

    covered = [Point(0,0)]
    for line in input:
        direction, number = line.split()
        number = int(number)
        move(head,tail,direction,number,covered)

    cover = {(p.x,p.y) for p in covered}
    print('Problem 1', len(set(cover)))

    head = Point(0,0)
    tail1 = Point(0,0)
    tail2 = Point(0,0)
    tail3 = Point(0,0)
    tail4 = Point(0,0)
    tail5 = Point(0,0)
    tail6 = Point(0,0)
    tail7 = Point(0,0)
    tail8 = Point(0,0)
    tail9 = Point(0,0)

    covered = [Point(0,0)]
    for line in input:
        direction, number = line.split()
        number = int(number)
        move10(head, tail1, tail2, tail3, tail4, tail5, tail6, tail7, tail8, tail9, direction, number, covered)
    cover = {(p.x,p.y) for p in covered}
    print('Problem 2', len(set(cover)))
