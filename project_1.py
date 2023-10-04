import pandas as pd
import numpy as np
import os

data_dir = "data/project_1/formatted_data/"
feature_dir = "data/project_1/"

def read_csv_file():
    files = os.listdir(f"{data_dir}")
    # df = pd.read_csv(f"{data_dir + files[0]}", names=['timestamp', 'x-axis', 'y-axis', 'z-axis'])
    df = pd.read_csv(f"{data_dir + files[0]}", names=['timestamp', 'uk1', 'uk2', 'x-axis', 'y-axis', 'z-axis'])
    return df


def extract_features():
    output = pd.DataFrame()
    files = os.listdir(f"{data_dir}")
    for j in files:
        # df = pd.read_csv(f"{data_dir + j}", names=['timestamp', 'x-axis', 'y-axis', 'z-axis'])
        df = pd.read_csv(f"{data_dir + j}", names=['timestamp', 'uk1', 'uk2', 'x-axis', 'y-axis', 'z-axis'])
        df.drop(columns=['uk1', 'uk2'], inplace=True)
        df2 = df_ops(df)
        activity = j.split('-')[3]
        df2['activity'] = activity
        output = pd.concat([output, df2], axis=0)
    # print(output)
    save_csv_file(output)

def save_csv_file(df):
    df.to_csv(feature_dir+'features.csv', index=None)

def df_ops(df):
    # df['timestamp'] = df['timestamp'] - df['timestamp'][0]
    # df['timestamp'] = df['timestamp']/1000000
    # df['timestamp'] = df['timestamp'].astype(str).str[:-6]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = pd.to_timedelta(df['timestamp'].dt.time.astype(str)).dt.total_seconds().astype(int)
    # print(df.head(10))
    # print(df.tail(10))
    # print(df.describe())
    feature_df = df.groupby(['timestamp'])
    mean_df = feature_df.mean().reset_index()
    std_df = feature_df.std().reset_index()
    mean_df.drop(columns='timestamp', inplace=True)
    std_df.drop(columns='timestamp', inplace=True)
    mean_df.columns = ['x-mean', 'y-mean', 'z-mean']
    std_df.columns = ['x-std', 'y-std', 'z-std']
    output = pd.concat([mean_df, std_df], axis=1)
    # print(output)
    return output

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_features()