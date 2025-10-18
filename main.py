import mouse

from Board import Board
from cvHandler import cvHandler
import time


def main():
    start = time.thread_time()
    myBoard = None

    found = False
    thresh = 5
    for i in range(10):
        myBoard = None
        try:
            mycv = cvHandler()
            unparsed, size = mycv.parse_board(cell_detection_tolerance=thresh)
            myBoard = Board(raw=unparsed, size=size)

            print(myBoard)
            myBoard.backtrack_solve()
            print(myBoard)
            found = True
        except ValueError as e:
            print(e)
            thresh += 1
        if found:
            print(f"Found board in {i+1} tries with thresh {thresh}")
            break

    if not found:
        raise ValueError("Failed to detect valid board")

    mycv.autoSolve(myBoard)
    timeToSolve = time.thread_time() - start
    print("Time to solve: " + str(timeToSolve))


def test():
    #mouse.move(1110, 280)
    mouse.move(750, 650)


def loop_main():
    for _ in range(3):
        main()
        mouse.move(750, 650)
        time.sleep(1)
        mouse.click()
        time.sleep(3)


if __name__ == "__main__":
    main()
