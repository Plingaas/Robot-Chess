import cv2
from chessCV import *


class GUI:
    def __init__(self, src, title, width=640, height=640):
        self.boardImage = src
        self.width = width
        self.height = height
        self.displayImage = None
        self.title = title

    def updateBoard(self, pieces):
        self.displayImage = self.boardImage.copy()
        if pieces is not None:
            for piece in pieces:
                y_pos = (7 - piece[1][1]) * h
                x_pos = piece[1][0] * w
                sprite = pieceList[piece[0]]
                self.displayImage[
                    y_pos : y_pos + sprite.shape[0], x_pos : x_pos + sprite.shape[1]
                ] = sprite

    def display(self):
        self.displayImage = cv2.resize(self.displayImage, (self.width, self.height))
        cv2.imshow(self.title, self.displayImage)
