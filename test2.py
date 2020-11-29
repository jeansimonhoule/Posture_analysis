import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def chunk_the_data(period):
    data_path = "C:/Users/Jeans/Posture_analysis/SAVED_DATA/2020_11_22/session5/DATA.csv"
    column_names = ["sensor","time","ax","ay","az"]
    real_data = pd.read_csv(data_path,names=column_names)
    max_time = real_data.time.max()
    n_chunks = int(np.ceil(max_time/period))
    time_frame = np.arange(0,(n_chunks*period)+1,step=period)
    chunk_data= []
    for i in range(0,n_chunks):
        start_time = time_frame[i]
        end_time = time_frame[i+1]
        chunk_data.append(real_data[(real_data.time>=start_time) & (real_data.time<end_time) & (real_data.sensor == 1)])
    return chunk_data

chunked = chunk_the_data(300)
mean1 = np.mean(chunked[0])
print(mean1)
print(mean1.ax)

