import pandas as pd
import joblib
import os
from pathlib import Path

from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier



class kNeighbors:
    def __init__(self):
        self.kN = KNeighborsClassifier()
    

    def load_csv_data(self,path):
        names = ['gdTorso','aaTorso','gdWaist','aaWaist','Label']
        data = pd.read_csv(path,names=names)
        return data

    
    def load_excel_data(self,path):
        names = ['gdTorso','aaTorso','gdWaist','aaWaist','Label']
        data = pd.read_excel(path,names=names)
        return data

    def fit(self,data):
        array = data.values
        Xdata = array[:,0:4]
        Ydata = array[:,4]

        self.kN.fit(Xdata,Ydata)


    def save_model(self):
        filepath= Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath("trained_kNeighbors.sav")
        joblib.dump(self.kN,str(filepath))

    def load_model(self,filepath):
        model = joblib.load(filepath)
        self.kN = model

    
    def predict_class(self,data):
        prediction = self.kN.predict(data)
        return prediction[0]


def main():
    KN = kNeighbors()
    KN.load_model(str(Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath("trained_kNeighbors.sav")))
    pred = KN.predict_class([[2.5039291724004964, -8.215638537231916, -9.524017421703224, 18.638557701132036]])
    print(pred)
if __name__ == "__main__":
    main()





