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

def transpose(commands):
    return [[commands[j][i] for j in range(len(commands))] for i in range(len(commands[0]))]

def command_filter(commands, filter_list):
    filtered_commands = []
    for c in commands:
        if c[:len(filter_list)] == filter_list:
            filtered_commands.append(c)
    return filtered_commands

# Creating object
if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    commands = []
    with open(sys.argv[1]) as fin:
        for line in fin:
            # ignore empty lines, get an double array as a list of the commands, and transpose it
            if len(line.strip()) > 0:
                commands.append(list(line.strip()))

        ox_filter = []
        for i in range(len(commands[0])):
            filtered_commands = command_filter(commands,ox_filter)
            # if we run out of commands
            if len(filtered_commands)==1:
                ox_filter = filtered_commands[0]
                break
            counts = []
            commands_t = transpose(filtered_commands)
            for c in commands_t:
                counts.append(Counter(c))
            ox_filter = ox_filter + ['1'] if counts[i]['1'] >= counts[i]['0'] else ox_filter + ['0']

        co_filter = []
        for i in range(len(commands[0])):
            filtered_commands = command_filter(commands,co_filter)
            # if we run out of commands
            if len(filtered_commands)==1:
                co_filter = filtered_commands[0]
                break
            counts = []
            commands_t = transpose(filtered_commands)
            for c in commands_t:
                counts.append(Counter(c))
            co_filter = co_filter + ['1'] if counts[i]['1'] < counts[i]['0'] else co_filter + ['0']

        ox = int(''.join(ox_filter), 2)
        co = int(''.join(co_filter), 2)
        print(ox_filter)
        print(co_filter)
        print(ox,co,ox*co)