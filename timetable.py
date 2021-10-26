from selenium import webdriver
import time

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

class Timetable:
    def __init__(self, busNumber):
        self.bus = busNumber

        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
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
            self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
            self.driver.get(url)
            time.sleep(15)
        return

    def getBusStop(self, busStopName):
        for busStop in self.busStops.keys():
            if busStopName in busStop:
                return self.busStops[busStop]
        print(f"Couldn't find bus stop: {busStopName}")
        self.driver.close()
        exit()


    def getBusStopTimes(self, busStopName):
        busTimes = []
        busStop = self.getBusStop(busStopName)

        print(busStop["link"])

        self.driver.get(busStop["link"])

        # put in thread
        try:
            update = self.driver.get_element_by_class_name("single-stop__body")
            if "The departure board below is out of date" in update.text:
                self.driver.get(busStop["link"])
        except:
            print("no need to update")
            pass

        buses = self.driver.find_elements_by_class_name("single-visit__name")
        destinations = self.driver.find_elements_by_class_name("single-visit__description")
        times = self.driver.find_elements_by_class_name("single-visit__time--expected")

        print(len(buses))
        print(len(destinations))
        print(len(times))

        for i in range(0,len(times)):
            print(f"{buses[i].text} : {times[i].text}")
            busTimes.append({"bus" : buses[i].text, "destination" : destinations[i].text, "time" : times[i].text})

        return busTimes