import re
from aocd.models import Puzzle

test_data = """30373
25512
65332
33549
35390"""

def matrixT(A):
    return  [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_LR(A):
    return [line[::-1] for line in A]

def visible(line):
    # return a list of 0,1 for visibility from the left
    return [1] + [1 if line[n] > max(line[0:n]) else 0 for n in range(1,len(line))]

def check_left(A):
    # check an array for visibility from the left, return an array of 0,1s
    C = []
    for line in A:
        C.append(visible(line))
    return C

def check_right(A):
    return matrix_LR(check_left(matrix_LR(A)))

def check_top(A):
    return matrixT(check_left(matrixT(A)))

def check_bottom(A):
    return matrixT(check_right(matrixT(A)))

def array_max(A1, A2, A3, A4):
    Amax = []
    for l1,l2,l3,l4 in zip(A1,A2,A3,A4):
        line = [max(a1,a2,a3,a4) for a1,a2,a3,a4 in zip(l1,l2,l3,l4)]
        Amax.append(line)
    return Amax

def array_sum(A):
    return sum([sum(line) for line in A])

def problem1(trees):
    left = check_left(trees)
    right = check_right(trees)
    top = check_top(trees)
    bottom = check_bottom(trees)
    return array_sum(array_max(left, right, top, bottom))

def to_right(line):
    L = len(line)-1   # items we can possible see
    ans = L*[0]
    for i in range(L):
        if line[i+1] < line[0]:
            ans[i] = 1
        else:
            ans[i] = 1
            break
    # print(line, sum(ans))
    return sum(ans)

def score_left_right(line,j):
    return to_right(line[j:])*to_right(line[:j+1][::-1])


def score_horizontal(A):
    score = []
    for line in A:
        score.append([score_left_right(line,j) for j in range(len(line))])
    return score

def score_vertical(A):
    return matrixT(score_horizontal(matrixT(A)))

def array_product(A1, A2):
    Aprod = []
    for l1,l2 in zip(A1,A2):
        line = [a1*a2 for a1,a2 in zip(l1,l2)]
        Aprod.append(line)
    return Aprod

def array_max2(A):
    return max([max(line) for line in A])


def problem2(trees):
    horizontal = score_horizontal(trees)
    vertical = score_vertical(trees)
    return array_max2(array_product(horizontal, vertical))
 

if __name__=="__main__":
    puzzle = Puzzle(year=2022, day=8)

    # input is an array, with each item being a string
    input = puzzle.input_data.split('\n')
    # input = test_data.split('\n')
    trees = [ [int(x) for x in list(line)] for line in input]

print("Problem 1:", problem1(trees))
print("Problem 2:", problem2(trees))

