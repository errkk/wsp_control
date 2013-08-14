from pigredients.displays import textStarSerialLCD as textStarSerialLCD


class Display(textStarSerialLCD.Display):
    " Simple wrapper for the Text Star display interface "

    baud_rate = 9600

    def write_all(line1, line1=None):
        self.clear()
        self.position_cursor(1, 1)
        self.ser.write(line1)
        self.position_cursor(2, 1)
        self.ser.write(line2)




