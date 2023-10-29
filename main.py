from camera import *
from engine import *
from serialcom import *
from gui import *
import threading

ser = SerialCOM("COM7", 9600)
serial_thread = threading.Thread(target=ser.mainloop)
serial_thread.daemon = True
serial_thread.start()

ser.writeToBuffer("calibrate")
ser.writeToBuffer("J190J2125J3-90J40J5-100J60")


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the coordinates when the left mouse button is clicked
        print(f"Coordinates: ({x}, {y})")


camera = Camera()
gameGUI = GUI(boardimg, "Chess", 800, 800)
cameraGUI = GUI(None, "Camera", 640, 640)
cv2.namedWindow(cameraGUI.title)
cv2.setMouseCallback(cameraGUI.title, click_event)

engine = ChessEngine()

game = chess.Board()
game.clear()

robotSide = chess.WHITE
camera.boardCorners = np.float32(
    [(146, 162 * 0.75), (480, 169 * 0.75), (53, 622 * 0.75), (521, 648 * 0.75)]
)
state = "setup"

corner1 = (-137.5, 527.5)
corner2 = (160.0, 500.0)
corner3 = (-165.0, 230.0)
corner4 = (132.5, 202.5)


def moveToSquare(square, t=3.0, down=False):
    index_h = float(ord(square[0:1]) - ord("a"))
    index_v = float(square[1:]) - 1

    deltav = ((corner1[0] - corner3[0]) * 0.125, (corner1[1] - corner3[1]) * 0.125)
    deltah = ((corner4[0] - corner3[0]) * 0.125, (corner4[1] - corner3[1]) * 0.125)

    x = corner3[0] + deltah[0] * index_h + deltav[0] * index_v
    y = corner3[1] + deltah[1] * index_h + deltav[1] * index_v

    z = 150 - 80 * down
    option = "LOOKDOWN"
    ser.writeToBuffer(f"X{x}Y{y}Z{z}T{t}O{option}")


while True:
    camera.updateFrame()
    pieces = camera.getPieceSquares()

    if state == "aquire board corners":
        camera.updateBoardCorners()
        if camera.boardCorners is not None:
            print(camera.boardCorners)
            state = "setup"

    if state == "setup":
        confirmed = False
        fen = str(camera.getFenPosition())

        if str(fen) == str(chess.STARTING_BOARD_FEN):
            confirmed = camera.confirmBoard(fen)
            robotSide = True
            print("Board confirmed. Robot plays as white.")

        if str(fen) == str(chess.STARTING_BOARD_FEN)[::-1]:
            confirmed = camera.confirmBoard(fen)
            robotSide = False
            print("Board confirmed. Robot plays as black.")

        if confirmed:
            state = "play"
            gameGUI.updateBoard(pieces)
            gameGUI.display()

    if state == "play":
        if game.turn == robotSide:
            # update engine
            fen = camera.getFenPosition()

            if camera.confirmBoard(fen):
                best_move = engine.getBestMove(1000)
                print(best_move)

                # send serial start command
                # await serial end response
                # confirm new board
                engine.playMove(best_move)
                game.turn = not robotSide

                square1High = moveToSquare(best_move[0:2], 2.0, False)
                square1Low = moveToSquare(best_move[0:2], 1.0, True)
                square1HighFast = moveToSquare(best_move[0:2], 1.0, False)

                square2High = moveToSquare(best_move[2:], 2.0, False)
                square2Low = moveToSquare(best_move[2:], 1.0, True)
                square2HighFast = moveToSquare(best_move[2:], 1.0, False)
                ser.writeToBuffer("J190J2125J3-90J40J5-100J60")

        else:
            fen = camera.getFenPosition()
            if camera.confirmBoard(fen):
                opponentsMove = engine.computeLastMove(fen)

                if opponentsMove is not None:
                    engine.playMove(opponentsMove)
                    game.turn = robotSide

    gameGUI.updateBoard(pieces)
    gameGUI.display()
    cameraGUI.displayImage = camera.YOLOframe
    cameraGUI.display()
    cv2.waitKey(1) & 0xFF

# FEN = camera.getFenPosition()
# while FEN is not chess.STARTING_FEN:
#    FEN = camera.getFenPosition()

# engine.setFenPosition(camera.getFenPosition())
# print(engine.stockfish.get_board_visual())

camera.release()
