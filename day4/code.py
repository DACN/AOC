from dataclasses import dataclass
import dataclasses
import sys
import re

@dataclass
class Board:
    board: list = dataclasses.field(default_factory=list)
    marked: list = dataclasses.field(default_factory=list)

    def completed(self):
        success_row = [0,1,2,3,4,]
        success_col = [0,5,10,15,20]
        success_rows = [success_row, [x+5 for x in success_row], [x+10 for x in success_row],
                        [x+15 for x in success_row], [x+20 for x in success_row]]
        success_cols = [success_col, [x+1 for x in success_col], [x+2 for x in success_col],
                        [x+3 for x in success_col], [x+4 for x in success_col]]
        # success_diag = [[0,6,12,18,24], [4,8,12,16,20]]
        success = success_rows + success_cols  #  + success_diag
        return any(set(s).issubset(set(self.marked)) for s in success)


    def sum_unmarked(self):
        sum = 0
        for cell in range(len(self.board)):
            if not cell in self.marked:
                sum += self.board[cell]
        return sum

    def clear(self):
        self.marked = []


def iter_boards(fin):
    ''' returns boardss'''
    b = Board()
    for row in fin:
        if row.strip() != "":
            for n in row.strip().split():
                b.board.append(int(n))
        else:
            if b.board != []:
                yield b
                b = Board()
    if b != Board():
        yield b


if __name__=="__main__":
    try:
        with open(sys.argv[1]):
            pass
    except:
        print('Give file name as argument')
        sys.exit()

    with open(sys.argv[1]) as fin:
        numbers = next(fin).split(',')
        numbers = [int(n) for n in numbers]
        boards = []
        for board in iter_boards(fin):
            boards.append(board)

# which boards are completed
completed = []
# boards which are completed for a specific number called
b_comp = {}
for n in numbers:
    b_comp[n] = []
    for i,b in enumerate(boards):
        if n in b.board:
            b.marked.append(b.board.index(n))
        if b.completed():
            if not i in completed:
                completed.append(i)
                last_n = n
                b_comp[n].append(i)

#
# and we pull the lowest numbered board of those completed for a given n
last_n
last_board = b_comp[last_n][0]
#
# clear the boards
for b in boards:
    b.clear()
#
# and pull numbers till we get to the last board
for n in numbers:
    for b in boards:
        if n in b.board:
            b.marked.append(b.board.index(n))
    if n==last_n:
        break
print(f'{last_n=}')
print(f'{last_board}')
print(f'{boards[last_board]}')
print(f'{boards[last_board].sum_unmarked()*last_n}')
