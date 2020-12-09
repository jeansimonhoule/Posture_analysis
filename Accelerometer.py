import serial
import serial.tools.list_ports
import time
import csv
import datetime
import os
from pathlib import Path
from user import User



class Accelerometer:
    "Class defining an acceleration sensor"

    def __init__(self):
        self.reset = False
        self.stop = False
        self.no_connection = True

    def setPort(self,portname, baudrate):
        """Sets the usb port on which the radio receptor is connected"""
        # by default COM port is COM4, if not found, we take the first communication port available
        while self.no_connection == True:
            ports = list(serial.tools.list_ports.comports())
            if len(ports) > 0:
                self.no_connection = False 
        try:
            print("")
            self.port= serial.Serial(str(portname),baudrate)
        except serial.SerialException:
            try:
                print("")
                time.sleep(0.5)
                ports = list(serial.tools.list_ports.comports())
                self.port = serial.Serial(str(ports[0][0]))
            except IndexError:
                print("Micro:bit not found")


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

            if read_usb[0]=='sensor':
                print('yo1')
                self.create_new_session() ###crée une nouvelle session lorsque le temps est remis à zéro
                time.sleep(1)
                while reset == False: 
                    print('yo2')
                    read_usb = self.port.readline().decode("utf-8").replace(" \r\n",'').split(',')
                    if read_usb[0]=='sensor': 
                        self.port.reset_input_buffer() #pour éviter que le message le heading s'envoie plein de fois si on appuie longuement
                        continue
                    if int(read_usb[1]) <= 5:
                        reset = True
                        print('break')
                    self.port.reset_input_buffer()
                heading = True
            
            if mode == 'in_session':
                print('yo1')
                self.create_new_session() ###crée une nouvelle session lorsque le temps est remis à zéro
                time.sleep(1)
                while reset == False: 
                    print('yo2')
                    read_usb = self.port.readline().decode("utf-8").replace(" \r\n",'').split(',')
                    if read_usb[0]=='sensor': 
                        self.port.reset_input_buffer() #pour éviter que le message le heading s'envoie plein de fois si on appuie longuement
                        continue
                    if int(read_usb[1]) <= 5:
                        reset = True
                        print('break')
                    self.port.reset_input_buffer()
                heading = True
            


    def create_folder(self):
        #get date of capture
        date = datetime.datetime.now().strftime("%Y_%m_%d")
        self.date = date
        #create the folder named after the day of capture
        path = Path(os.path.abspath(__file__))
        path = path.parent.joinpath("SAVED_DATA").joinpath(User.currentUser).joinpath(str(date))
        if path.exists() == False:
            os.mkdir(path)
        return path
    
    def create_new_session(self):
        i = 1

        data_path = self.create_folder().joinpath('session'+str(i)) 
        existence = data_path.exists()

        while existence is True:
            i+=1
            data_path = self.create_folder().joinpath('session'+str(i))
            existence = data_path.exists()

        os.mkdir(data_path)
        self.data_path = data_path.joinpath('DATA.csv')
        self.write_time()
       

    def write_time(self):
        creation_time = str(datetime.datetime.now().strftime("%H:%M"))
        file1 = open(self.data_path.parent.joinpath("time.txt"),"w") 
        file1.write(creation_time+"\n")
        file1.close()

    def write_ref_to_csv(self):
        """Writes reference to csv file"""
        with open (str(self.create_folder().parent.joinpath('REFERENCE.csv')),'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.acceleration)

    def write_data_to_csv(self,path,data_to_write):
        """writes data to csv file"""
        with open (str(path),'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_to_write)



    def save_reference(self):
        """do all the process of reading the port and saving in the csv file"""
        start = time.time()
        ref_time = time.time()-start
        self.setPort('COM4',9600)
        #delete reference to update it
        reference_path = self.create_folder().parent.joinpath("REFERENCE.csv")
        print(reference_path)
        if reference_path.exists():
            os.remove(reference_path)
        print("Recording reference")
        while ref_time <= 30: 
            self.getAcceleration()
            self.write_ref_to_csv()
            ref_time = time.time()-start


    def start_data(self):
        self.setPort('COM3',9600)
        self.reset_microbit()
        self.check_for_heading(mode='in session')
        print("Recording starts now...")

    def save_loop(self):
        self.getAcceleration()
        print(self.acceleration)
        if self.acceleration[0] == 'sensor':
            self.check_for_heading(mode='in_session')
        else:
            self.write_data_to_csv(self.data_path,self.acceleration)


    def reset_microbit(self):
        flag = "$"
        flag = flag.encode('utf-8')
        time.sleep(0.5)
        self.port.write(flag)

    def save_data(self):
        self.start_data()
        while True:
            self.save_loop()
            if self.reset==True:
                self.reset_microbit()
                print("reset..")
                self.reset==False
            if self.stop == True:
                self.stop = False
                self.port.close()
                break


