import os
import pathlib
import re
from numpy import sort
import pandas as pd
from pandas.errors import EmptyDataError

target_path_template = "{option}/{project}-log"

def check_acceptable(ids, prev, cur, g):
    count = 0
    for id in range(prev, cur + 1):
        if id in ids:
            count = count + 1
    return count
        
def extract_generation_number(target_path, seed):
    correct_filename = "{target_path}/correct_patch{seed}.csv".format(target_path=str(target_path), seed=seed)
    try:
        correct_df = pd.read_csv(correct_filename, sep=',')
        correct_patch_list = correct_df['0'].to_list()
        correct_patch_ids = [int(line.split("/")[1]) for line in correct_patch_list]
    except EmptyDataError:
        correct_patch_ids = []
        
    log_filename = "{target_path}/seed{seed}.txt".format(target_path=str(target_path), seed=seed)
    with open(log_filename, 'r') as file:
        content = file.read()
    lines = content.split('\n')

    output_data = []
    generation_number = ''
    consumed_time = ''
    output_number = 0
    id_num = 1

    for line in lines:
        if "entered the era" in line:
            generation_number = line.split(' ')[-2]  # Extract the generation number

        if "Elapsed time" in line:
            consumed_time = line.split(":")[1]

        if "Fitness: max" in line:
            if "Fitness: max 1(" in line:
                # "Fitness: max 1(" means successfully presented a patch
                # The number sandwitched betwwen parentheses indicates the number of presented patches
                output_number = int(line.split('(')[1].split(')')[0])
                acceptance_number = check_acceptable(correct_patch_ids, id_num, id_num + output_number - 1, generation_number)
            else:
                output_number = 0
                acceptance_number = 0
            data = [generation_number, consumed_time, output_number, acceptance_number, output_number - acceptance_number]
            id_num = id_num + output_number
            output_data.append(data)

        if "GA stopped" in line:
            break

    column = ["Generation", "Time", "All", "Acceptable", "Unacceptable"]
    df = pd.DataFrame(output_data, columns=column, index=None)
    return df

def output(target_path, seed, df):
    filename = "{target_path}/seed{seed}-info.csv".format(target_path=str(target_path), seed=seed)
    df.to_csv(filename, header=True, index=False)

if __name__ == "__main__":
    options = ["50-50-25", "100-100-50", "200-200-100"]
    projects = ["codec8", "codec9"]
    for option in options:
        for project in projects:
            for seed in range(10):
                print(option + " - " + project + " - " + str(seed))
                target_path = pathlib.Path(target_path_template.format(option=option, project=project))
                df = extract_generation_number(target_path, seed)
                output(target_path, seed, df)
                
