import re
from aocd.models import Puzzle
from collections import namedtuple
import itertools

test_data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
test_data = test_data.strip().splitlines()

File = namedtuple("File", "name, size")

class Directory():
    def __init__(self, value, parent=None):
        self.name = value # data
        self.subdirs = [] # references to subdirectories
        self.subdir_names = []  # names of subdirs (not strictly necessary to keep as well)
        self.files = []  # a list of files
        self.parent = parent  # parent directory

    def add_sub_dir(self, subdir_name):
        # creates a subdirectory if it doesn't already exist
        if subdir_name not in self.subdir_names:
            self.subdirs.append(Directory(subdir_name, self))
            self.subdir_names.append(subdir_name)

    def return_sub_dir(self, name):
        for sd in self.subdirs:
            if sd.name == name:
                return sd

    def add_file(self, file):
        self.files.append(file)

    def traverse(self):
        # moves through each node referenced from self downwards
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            print(current_node.name)
            nodes_to_visit += current_node.subdirs

    def size_this_dir(self):
        return sum([x.size for x in self.files])

    def traverse_size(self):
        # finds total size including subdirectoris
        nodes_to_visit = [self]
        size = 0
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            size += current_node.size_this_dir()
            nodes_to_visit += current_node.subdirs
        return size

    def traverse_all_sizes(self):
        sizes = []
        # moves through each node referenced from self downwards
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            sizes.append((current_node.name, current_node.traverse_size()))
            nodes_to_visit += current_node.subdirs
        return sizes

def peek_ahead(input):
    items, peeker = itertools.tee(input, 2)
    next(peeker) # skip ahead on peeker
    for line, next_line in zip(items, peeker):
        yield line, next_line
    yield next_line, "$END"  # used to use None - but this makes parsing easier if last command is $ls


def parser(input):
    ph = peek_ahead(input)
    for line, next_line in ph:
        if line.startswith("$ cd /"):
            current = root
            # print(line)  
        elif line.startswith("$ cd .."):
            current = current.parent
            # print(line)  
        elif line.startswith("$ cd"):
            name = line.split(' ')[2].strip()
            current.add_sub_dir(name)
            current =  current.return_sub_dir(name)
            # print(line)  
        elif line.startswith("$ ls"):
            print(line)
            while not next_line.startswith("$"):
                line, next_line = next(ph)
                m, name = line.split(' ')
                if m=="dir":
                    current.add_sub_dir(name)
                else:
                    size = int(m)
                    current.add_file(File(name,size))
        else:
            print('NOT PARSED')
            halt()


if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=7)

    # create our root directory
    root = Directory("/")
    # set current directory to root
    current = root

    input_data = puzzle.input_data.splitlines()
    parser(input_data)
    sizes = root.traverse_all_sizes()
    print("Problem 1;", sum([size if size<=100_000 else 0 for (d,size) in sizes]))

    total_disk = 70_000_000
    needed = 30_000_000
    used = sizes[0][1]
    free = total_disk - used
    to_be_freed = needed - free
    candidates = [(d, size) for (d, size) in sizes if size >= to_be_freed]
    print("Problem 2", min([s for (d,s) in candidates]))
 
    