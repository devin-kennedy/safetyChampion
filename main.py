import mouse

from Board import Board
from cvHandler import cvHandler
import time


def main():
    size = int(input("Board Size: "))

    for _ in range(100):
        mycv = cvHandler()
        unparsed = mycv.parse_board(size)
        myBoard = Board(raw=unparsed, size=size)

        print(myBoard)
        myBoard.backtrack_solve()
        print(myBoard)

        mycv.autoSolve(myBoard)
        break
        #mouse.move(1110, 360)
        #mouse.click()
        #time.sleep(0.1)


def test():
    mouse.move(1110, 360)


if __name__ == "__main__":
    main()
