import csv 
import os 
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
from utils import *


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
        ref_data = pd.read_csv(self.Reference_path)
        reference = np.zeros((2,3))

        for i in range(0,2):
            reference[i,0] = ref_data[ref_data['sensor'] == i]['ax'].mean()
            reference[i,1] = ref_data[ref_data['sensor'] == i]['ay'].mean()
            reference[i,2] = ref_data[ref_data['sensor'] == i]['az'].mean()

        return reference


    def mean_by_epoch(self,reference):
        "Split data from csv file in epochs of specified lenght"

        real_data = pd.read_csv(self.Data_path)
        max_time = real_data['time'].max()
        time_index = 0
        data_by_epoch = {}

        while time_index <= max_time:

            epoch_mean = real_data[real_data['sensor'] == 0][real_data['time']>=time_index][real_data['time']<=time_index+self.epoch_lenght].mean()

            if pd.isnull(epoch_mean['ax']) == True:
                pass

            else:
                difference = abs(round_to_x(epoch_mean['ax']-reference[0,0],x=100))
                data_by_epoch[time_index] = self.classification_dict[difference]

            time_index+=self.epoch_lenght

        return data_by_epoch

        


classification_dict = {
    0 : "a",
    100 : "b",
    200 : "c",
    300 : "d",
    400 : "e",
    500 : "e",
    600 : "e",
    700 : "e",
    800 : "e",
    900 : "e",
    1000 : "e"
}

 
data = Data(classification_dict,2000,day="2020_10_24")
print(data.mean_by_epoch(data.get_reference()))