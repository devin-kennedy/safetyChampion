import math

from boardDB import *
from methods import *
import random
from Cell import Cell


class Board:
    def __init__(self, selection=None, raw=None, preParsed=None, size=None):
        try:
            if selection:
                int(selection)
                allBoards[selection]
        except ValueError:
            raise ValueError("Enter an integer for the board selection within the range of the board database")
        if preParsed:
            self.board = preParsed
            self.size = len(self.board)
        else:
            if raw is not None:
                self.unparsed = raw
            elif selection is None:
                self.unparsed = allBoards[random.randint(0, len(allBoards) - 1)]
            else:
                self.unparsed = allBoards[selection]

            if not size:
                self.size = 8
            else:
                self.size = size
            self.board = self.__parse()

    def __str__(self):
        out = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                out += str(self.board[i][j])
            out += "\n"
        return out

    def __getitem__(self, item: tuple[int, int]):
        return self.board[item[0]][item[1]]

    def __parse(self):
        board = []
        row = []
        allCodes = self.unparsed.replace("\n", " ").split(" ")
        for i in range(len(allCodes)):
            rowPos, colPos = xy_by_index(i, self.size)
            cell = Cell(rowPos, colPos, allCodes[i], "E")
            if i % self.size == 0 and i >= self.size:
                board.append(row)
                row = []
            row.append(cell)
        board.append(row)
        return board

    def __allColors(self):
        colors = []
        for i in range(self.size):
            for j in range(self.size):
                if self[(i, j)].color not in colors:
                    colors.append(self[(i, j)].color)
        return colors

    def __numQueens(self):
        queens = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].getState() == "Q":
                    queens += 1
        return queens

    def __checkLegal(self, pos):
        # Check queens in surrounding cells
        for p in surrounding_cells(self.size, pos):
            if self[p].getState() == "Q":
                return False
        # Check queens in the row
        for p in row_cells(self.size, pos):
            if self[p].getState() == "Q":
                return False
        # Check queens in the column
        for p in col_cells(self.size, pos):
            if self[p].getState() == "Q":
                return False
        # Check queens in the same color
        numColor = 0
        color = self[pos].color
        for i in range(self.size):
            for j in range(self.size):
                if self[(i, j)].color == color and self[(i, j)].getState() == "Q":
                    numColor += 1
        if numColor >= 1:
            return False

        return True

    def __checkQueenPlacements(self):
        # Check by color
        openByColor = {k: [] for k in self.__allColors()}
        for i in range(self.size):
            for j in range(self.size):
                c = self[(i, j)]
                if c.getState() == "E":
                    openByColor[c.color].append(c.getPos())
        cells = [v[0] for v in openByColor.values() if len(v) == 1]

        # Check by row and col
        for i in range(self.size):
            row = self.board[i].copy()
            col = [self[(k, i)] for k in range(self.size)]
            if [j.getState() for j in row].count("E") == 1:
                for j in range(self.size):
                    if self[(i, j)].getState() == "E":
                        cells.append(self[(i, j)].getPos())
            if [j.getState() for j in col].count("E") == 1:
                for j in range(self.size):
                    if self[(j, i)].getState() == "E":
                        cells.append(self[(j, i)].getPos())
        # Dude this function fucking sucks and needs to be rewritten but I will never do that
        return cells

    def setCellState(self, pos: tuple[int, int], state: str):
        if state not in validStates:
            raise ValueError("Invalid state")
        if pos[0] >= self.size or pos[1] >= self.size:
            raise ValueError("Pos out of board range")
        self.board[pos[0]][pos[1]].setState(state)

    def setQueen(self, pos):
        if pos[0] >= self.size or pos[1] >= self.size:
            raise ValueError("Pos out of board range")
        if not self.__checkLegal(pos):
            raise ValueError("Illegal move")

        self.setCellState(pos, "Q")

        for p in surrounding_cells(self.size, pos):
            self.setCellState(p, "X")

        for p in row_cells(self.size, pos):
            self.setCellState(p, "X")

        for p in col_cells(self.size, pos):
            self.setCellState(p, "X")

    def isWon(self):
        return self.__numQueens() == self.size

    def copyBoard(self):
        return Board(preParsed=self.board)

    def n_queens(self, row, out):
        if row == self.size:
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j].getState() == "Q":
                        out.append((i, j))
            return

        for i in range(self.size):
            if self.__checkLegal((row, i)):
                self.setCellState((row, i), "Q")
                self.n_queens(row + 1, out)
                self.setCellState((row, i), "E")

    def naive_solve(self, maxTries=None):
        maxTries = math.inf if maxTries is None else maxTries
        n = 0

        while not self.isWon() and n <= maxTries:
            # This logic alone can solve an easy board
            for p in self.__checkQueenPlacements():
                self.setQueen(p)

            n += 1

    def backtrack_solve(self):
        placements = []
        self.n_queens(0, placements)
        for p in placements:
            self.setQueen(p)

        if self.isWon():
            return True
        return False
