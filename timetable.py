from selenium import webdriver
import time

class Timetable:
    def __init__(self, busNumber):
        self.bus = busNumber
        self.driver = webdriver.Firefox()
        self.busStops = self.getBusStops(self.bus)

    def getBusStops(self, bus):
        timetable = {}
        url = f"https://www.nctx.co.uk/services/NCT/{bus}?direction=inbound&all=on"
        
        self.driver.get(url)
        self.cloudFlareCheck(url)


        # Check if bus is found
        if "Page Not Found" in self.driver.title:
            print(f"Bus {bus} not found!")
            self.driver.close()
            exit()

        busStops = self.driver.find_elements_by_class_name("line-timetable__link")
        
        for busStop in busStops:
            if(busStop.text != ""):
                print(busStop.text + " : " + busStop.get_attribute('href'))
                timetable[busStop.text] = {"link":busStop.get_attribute('href')}
        
        return timetable

    def cloudFlareCheck(self, url):
        while "Just a moment" in self.driver.title:
            self.driver.close()
            self.driver = webdriver.Firefox()
            self.driver.get(url)
            time.sleep(10)
        return

    def getBusStop(self, busStopName):
        for busStop in self.busStops.keys():
            if busStopName in busStop:
                return self.busStops[busStop]
        print(f"Couldn't find bus stop: {busStopName}")
        self.driver.close()
        exit()


    def getBusStopTimes(self, busStopName):
        busStop = self.getBusStop(busStopName)

        self.driver.get(busStop["link"])

        # put in thread
        try:
            update = self.driver.get_element_by_class_name("single-stop__body")
            if "The departure board below is out of date" in update.text:
                self.driver.get(busStop["link"])
        except:
            print("no need to update")
            pass

        



        return {}