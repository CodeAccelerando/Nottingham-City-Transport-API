from bus import Bus
from timetable import Timetable
import serial
import time

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
time.sleep(2)
b1 = Timetable(69)


while(True):
    busTimes = b1.getBusStopTimes("Central Avenue")
    print(busTimes)

    for i in range(4):
        message = busTimes[i]['bus'] + (20-(len(busTimes[i]['bus'])+len(busTimes[i]['time'])))*" " + busTimes[i]['time'] + '\n'
        print(message)
        time.sleep(1)
        arduino.write(bytes(message,'utf-8'))

    

    time.sleep(15)

