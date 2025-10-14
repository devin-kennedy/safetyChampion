import boardDB


class Cell:
    def __init__(self, rowPos: int, colPos: int, color: str, state: str):
        self.rowPos = rowPos
        self.colPos = colPos
        self.color = color
        self.state = state

    def __str__(self):
        if self.state == "E":
            return boardDB.colorIcons[self.color]
        if self.state == "Q":
            return "👑"
        return " X"

    def __repr__(self):
        return self.color

    def getPos(self):
        return self.rowPos, self.colPos

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
