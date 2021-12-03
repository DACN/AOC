from dataclasses import dataclass
import sys
import re
from collections import Counter

@dataclass
class Position:
    forward: int=0
    down: int=0
    aim: int=0

    def __add__(self, right):
        self.vector = []
        return Position(self.forward+right.forward, self.down+right.down, self.aim+right.aim)

# Creating object
if __name__=="__main__":
    commands = []
    with open(sys.argv[1]) as fin:
        for line in fin:
            # get an double array as a list of the commands, and transpose it
            commands.append(list(line.strip()))
            commands_t = [[commands[j][i] for j in range(len(commands))] for i in range(len(commands[0]))]
        # count the 0s and 1s
        counts = []
        for c in commands_t:
            counts.append(Counter(c))
        gamma = ''
        epsilon = ''
        for c in counts:
            gamma = gamma + '0' if c['0'] > c['1'] else gamma + '1'
            epsilon = epsilon + '0' if c['0'] < c['1'] else epsilon + '1'
        gamma = int(gamma,2)
        epsilon = int(epsilon,2)
        print(gamma*epsilon)
