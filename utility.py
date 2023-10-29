import chess


class Color:
    red = (0, 0, 255)
    orange = (0, 128, 255)
    yellow = (0, 255, 255)
    lightgreen = (0, 255, 128)
    green = (0, 255, 0)
    offgreen = (128, 255, 0)
    lightblue = (255, 255, 0)
    offblue = (255, 128, 0)
    blue = (255, 0, 0)
    purple = (255, 0, 128)
    pink = (255, 0, 255)
    pinkred = (255, 0, 128)


classColors = [
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 0, 0),
]

spriteWidth = 132
spriteHeight = 132


def classIDToPiece(id):
    if id == 0:
        return chess.Piece(chess.BISHOP, chess.BLACK)
    elif id == 1:
        return chess.Piece(chess.KING, chess.BLACK)
    elif id == 2:
        return chess.Piece(chess.KNIGHT, chess.BLACK)
    elif id == 3:
        return chess.Piece(chess.PAWN, chess.BLACK)
    elif id == 4:
        return chess.Piece(chess.QUEEN, chess.BLACK)
    elif id == 5:
        return chess.Piece(chess.ROOK, chess.BLACK)
    elif id == 6:
        return chess.Piece(chess.BISHOP, chess.WHITE)
    elif id == 7:
        return chess.Piece(chess.KING, chess.WHITE)
    elif id == 8:
        return chess.Piece(chess.KNIGHT, chess.WHITE)
    elif id == 9:
        return chess.Piece(chess.PAWN, chess.WHITE)
    elif id == 10:
        return chess.Piece(chess.QUEEN, chess.WHITE)
    elif id == 11:
        return chess.Piece(chess.ROOK, chess.WHITE)
