import csv 
import os 
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
from utils import *
import matplotlib.pyplot as plt

column_names = ["sensor","time","ax","ay","az"]

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


class Data:
    """Data to be analyzed, caracterized by: 
    -day of csv file containing the data
    -range of acceptability for acceleration values
    -epoch lenght"""

    today = datetime.datetime.now().strftime("%Y_%m_%d")

    def __init__(self,session,day):
        
        root = Path(os.path.abspath(__file__))
        
        self.day=day
        self.session = session
        self.Data_path = root.parent.joinpath("SAVED_DATA").joinpath(self.day).joinpath(self.session).joinpath("DATA.csv") 
        self.Reference_path = self.Data_path.parents[2].joinpath("REFERENCE.csv")
        self.classification_dict = {0 : 1,100 : 2,200 : 3,300 : 4,400 : 5,500 : 5,600 : 5,700 : 5, 800 : 5,900 : 5,1000 : 5}
        
        self.epoch_lenght = 2000
        self.column_names = ["sensor","time","ax","ay","az"]


    def get_mean_reference(self):
        "Compute mean acceleration from reference.csv file"
        ref_data = pd.read_csv(self.Reference_path,names=column_names)
        reference = {}

        for i in range(0,2):
            reference[(i,"ax")] = ref_data[ref_data['sensor'] == i]['ax'].mean()
            reference[(i,"ay")] = ref_data[ref_data['sensor'] == i]['ay'].mean()
            reference[(i,"az")] = ref_data[ref_data['sensor'] == i]['az'].mean()

        return reference


    def compare_by_epoch(self,reference,sensor,axe):
        "Split data from csv file in epochs of specified lenght"

        real_data = pd.read_csv(self.Data_path,names=column_names)
        max_time = real_data['time'].max()
        time_index = 0
        class_by_epoch = {}

        while time_index <= max_time:

            epoch_mean = real_data[real_data['sensor'] == sensor][real_data['time']>=time_index][real_data['time']<=time_index+self.epoch_lenght].mean()

            if pd.isnull(epoch_mean[axe]) == True:
                pass

            elif type(epoch_mean[axe]) is not int:
                pass

            else:
                difference = abs(round_to_x(epoch_mean[axe]-reference[sensor,axe],x=100)) #arrondi à la centaine près
                if difference >= 1000:
                    difference = 1000
                class_by_epoch[time_index] = self.classification_dict[difference]

            time_index+=self.epoch_lenght

        return class_by_epoch

    def get_overall_result(self):
        #get classification from first sensor
        ax0 = self.compare_by_epoch(self.get_mean_reference(),0,"ax")
        ay0 = self.compare_by_epoch(self.get_mean_reference(),0,"ay")
        az0 = self.compare_by_epoch(self.get_mean_reference(),0,"az")
        #get classification from second sensor
        ax1 = self.compare_by_epoch(self.get_mean_reference(),1,"ax")
        ay1 = self.compare_by_epoch(self.get_mean_reference(),1,"ay")
        az1 = self.compare_by_epoch(self.get_mean_reference(),1,"az")

        dict0 = {}
        dict1 = {}
        for keys in ax0:
            try:
                dict0[keys] = (ax0[keys]+ay0[keys]+az0[keys])/3
                dict1[keys] = (ax1[keys]+ay1[keys]+az1[keys])/3
            except KeyError:
                continue
        self.result0 = dict0
        self.result1 = dict1

    def get_figures(self):
        plt.figure(1)
        plt.plot(*zip(*sorted(self.result0.items())))
        plt.savefig(self.Data_path.parent.joinpath("result1.png"))
        plt.figure(2)
        plt.plot(*zip(*sorted(self.result1.items())))
        plt.savefig(self.Data_path.parent.joinpath("result2.png"))


    def analyze_my_data(self):
        self.get_overall_result()
        self.get_figures()

def main():
    data = Data("session1","2020_11_06")
    data.analyze_my_data()

if __name__ == '__main__':
    main()
