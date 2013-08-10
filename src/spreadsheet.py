import gspread
from datetime import datetime

from config import GOOGLE_CONF


class SpreadSheet:
    INTERVALS = 2
    def __init__(self):
        multiplier = 0

    def tick(self, temp_in, temp_out):
        multiplier += 1
        if self.multiplier >= self.INTERVALS:
            self.multiplier = 0
            self.update_spreadsheet(temp_in, temp_out)

    def update_spreadsheet(self, temp_in, temp_out):
        gc = gspread.login(*GOOGLE_CONF)
        sh = gc.open("Solar Panel Temp").sheet1
        values = [datetime.now(), temp_in, temp_out]
        sh.append_row(values)

