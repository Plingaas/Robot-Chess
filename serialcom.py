import serial


class SerialCOM:
    def __init__(self, comPort, baud):
        self.ser = serial.Serial(comPort, baud)
        self.active = False
        self.read_data = None
        self.write_data = []

    def send_position_command(self, x, y, z, t, option):
        custom_command = f"X{x}Y{y}Z{z}T{t}O{option}"
        self.writeToBuffer(custom_command)

    def send_grip_command(self):
        self.writeToBuffer("grip")

    def send_jog_command(self, motor, steps):
        jog_command = f"{motor}{steps}"
        self.writeToBuffer(jog_command)

    def send_calibration_command(self):
        self.writeToBuffer("calibrate")

    def write(self):
        self.ser.write(self.write_data[0].encode("utf-8"))
        self.write_data = self.write_data[1:]
        self.active = True
        print("wrote data")

    def read(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode().strip()
            print(data)
            self.read_data = data
            self.active = False

    def writeToBuffer(self, data):
        self.write_data.append(data)

    def mainloop(self):
        while True:
            self.read()
            if self.write_data and not self.active:
                self.write()
