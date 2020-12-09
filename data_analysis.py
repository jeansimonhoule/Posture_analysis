import csv 
import os 
import numpy as np
import pandas as pd
from pathlib import Path
import datetime
import matplotlib.pyplot as plt
import json
from classification import kNeighbors
from user import User


class Data:
    """Data to be analyzed, caracterized by: 
    -day of csv file containing the data
    -range of acceptability for acceleration values
    -epoch lenght"""

    def __init__(self,session,day):
        
        root = Path(os.path.abspath(__file__))
        
        self.day=day
        self.session = session
        self.Data_path = root.parent.joinpath("SAVED_DATA").joinpath(User.currentUser).joinpath(self.day).joinpath(self.session).joinpath("DATA.csv") 
        
        self.column_names = ["sensor","time","ax","ay","az"]
        self.posture_type = {}
        self.final_class = []
        
        self.data = pd.read_csv(self.Data_path,names=self.column_names)
        self.epoch_lenght = self.decide_epoch_lenght()

    def decide_epoch_lenght(self):
        #we want at least 4 time period and max 5 minutes 
        max_time = self.data.time.max()
        epoch_length = np.ceil(max_time/4)
        if epoch_length > 300:
            epoch_length = 300
        print(epoch_length)
        return epoch_length
    
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

    def compute_angle_of_chunks(self,data_chunk):
        #prend en paramètre un morceau de data et un sensor (ex: le deuxième 5 minutes et le capteur de la taille)
        X_to_predict = []
        for i in range(0,2):
            sensor_data = data_chunk[data_chunk.sensor == i]

            angle_gd = np.rad2deg(np.arctan(sensor_data.ax.mean()/sensor_data.ay.mean()))
            
            angle_aa = np.rad2deg(np.arctan(sensor_data.az.mean()/sensor_data.ay.mean()))
            X_to_predict.append(angle_gd)
            X_to_predict.append(angle_aa)

        X_to_predict = [X_to_predict]
        return X_to_predict


    def time_label(self):
        #get initialization time from text file
        file1 = open(self.Data_path.parent.joinpath("time.txt"),"r")
        time = file1.readline()
        self.time = datetime.datetime(2020,1,1,hour=int(time[0]+time[1]),minute=int(time[3]+time[4]))
        file1.close()
        
        #create array for time of each epoch
        time_label = []
        for i in range(len(self.final_class)):
            time_index = self.time + datetime.timedelta(seconds=i*self.epoch_lenght)
            time_index = time_index.strftime("%H:%M")
            time_label.append(time_index)
        with open(self.Data_path.parent.joinpath("times.json"), 'w') as f:
            json.dump(time_label,f)
        self.times = time_label
        return time_label


    def get_figures(self):
        bg_color = (0.85,0.90,1)
        fig1 = plt.figure(1)
        fig1.patch.set_facecolor(bg_color)
        ax = plt.subplot(111)

        #add 3 blank time at the beginning to make sure ylabel are placed in correct order
        self.time_label()
        label_initialize = [self.times[0],self.times[0],self.times[0]]
        timeLabel = label_initialize+self.times
        
        #add 3 blank positions at the beginning to make sure ylabel are placed in correct order
        label_pos = [0,0,0]
        x = np.arange(1,len(self.final_class)+1)
        x = np.insert(x,0,label_pos)

        #add the label and one blank space so that first label starts higher than x axis
        label = ["","Good","Bad"]
        result = self.binaryClass
        y_data = label+result
    
        ax.bar(timeLabel,y_data,color=self.colors)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.xticks(rotation=45)
        plt.yticks(fontsize=15)
        ax.set_facecolor(bg_color)
        plt.savefig(self.Data_path.parent.joinpath("result1.png"),bbox_inches="tight",facecolor=bg_color)
        plt.close()
    
    def load_Kneighbors(self):
        loadpath = self.Data_path.parents[3].joinpath("trained_kNeighbors.sav")
        self.classifier = kNeighbors()
        self.classifier.load_model(str(loadpath))

    
    def get_prediction(self,X):
        prediction = self.classifier.predict_class(X)
        return prediction
    
    def get_binary_and_coloured(self,finalClass):
        binaryclass = []
        colorList = []
        for classe in finalClass:
            if classe == "perfect":
                colorList.append((0.09,0.74,0.11,1))
                binaryclass.append("Good")
            else: 
                colorList.append((0.88,0.16,0.16,1))
                binaryclass.append("Bad")
        colorList = [(0,0,0,0),(0,0,0,0),(0,0,0,0)]+colorList
        self.colors = colorList
        self.binaryClass = binaryclass


    def get_classification(self):
        self.load_Kneighbors()
        for i in range(len(self.chunked_data)):
            X_to_predict = self.compute_angle_of_chunks(self.chunked_data[i])
            prediction  = self.get_prediction(X_to_predict)
            self.final_class.append(prediction)
        self.get_binary_and_coloured(self.final_class)
        

    def save_posture_type(self):
        for i,time in enumerate(self.times):
            self.posture_type[time] = self.final_class[i]

        with open(self.Data_path.parent.joinpath("postures.json"), 'w') as filef:
            json.dump(self.posture_type,filef)


    def analyze_my_data(self):
        self.chunk_the_data()
        self.get_classification()
        self.time_label()
        self.get_figures()
        self.save_posture_type()

