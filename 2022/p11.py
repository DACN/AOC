import re
from aocd.models import Puzzle
import timeit
from dataclasses import dataclass
import dataclasses
import sys


test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

def split_on_empty_lines(s):
    # greedily match 2 or more new-lines, but don't strip lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s)


class Monkey:
    def __init__(self, items, operation, divisible_by, iftrue, iffalse):
        """ Create a new Monkey """
        self.items =  [int(x) for x in re.findall(r'\b\d+\b', items)]
        self.op, self.op_num = re.search(r'old.*?(\+|\*).*?(old|\d+)', operation).groups() 
        self.divisible_by = int(re.search(r'\b(\d+)\b', divisible_by).groups()[0])
        self.iftrue = int(re.search(r'\b(\d+)\b', iftrue).groups()[0])
        self.iffalse = int(re.search(r'\b(\d+)\b', iffalse).groups()[0])
        self.current_item_level = None
        self.monkey_to = None
        self.inspections = 0

    def inspect(self):
        second_value = self.current_item_level if self.op_num=="old" else int(self.op_num)
        if self.op=="+":
            self.current_item_level = (self.current_item_level + second_value) // 3 
        elif self.op == "*":
            self.current_item_level = (self.current_item_level * second_value) // 3
        else:
            print("arg")
            self.exit()

    def test(self):
        return self.current_item_level % self.divisible_by == 0
    
    def monkey_find(self):
        self.current_item_level = self.items.pop(0)
        self.inspect()
        self.monkey_to = self.iftrue if self.test() else self.iffalse

    def throw(self):
        self.monkey_find()
        self.inspections+= 1
        return self.monkey_to, self.current_item_level, 

def round():
    for n in range(len(monkeys)):
        m = monkeys[n]
        print('Monkey', n)
        while m.items:
            to_monkey, item = m.throw()
            print(' throw', to_monkey, item)
            monkeys[to_monkey].items.append(item)

if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=11)

    # input is an array, with each item being a string
    # input = puzzle.input_data.split('\n')
    monkey_lines = split_on_empty_lines(puzzle.input_data)
    # monkey_lines = split_on_empty_lines(test_data)

    monkeys = []    
    for lines in monkey_lines:
        arg = lines.split('\n')
        monkeys.append(Monkey(arg[1], arg[2], arg[3], arg[4], arg[5]))
    for n in range(20):
        round()
    inspections = [m.inspections for m in monkeys]
    inspections.sort(reverse=True)
    print("Problem 1:", inspections[0]*inspections[1])
  