import re
import string
from aocd.models import Puzzle


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=6)

    # input is a long string
    input = puzzle.input_data
    # for testing
    # input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    for i, letters in enumerate(zip(input,input[1:],input[2:],input[3:])):
        if len(set(letters)) == 4:
            break
    print("Problem 1: ", i+4)
    
    # a second solution, avoiding zips
    for i in range(len(input)):
        if len(set(input[i:i+4])) == 4:
            break
    print("Problem 1: ", i+4)

    # And now using that for 14 letters for problem 2
    for i in range(len(input)):
        if len(set(input[i:i+14])) == 14:
            break
    print("Problem 2: ", i+14)
