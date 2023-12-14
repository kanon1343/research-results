import os
import pathlib
import re
from numpy import sort
import pandas as pd
from pandas.errors import EmptyDataError

target_path_template = "{option}/{project}-log"

def show_generation_number(target_path, seed):
    correct_filename = "{target_path}/correct_patch{seed}.csv".format(target_path=str(target_path), seed=seed)
    try:
        correct_df = pd.read_csv(correct_filename, sep=',')
        correct_patch_list = correct_df['0'].to_list()
        correct_patch_ids = [int(line.split("/")[1]) for line in correct_patch_list]
    except EmptyDataError:
        correct_patch_ids = []

    print(str(len(correct_patch_ids)) + ", ", end="")

if __name__ == "__main__":
    options = ["50-50-25", "100-100-50", "200-200-100"]
    projects = ["codec8", "codec9"]
    for option in options:
        print(option)
        for project in projects:
            for seed in range(10):
                target_path = pathlib.Path(target_path_template.format(option=option, project=project))
                show_generation_number(target_path, seed)
            print()
            
                
