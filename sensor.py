import serial
import time
import csv


class Accelerometer:
    "Class defining an acceleration sensor"

    def __init__(self):
        pass

    def setPort(self,portname, baudrate):
        """Sets the usb port on which the radio receptor is connected"""
        self.port= serial.Serial(str(portname),baudrate)

    def getAcceleration(self):
        """Reads and decode to string the information from the serial port"""
        self.acceleration = self.port.readline().decode("utf-8").replace(" \r\n",'').split(',')
        return self.acceleration
    
    def write_to_csv(self, filename):
        """Writes data to csv file"""
        with open ('test_csv.csv','a') as file:
            writer = csv.writer(file)
            writer.writerow(self.acceleration)

        
def main():
    sensor = Accelerometer()
    sensor.setPort('COM4',9600)
    while True:
        sensor.getAcceleration()
        sensor.write_to_csv("test_csv.csv")

if __name__ == "__main__":
    main()
