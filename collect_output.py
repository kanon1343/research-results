import os
import pathlib
import re
from numpy import sort
import pandas as pd
import numpy as np

target_path_template = "{option}/{project}-log"

def merge(target_path):
    column = ["Generation", "Time", "All", "Acceptable", "Unacceptable"]
    ret_df = pd.DataFrame([], columns=column, index=None)

    for seed in range(10):
        filename = "{target_path}/seed{seed}-info.csv".format(target_path=str(target_path), seed=seed)
        df = pd.read_csv(filename, sep=',')
        ret_df = pd.concat([ret_df, df])
    return ret_df

def convert_time_to_seconds(time_string):
    pattern = r'(\d+)\s*hours?\s*(\d+)\s*minutes?\s*(\d+)\s*seconds?'
    matches = re.match(pattern, time_string)

    if matches:
        hours = int(matches.group(1))
        minutes = int(matches.group(2))
        seconds = int(matches.group(3))

        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        return total_seconds
    else:
        return 0  # when any error occurs

def parse_and_convert_time(time_string):
    if re.match(r'\d+\s*hours?\s*\d+\s*minutes?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds(time_string)
    elif re.match(r'\d+\s*minutes?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds("0 hours " + time_string)
    elif re.match(r'\d+\s*hours?\s*\d+\s*seconds?', time_string):
        return convert_time_to_seconds(time_string.split()[0] + " " + time_string.split()[1] + " 0 minutes " + time_string.split()[2] + " " + time_string.split()[3])
    elif re.match(r'\d+\s*seconds?', time_string):
        return convert_time_to_seconds("0 hours 0 minutes " + time_string)
    else:
        return 0

def convert_to_generation_number(str):
    matches = re.match(r'(\d+)*', str)
    number = int(matches.group(1))
    return number
    
def sort_by_time(df):
    generation_list = df['Generation'].to_list()
    generation_number_list = [convert_to_generation_number(generation_string.strip()) for generation_string in generation_list]
    df.insert(0, 'Generation2', generation_number_list)
    
    time_list = df['Time'].to_list()
    second_list = [parse_and_convert_time(time_string.strip()) for time_string in time_list]
    df.insert(1, 'Time2', second_list)

    df = df.drop(columns=['Generation', 'Time'])
    df = df.rename(columns={'Time2': 'Time'})
    df = df.rename(columns={'Generation2': 'Generation'})
    df = df.sort_values('Time').reset_index(drop=True)
    return df
    
def count(target_path, df):
    df = df.groupby('Time', as_index=False).agg({'All': np.sum, 'Acceptable': np.sum, 'Unacceptable': np.sum})

    new_data = []
    accumulated_all = 0
    accumulated_acceptable = 0
    accumulated_unacceptable = 0
    for index, data in df.iterrows():
        accumulated_all = accumulated_all + data[1]
        accumulated_acceptable = accumulated_acceptable + data[2]
        accumulated_unacceptable = accumulated_unacceptable + data[3]
        
        new_data.append([data[0], accumulated_all, accumulated_acceptable, accumulated_unacceptable])
        
    column = ["Time", "Accumulated All", "Accumulated Acceptable", "Accumulated Unacceptable"]
    new_df = pd.DataFrame(new_data, columns=column, index=None)
    return new_df

def output(target_path, df):
    filename = "{target_path}/summary-info.csv".format(target_path=str(target_path))
    df.to_csv(filename, header=True, index=False)

if __name__ == "__main__":
    options = ["50-50-25", "100-100-50", "200-200-100"]
    projects = ["codec8", "codec9"]
    pd.set_option('display.max_rows', None)
    for option in options:
        for project in projects:
            print(option + " - " + project)

            target_path = pathlib.Path(target_path_template.format(option=option, project=project))
            df = merge(target_path)
            df = sort_by_time(df)
            df = count(target_path, df)
            output(target_path, df)
