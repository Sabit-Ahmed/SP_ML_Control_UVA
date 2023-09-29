import pandas as pd
import numpy as np
import os

data_dir = "data/project_1/formatted_data/"


def read_csv_file():
    files = os.listdir(f"{data_dir}")
    df = pd.read_csv(f"{data_dir+files[0]}", names=['timestamp','x-axis','y-axis','z-axis'])
    return df

def df_ops():
    df = read_csv_file()
    # df['timestamp'] = df['timestamp'] - df['timestamp'][0]
    # df['timestamp'] = df['timestamp']/1000
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = pd.to_timedelta(df['timestamp'].dt.time.astype(str)).dt.total_seconds()
    # print(df.head(10))
    # print(df.tail(10))
    # print(df.describe())
    feature_df = df.groupby(['timestamp'])
    mean_df = feature_df.mean().reset_index()
    std_df = feature_df.std().reset_index()
    mean_df.columns = ['timestamp', 'x-mean', 'y-mean', 'z-mean']
    std_df.columns = ['timestamp', 'x-std', 'y-std', 'z-std']
    output = pd.concat([mean_df, std_df], axis=1)
    print(output)

def read_csv_files():
    files = os.listdir(f"{data_dir}")
    for j in files:
        df = pd.read_csv(f"{data_dir+j}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # demo.read_file()
    df_ops()