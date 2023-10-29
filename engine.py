import chess
from stockfish import Stockfish


class ChessEngine:
    def __init__(
        self,
        stockfish_path="stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe",
    ):
        self.plays = []
        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.update_engine_parameters({"Hash": 2048})
        self.board = chess.Board(chess.STARTING_FEN)

    def playMove(self, move):
        self.plays.append(str(move))
        self.stockfish.set_position(self.plays)
        self.board.set_fen(self.stockfish.get_fen_position())
        # print(self.stockfish.get_board_visual())

    def computeLastMove(self, new_fen):
        for move in self.board.legal_moves:
            boardCopy = self.board.copy()
            boardCopy.push(move)
            if boardCopy.board_fen() == new_fen:
                return str(move)
        return None

    def getBestMove(self, ms=1000):
        return str(self.stockfish.get_best_move_time(ms))

    def setFenPosition(self, fen):
        self.stockfish.set_fen_position(fen)
