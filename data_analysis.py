import csv 
import os 
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
from utils import *
import matplotlib.pyplot as plt
import seaborn
import json



class Data:
    """Data to be analyzed, caracterized by: 
    -day of csv file containing the data
    -range of acceptability for acceleration values
    -epoch lenght"""

    def __init__(self,session,day):
        
        root = Path(os.path.abspath(__file__))
        
        self.day=day
        self.session = session
        self.time = ""
        self.Data_path = root.parent.joinpath("SAVED_DATA").joinpath(self.day).joinpath(self.session).joinpath("DATA.csv") 
        self.Reference_path = self.Data_path.parents[2].joinpath("REFERENCE.csv")
        self.classification_dict = {0 : 1,100 : 2,200 : 3,300 : 4,400 : 5,500 : 5,600 : 5,700 : 5, 800 : 5,900 : 5,1000 : 5}
        
        self.epoch_lenght = 60 # 300 secondes car nous voulons des périodes de 5 minutes
        self.column_names = ["sensor","time","ax","ay","az"]
        self.sensor_waist= []
        self.sensor_torso= []
        #self.waist
        self.final_class = []
        self.angle_reference = {}

    def get_mean_reference(self):
        "Compute mean acceleration from reference.csv file"
        ref_data = pd.read_csv(self.Reference_path,names=self.column_names)
        reference= {}
        for i in range(0,2):
            reference[(i,"ax")] = ref_data[ref_data['sensor'] == i]['ax'].mean()
            reference[(i,"ay")] = ref_data[ref_data['sensor'] == i]['ay'].mean()
            reference[(i,"az")] = ref_data[ref_data['sensor'] == i]['az'].mean()

        self.angle_reference['Torso_gd'] = np.rad2deg(np.arctan(reference[(0,"ax")]/reference[(0,"ay")]))
        self.angle_reference['Torso_aa'] = np.rad2deg(np.arctan(reference[(0,"az")]/reference[(0,"ay")]))
        self.angle_reference['Waist_gd'] = np.rad2deg(np.arctan(reference[(1,"ax")]/reference[(1,"ay")]))
        self.angle_reference['Waist_aa'] = np.rad2deg(np.arctan(reference[(1,"az")]/reference[(1,"ay")]))
        

    def load_data(self):
        self.data = pd.read_csv(self.Data_path,names=self.column_names)
        self.get_time()
    
    def get_time(self):
        file1 = open(self.Data_path.parent.joinpath("time.txt"),"r")
        time = file1.readline()
        self.time = datetime.datetime(2020,1,1,hour=int(time[0]+time[1]),minute=int(time[3]+time[4]))
        file1.close()

    def chunk_the_data(self):

        max_time = self.data.time.max()
        n_chunks = int(np.ceil(max_time/self.epoch_lenght))
        time_frame = np.arange(0,(n_chunks*self.epoch_lenght)+1,step=self.epoch_lenght)
        chunked_data= []
        for i in range(0,n_chunks):
            start_time = time_frame[i]
            end_time = time_frame[i+1]
            chunked_data.append(self.data[(self.data.time>=start_time) & (self.data.time<end_time)])
        self.chunked_data = chunked_data

    def compute_angle_of_chunks(self,data_chunk,sensor):
        #prend en paramètre un morceau de data et un sensor (ex: le deuxième 5 minutes et le capteur de la taille)
        sensor_class, class_gd, class_aa = 0,0,0
        sensor_data = data_chunk[data_chunk.sensor == sensor]
        
        if sensor == 0: 
            angle_gd_ref = self.angle_reference['Torso_gd']
            angle_aa_ref = self.angle_reference['Torso_aa']
        
        if sensor == 1: 
            angle_gd_ref = self.angle_reference['Waist_gd']
            angle_aa_ref = self.angle_reference['Waist_aa']

        angle_gd = np.rad2deg(np.arctan(sensor_data.ax.mean()/sensor_data.ay.mean()))
        diff_angle_gd = angle_gd_ref-angle_gd

        # classification de l'angle gauche/droite
        if abs(diff_angle_gd) <= 10:
            class_gd = 1

        elif abs(diff_angle_gd) <=15:
            class_gd = 2
        
        elif abs(diff_angle_gd) <=20:
            class_gd = 3
        
        else:
            class_gd = 4
        
        # classification de l'angle avant/arrière
        angle_aa = np.rad2deg(np.arctan(sensor_data.az.mean()/sensor_data.ay.mean()))
        diff_angle_aa = angle_aa_ref-angle_aa

        if abs(diff_angle_aa) <= 5: 
            class_aa = 1
     
        elif abs(diff_angle_aa) <= 10:
            class_aa= 2
        
        elif abs(diff_angle_aa) <=15:
            class_aa = 3
        
        else:
            class_aa = 4
        
        sensor_class = np.maximum(class_gd,class_aa)
        print(diff_angle_gd,diff_angle_aa)

        if sensor == 1:
            self.sensor_waist.append(sensor_class)
        if sensor == 0:
            self.sensor_torso.append(sensor_class)

    def time_label(self):
        time_label = []
        for i in range(len(self.final_class)):
            time_index = self.time + datetime.timedelta(seconds=i*self.epoch_lenght)
            time_index = time_index.strftime("%H:%M")
            time_label.append(time_index)
        with open(self.Data_path.parent.joinpath("times.json"), 'w') as f:
            json.dump(time_label,f)
        return time_label


    def get_figures(self):
        #plt.rcParams["font.family"] = "roboto"
        bg_color = (0.88,0.88,0.88)
        fig1 = plt.figure(1)
        fig1.patch.set_facecolor(bg_color)
        ax = plt.subplot(111)

        timeLabel = self.time_label()
        label_initialize = [timeLabel[0],timeLabel[0],timeLabel[0],timeLabel[0],timeLabel[0]]
        timeLabel = label_initialize+timeLabel
        print(timeLabel)
        #to change for time
        #timeLabel = self.time_label(self)
        label_pos = [0,0,0,0,0]
        x = np.arange(1,len(self.final_class)+1)
        x = np.insert(x,0,label_pos)

        label = ["","parfait","bien","attention","à corriger"]
        result = self.final_class
        y_data = label+result
        barlist = ax.bar(timeLabel,y_data,color=self.colors)
        for i in range(4):
            barlist[i].set_color((0,0,0,0))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.xticks(rotation=45)
        ax.set_facecolor(bg_color)
        plt.savefig(self.Data_path.parent.joinpath("result1.png"),bbox_inches="tight")

        fig2 = plt.figure(2)
        fig2.patch.set_facecolor(bg_color)
        plt.pie([15,15,15,55],shadow=True)
        plt.savefig(self.Data_path.parent.joinpath("result2.png"))
    
    
    def get_classification(self):
        for i in range(len(self.chunked_data)):
            self.compute_angle_of_chunks(self.chunked_data[i],0)
            self.compute_angle_of_chunks(self.chunked_data[i],1)
            self.final_class.append(np.maximum(self.sensor_torso[i],self.sensor_waist[i]))
        qualitative, colors = self.get_qualitative_and_coloured(self.final_class)
        self.final_class = qualitative
        self.colors = colors

    def get_qualitative_and_coloured(self,numberList):
        qualitativeList = []
        colorList = []
        for number in numberList:
            if number==1:
                qualitativeList.append("parfait")
                colorList.append((0.18,0.40,0.78,1)) #blue
            elif number == 2:
                qualitativeList.append("bien")
                colorList.append((0.24,0.65,0.25,1)) #green
            elif number == 3:
                qualitativeList.append("attention")
                colorList.append((0.96,0.86,0.22,1)) #yellow
            elif number == 4:
                qualitativeList.append("à corriger")
                colorList.append((0.98,0.26,0.15,1)) #red
            else:
                qualitativeList.append("")
                colorList.append((0,0,0,0))
        colorList = [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)]+colorList
        print(qualitativeList)
        print(colorList)
        return qualitativeList,colorList


    def analyze_my_data(self):
        self.get_mean_reference()
        self.load_data()
        self.chunk_the_data()
        self.get_classification()
        self.get_figures()

def main():
    data = Data("session5","2020_11_22")
    data.get_mean_reference()
    data.load_data()
    data.chunk_the_data()
    print('GD---------------AA')
    data.get_classification()
    print(data.sensor_torso)
    print(data.sensor_waist)
    print(data.angle_reference['Waist_gd'],data.angle_reference['Waist_aa'])
    print(data.final_class)
    data.time_label()
    data.get_figures()


if __name__ == '__main__':
    main()
