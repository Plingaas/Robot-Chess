import cv2
import chess
from chessCV import *
from utility import *
from yolo import *


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(
            0, cv2.CAP_DSHOW
        )  # Use the first camera (index 0)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cv = CVModel(0.6)
        self.frame = None
        self.boardCorners = None
        self.confirmationRequirement = 10
        self.YOLOframe = None

    def updateFrame(self):
        self.frame = self.camera.read()[1]
        self.YOLOframe = self.frame.copy()

    def findPieces(self):
        if self.frame is None:
            return

        pieces = []
        results = self.cv.model.predict(self.frame, verbose=False)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > self.cv.threshold:
                pieces.append(
                    [int(class_id), ((x2 + x1) * 0.5, (0.667 * y2 + 0.333 * y1))]
                )
                cv2.rectangle(
                    self.YOLOframe,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    classColors[int(class_id)],
                    1,
                )
                cv2.putText(
                    self.YOLOframe,
                    f"{results.names[int(class_id)].upper()[0:1]}{results.names[int(class_id)].upper()[6:]}",
                    (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    classColors[int(class_id)],
                    1,
                    cv2.LINE_AA,
                )

        return pieces

    # Projection Transformation to get 2D board.
    def getBoardFromImage(self):
        self.boardCorners = getCornersFromImage(self.frame)

        if self.boardCorners is None:
            return None
        return extractBoard(self.frame, self.boardCorners)

    def getBoard(self):
        if self.boardCorners is None:
            return None

        pieces = self.findPieces()
        matrix = getPerspectiveTransformationMatrix(self.boardCorners)

        board = chess.Board()
        board.clear()

        for piece in pieces:
            p = transformPoint(piece[1], matrix)
            pos = getSquareFromPoint(p)

            class_id = int(piece[0])
            x_index = pos[0]
            y_index = pos[1]

            if x_index < 0 or x_index > 7 or y_index < 0 or y_index > 7:
                continue

            board_index = x_index + y_index * 8
            board.set_piece_at(board_index, classIDToPiece(class_id))

        return board

    def getPieceSquares(self):
        if self.boardCorners is None:
            return None

        pieces = self.findPieces()
        matrix = getPerspectiveTransformationMatrix(self.boardCorners)

        validPieces = []
        for piece in pieces:
            p = transformPoint(piece[1], matrix)
            pos = getSquareFromPoint(p)
            x_index = pos[0]
            y_index = pos[1]

            if not (x_index < 0 or x_index > 7 or y_index < 0 or y_index > 7):
                validPieces.append([piece[0], (x_index, y_index)])

        return validPieces

    def confirmBoard(self, fen):
        for i in range(self.confirmationRequirement):
            matching = str(self.getFenPosition()) == str(fen)
            if not matching:
                print(f"Failed to confirm board after {i+1} frames.")
                return False
        return True

    def getFenPosition(self):
        board = self.getBoard()
        if board is None:
            return None

        return board.board_fen()

    def updateBoardCorners(self):
        self.boardCorners = getCornersFromImage(self.frame)

    def release(self):
        self.camera.release()
