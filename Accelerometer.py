import serial
import time
import csv
import datetime
import os
from pathlib import Path



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


    def create_folder(self):
        #get date of capture
        date = datetime.datetime.now().strftime("%Y_%m_%d")

        #create the folder named after the day of capture
        path = Path(os.path.abspath(__file__))
        path = path.parent.joinpath("SAVED_DATA").joinpath(str(date))
        if path.exists() == False:
            os.mkdir(path)
        return path
        
        
    def write_to_csv(self, filename_data,filename_reference):
        """Writes data to csv file"""
        if int(self.acceleration[0]) == 1:
            with open (str(self.create_folder().joinpath('REFERENCE.csv')),'a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.acceleration[1:])
        else:
            with open (str(self.create_folder().joinpath('DATA.csv')),'a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.acceleration[1:])


        
def main():
    sensor = Accelerometer()
    sensor.setPort('COM4',9600)
    while True:
        sensor.getAcceleration()
        print(sensor.acceleration)
        sensor.write_to_csv("DATA.csv","REFERENCE.csv")


if __name__ == "__main__":
    main()
