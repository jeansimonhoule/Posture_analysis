import pandas as pd
import joblib
import os
from pathlib import Path

from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier



class KNeighbors:
    def __init__(self,n_neighbors,weights):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights = weights)
    

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

        self.model.fit(Xdata,Ydata)


    def save_model(self):
        filepath= Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath("trained_kNeighbors.sav")
        joblib.dump(self.model,str(filepath))

    def load_model(self,filepath):
        model = joblib.load(filepath)
        return model

    
    def predict(self,data):
        prediction = self.model.predict(data)
        return prediction

def main():
    KN = KNeighbors(5,'uniform')
    data = KN.load_excel_data('for_classification_xls.xlsx')
    KN.fit(data)
    KN.save_model()
    model= KN.load_model(str(Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath("trained_kNeighbors.sav")))
    
if __name__ == "__main__":
    main()




