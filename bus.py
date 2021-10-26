from timetable import Timetable

class Bus:
    def __init__(self, busNumber):
        self.bus = busNumber
        self.timetable = Timetable(self.bus)
        return

    def isBusFound(self):
        return