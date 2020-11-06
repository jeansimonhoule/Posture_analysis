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

    def check_for_heading(self,mode=''):
        heading = False
        reset = False
        while (heading) == False:
            read_usb = self.port.readline().decode("utf-8").replace(" \r\n",'').split(',')
            if mode =='start':
                print('*',read_usb)
            else:
                print(read_usb)
                break  
            if read_usb[0]=='sensor':
                print('yo1')
                while reset == False: 
                    print('yo2')
                    read_usb = self.port.readline().decode("utf-8").replace(" \r\n",'').split(',')
                    if read_usb[0]=='sensor':
                        self.port.reset_input_buffer()
                        continue
                    if int(read_usb[2]) <= 500:
                        reset = True
                        print('break')
                    self.port.reset_input_buffer()
                heading = True
            


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
    sensor.check_for_heading(mode='start')
    print("Recording starts now...")
    while True:
        sensor.check_for_heading()
        sensor.getAcceleration()
        print(sensor.acceleration)
        sensor.write_to_csv("DATA.csv","REFERENCE.csv")

if __name__ == "__main__":
    main()
