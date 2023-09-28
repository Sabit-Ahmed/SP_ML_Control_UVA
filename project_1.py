import pandas as pd
import numpy as np
import os

data_dir = "data/project_1/formatted_data/"


def read_csv_file():
    files = os.listdir(f"{data_dir}")
    df = pd.read_csv(f"{data_dir+files[0]}", names=['timestamp','x-axis','y-axis','z-axis'])
    print(df.describe())

def read_csv_files():
    files = os.listdir(f"{data_dir}")
    for j in files:
        df = pd.read_csv(f"{data_dir+j}")
