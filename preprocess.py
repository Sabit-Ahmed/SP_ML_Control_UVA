import pandas as pd
import numpy as np
import os

resource_path = "/home/ycl/Desktop/ML_SP/data_csv/"
result = pd.DataFrame(columns=['x_mean','x_std','y_mean','y_std','z_mean','z_std','activity'])
file = os.listdir(resource_path)
for f in file:
    df = pd.read_csv('data_csv/'+f,header = None)
    nameSrc = f
    activity = ''
    if nameSrc.find("not") == -1:
        activity = 'wash'
    else:
        activity = 'not wash'

    new_colums = ['time','x','y','z']
    df.columns = new_colums
    tempo = 0
    X = []
    Y = []
    Z = []

    time = 0
    i = 0
    for index, row in df.iterrows():
        if tempo == 0:
            X.append(float(row['x']))
            Y.append(float(row['y']))
            Z.append(float(row['z']))
            time = row['time']
            tempo = 1
        else:
            if int(row['time'])-time < 1000:
                X.append(float(row['x']))
             
                Y.append(float(row['y']))
                Z.append(float(row['z']))
                continue
            else:
                result.loc[i] = [np.mean(X),np.std(X),np.mean(Y),np.std(Y),np.mean(Z),np.std(Z),activity]
                i = i + 1
                X.clear()
                Y.clear()
                Z.clear()
                X.append(float(row['x']))
                Y.append(float(row['y']))
                Z.append(float(row['z']))
                time = row['time']
                continue
result.to_csv('result.csv', index= False)