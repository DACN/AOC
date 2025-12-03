import io
from aocd import get_data
import re



def read_data(test):
    if test:
        text_file = io.StringIO(test_data)
    else:
        data = get_data(day=2,year=2025)
        text_file = io.StringIO(data)
    return text_file


def parse_string(s):
    match = re.match(r"(\d*)-(\d*)$", s)
    if match:
        low, high = match.groups()
        return int(low), int(high)
    else:
        print(f"{match=}")
        raise ValueError("String format not valid")


def get_factors(N):
   factors = []
   for i in range(1,N):
       if N%i==0:
           factors += [i]
   return factors


def invalid(id):
    id_string = str(id)
    L = len(id_string)
    if L%2==1:
        return False
    return id_string[0:L//2]==id_string[L//2:]


def invalid1(id_string, L):
    return len(set(id_string))==1

def invalid2(id_string, L):
    return id_string[0:L//2]==id_string[L//2:]

def invalid3(id_string, L):
    return id_string[0:L//3]==id_string[L//3:2*L//3]==id_string[2*L//3:]

def invalid4(id_string, L):
    return id_string[0:L//4]==id_string[L//4:2*L//4]==id_string[2*L//4:3*L//4]==id_string[3*L//4:]

def invalid5(id_string, L):
    return id_string[0:L//5]==id_string[L//5:2*L//5]==id_string[2*L//5:3*L//5]==id_string[3*L//5:4*L//5]==id_string[4*L//5:]

def invalid6(id_string, L):
    return id_string[0:L//6]==id_string[L//6:2*L//6]==id_string[2*L//6:3*L//6]==id_string[3*L//6:4*L//4]==id_string[4*L//6:5*L//6]==id_string[5*L//6:]


def invalid_part2(id):
    id_string = str(id)
    L = len(id_string)
    return (invalid1(id_string, L) or invalid2(id_string, L) or invalid3(id_string, L)
           or invalid4(id_string, L) or invalid5(id_string, L) )


test_data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

if __name__=="__main__":

    max_high = 0
    text_file = read_data(test=False)
    line = text_file.read()
    ranges = line.split(',')
    sum_part1 = 0
    for rng in ranges:
        rng = rng.strip()
        low, high = parse_string(rng)
        max_high = max(max_high, high)
        for n in range(low, high+1):
            if invalid(n):
                sum_part1 += n
    print('part 1 = ',sum_part1)
    print('max_high = ',max_high)

    sum_part2 = 0
    for rng in ranges:
        rng = rng.strip()
        low, high = parse_string(rng)
        max_high = max(max_high, high)
        for n in range(low, high+1):
            if n <=9:
                continue
            if invalid_part2(n):
                print('Invalid part 2 -- ',n)
                sum_part2 += n
    print('part 2 = ',sum_part2)

    