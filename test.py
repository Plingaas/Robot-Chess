from serialcom import *
import threading

ser = SerialCOM("COM7", 9600)
serial_thread = threading.Thread(target=ser.mainloop)
serial_thread.daemon = True
serial_thread.start()

ser.writeToBuffer("calibrate")
ser.writeToBuffer("calibrate")
ser.writeToBuffer("J190J2125J3-90J40J5-100J60")

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

    z = 150 - 50 * down
    option = "LOOKDOWN"
    ser.writeToBuffer(f"X{x}Y{y}Z{z}T{t}O{option}")


best_move = "e2e4"
square1High = moveToSquare(best_move[0:2], 2.0, False)
square1Low = moveToSquare(best_move[0:2], 1.0, True)
square1HighFast = moveToSquare(best_move[0:2], 1.0, False)

square2High = moveToSquare(best_move[2:], 2.0, False)
square2Low = moveToSquare(best_move[2:], 1.0, True)
square2HighFast = moveToSquare(best_move[2:], 1.0, False)
ser.writeToBuffer("J190J2125J3-90J40J5-100J60")

while True:
    print("running")
