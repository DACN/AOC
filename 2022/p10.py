import re
from aocd.models import Puzzle
import timeit
from dataclasses import dataclass
import dataclasses
import sys


test_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

def test_register(cycle, register):
    if cycle in [20, 60, 100, 140, 180, 220]:
        strengths.append(cycle*register)
    add_to_display(cycle, register)

def add_to_display(cycle, register):
    dp = cycle - 1
    if dp % 40 in [register-1, register, register+1]:
        display[dp] = "#"
        print(dp, "#")
    else:
        display[dp] = " "
        print(dp, ".")

def run_noop(cycle, register):
    cycle += 1
    test_register(cycle, register)
    return cycle, register

def run_addx(line, cycle, register):
    x = int(line.split(' ')[1])  # second item on the line
    cycle += 1
    test_register(cycle, register)
    cycle += 1
    test_register(cycle, register)
    register += x
    return cycle, register


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=10)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    
    strengths = []
    cycle = 0
    register = 1
    display = 240*["."]

    for line in input:
        if line=="noop":
            cycle, register = run_noop(cycle, register)
        elif line.startswith('addx'):
            cycle, register = run_addx(line, cycle, register)
        else:
            print("argh")
            print(line)
            sys.exit()
    print("Problem 1:", sum(strengths))

    for i in range(6):
        print(''.join(display[40*i:40*(i+1)]))