import cv2 as cv
from imutils import contours
import pyautogui
import numpy as np
from boardDB import allColors
from Board import Board
import mouse
import time
from methods import check_rgb


class cvHandler:
    def __init__(self):
        mouse.move(100, 500)
        mouse.click()
        time.sleep(0.01)

        raw = pyautogui.screenshot()
        self.img = cv.cvtColor(np.array(raw), cv.COLOR_RGB2BGR)
        self.gray = cv.cvtColor(np.array(raw), cv.COLOR_RGB2GRAY)
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.boardImg = None
        self.cellIterBoard = None
        self.boardLoc = None

    def __thresh_board(self):
        grayBoard = cv.cvtColor(self.boardImg, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(grayBoard, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 57, 5)

        cnts = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv.contourArea(c)
            if area < 1000:
                cv.drawContours(thresh, [c], -1, (0, 0, 0), -1)

        vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 5))
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, vertical_kernel, iterations=9)

        horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, horizontal_kernel, iterations=4)

        invert = 255 - thresh
        cnts = cv.findContours(invert, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
        return grayBoard, thresh, cnts

    def showScreen(self):
        cv.imshow("Screen", self.img)
        cv.waitKey(0)

    def find_board(self):
        ret, binary = cv.threshold(self.gray, 100, 255, cv.THRESH_OTSU)
        inverted_binary = ~binary

        cnts, hierarchy = cv.findContours(inverted_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        boardLst = sorted(cnts, key=cv.contourArea)
        roi = x = y = None

        for pos in boardLst:
            thisImg = self.img.copy()
            x, y, w, h = cv.boundingRect(pos)
            cv.rectangle(thisImg, (x, y), (x + w, y + h), (0, 255, 0), 2)

            roi = thisImg[y:y + h, x:x + w]

            if roi.shape[0] == roi.shape[1] and roi.shape[0] > 200:
                break

        if roi is None:
            raise ValueError("Board not found")

        self.boardImg = roi
        self.boardLoc = (x, y)

        # cv.imshow("Board", roi)
        # cv.waitKey(0)

    def parse_board(self, size: int):
        if not self.boardImg:
            self.find_board()

        grayBoard, thresh, cnts = self.__thresh_board()

        board = []
        row = []
        for (i, c) in enumerate(cnts, 1):
            area = cv.contourArea(c)
            if area < 50000:
                row.append(c)
                if i % size == 0:
                    (cnts, _) = contours.sort_contours(row, method='left-to-right')
                    board.append(cnts)
                    row = []

        unparsed_board = ""
        color_values = {}
        unusedColors = list(allColors.keys())
        self.cellIterBoard = board
        for row in board:
            for c in row:
                mask = np.zeros(self.boardImg.shape, dtype=np.uint8)
                cv.drawContours(mask, [c], -1, (255, 255, 255), -1)
                result = cv.bitwise_and(self.boardImg, mask)
                result[mask == 0] = 255

                x, y, w, h = cv.boundingRect(c)
                cropped = result[y:y+h, x:x+w]

                # cv.imshow("cell", cropped)
                # cv.waitKey(0)

                b = np.mean(cropped[:, :, 0])
                g = np.mean(cropped[:, :, 1])
                r = np.mean(cropped[:, :, 2])
                knownColor = check_rgb((r, g, b), list(color_values.keys()), 5)

                if knownColor is None:
                    color_values[(r, g, b)] = unusedColors[0]
                    unusedColors.pop(0)
                    unparsed_board += (color_values[(r, g, b)] + " ")
                else:
                    unparsed_board += (color_values[knownColor] + " ")

            unparsed_board = unparsed_board[:-1]
            unparsed_board += "\n"

        return unparsed_board[:-1]

    def autoSolve(self, solved_board: Board):
        if not solved_board.isWon() or self.boardImg is None or self.cellIterBoard is None:
            return False

        for i, row in enumerate(self.cellIterBoard):
            for j, c in enumerate(row):
                if solved_board[(i, j)].getState() == "Q":
                    (x, y) = c[0][0]

                    x = x + self.boardLoc[0] + 5
                    y = y + self.boardLoc[1] + 5
                    mouse.move(x, y)
                    mouse.double_click()
