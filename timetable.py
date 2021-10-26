from selenium import webdriver

class Timetable:
    def __init__(self, busNumber):
        self.bus = busNumber
        self.driver = webdriver.Firefox()
        self.getTimetable()
        return

    def getTimetable(self):
        self.driver.get(f"https://www.nctx.co.uk/services/NCT/{self.bus}?direction=inbound&all=on")
        return