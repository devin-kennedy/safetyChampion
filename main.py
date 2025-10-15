import mouse

from Board import Board
from cvHandler import cvHandler
import time


def main():

    for _ in range(100):
        start = time.thread_time()
        mycv = cvHandler()
        unparsed, size = mycv.parse_board()
        myBoard = Board(raw=unparsed, size=size)

        print(myBoard)
        myBoard.backtrack_solve()
        print(myBoard)

        mycv.autoSolve(myBoard)
        timeToSolve = time.thread_time() - start
        print("Time to solve: " + str(timeToSolve))

        break
        #mouse.move(1110, 360)
        #mouse.click()
        #time.sleep(0.1)


def test():
    mouse.move(1110, 360)


if __name__ == "__main__":
    main()
