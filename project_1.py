import pandas as pd
import numpy as np
import os

data_dir = "data/project_1/formatted_data/"


def read_csv_file():
    files = os.listdir(f"{data_dir}")
    df = pd.read_csv(f"{data_dir+files[0]}", names=['timestamp','x-axis','y-axis','z-axis'])
    df['timestamp'] = df['timestamp']/1000
    print(df.head(10))
    print(df.describe())

def df_ops():
    df = read_csv_file()
    df['timestamp'] = df['timestamp']

def read_csv_files():
    files = os.listdir(f"{data_dir}")
    for j in files:
        df = pd.read_csv(f"{data_dir+j}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # demo.read_file()
    read_csv_file()