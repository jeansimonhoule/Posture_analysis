import csv 
import os 
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
from utils import *
import matplotlib.pyplot as plt

column_names = ["sensor","time","ax","ay","az"]


class Data:
    """Data to be analyzed, caracterized by: 
    -day of csv file containing the data
    -range of acceptability for acceleration values
    -epoch lenght"""

    today = datetime.datetime.now().strftime("%Y_%m_%d")

    def __init__(self,classification_dict,epoch_lenght,day=today):
        
        root = Path(os.path.abspath(__file__))
        
        self.day=day
        self.Data_path = root.parent.joinpath("SAVED_DATA/"+self.day+"/DATA.csv") #default is the present day
        self.Reference_path = self.Data_path.parent.joinpath("REFERENCE.csv")
        self.classification_dict = classification_dict
        self.epoch_lenght = epoch_lenght


    def get_reference(self):
        ref_data = pd.read_csv(self.Reference_path,names=column_names)
        reference = {}

        for i in range(0,2):
            reference[(i,"ax")] = ref_data[ref_data['sensor'] == i]['ax'].mean()
            reference[(i,"ay")] = ref_data[ref_data['sensor'] == i]['ay'].mean()
            reference[(i,"az")] = ref_data[ref_data['sensor'] == i]['az'].mean()

        return reference


    def mean_by_epoch(self,reference,sensor,axe):
        "Split data from csv file in epochs of specified lenght"

        real_data = pd.read_csv(self.Data_path,names=column_names)
        max_time = real_data['time'].max()
        time_index = 0
        data_by_epoch = {}

        while time_index <= max_time:

            epoch_mean = real_data[real_data['sensor'] == sensor][real_data['time']>=time_index][real_data['time']<=time_index+self.epoch_lenght].mean()

            if pd.isnull(epoch_mean[axe]) == True:
                pass

            else:
                difference = abs(round_to_x(epoch_mean[axe]-reference[sensor,axe],x=100))
                data_by_epoch[time_index] = self.classification_dict[difference]

            time_index+=self.epoch_lenght

        return data_by_epoch

        


classification_dict = {
    0 : 1,
    100 : 2,
    200 : 3,
    300 : 4,
    400 : 5,
    500 : 5,
    600 : 5,
    700 : 5,
    800 : 5,
    900 : 5,
    1000 : 5
}

 
data = Data(classification_dict,2000,day="2020_11_06")
print("__________________Sensor 0__________________")
print("ax")
ax0 = data.mean_by_epoch(data.get_reference(),0,"ax")
print(ax0)
print("ay")
ay0 = data.mean_by_epoch(data.get_reference(),0,"ay")
print(ay0)
print("az")
az0 = data.mean_by_epoch(data.get_reference(),0,"az")
print(az0)
print("__________________Sensor 1__________________")
print("ax")
ax1 = data.mean_by_epoch(data.get_reference(),1,"ax")
print(ax1)
print("ay")
ay1 = data.mean_by_epoch(data.get_reference(),1,"ay")
print(ay1)
print("az")
az1 = data.mean_by_epoch(data.get_reference(),1,"az")
print(az1)

dict0 = {}
dict1 = {}
for keys in ax0:
    try:
        dict0[keys] = (ax0[keys]+ay0[keys]+az0[keys])/3
        dict1[keys] = (ax1[keys]+ay1[keys]+az1[keys])/3
    except KeyError:
        continue


print("dict1")
print(dict1)
f = plt.figure(1)
plt.plot(*zip(*sorted(dict1.items())))
g = plt.figure(2)
plt.plot(*zip(*sorted(dict0.items())))

plt.show()

