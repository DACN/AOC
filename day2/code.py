from dataclasses import dataclass
import sys
import re
  
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
    p = Position()
    with open(sys.argv[1]) as fin:
        for line in fin:
            m = re.search(r'(?P<instruction>\w+)\s+(?P<value>\d+)', line)
            print(line,m)

#    down X increases your aim by X units.
#    up X decreases your aim by X units.
#    forward X does two things:
#        It increases your horizontal position by X units.
#        It increases your depth by your aim multiplied by X.


            X = int(m.group('value'))
            match m.group('instruction'):
                case 'forward':
                    p = p + Position(X, p.aim*X,0)
                case 'down':
                    p = p + Position(0, 0, X)
                case 'up':
                    p = p + Position(0, 0, -X)
                case _:
                    print('error')
                    sys.exit()
            print(p)
            print()
        print('Result=',p.forward*p.down)

