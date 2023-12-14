import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

output_path = "."
target_path_template = "{option}/{project}-log"

def draw_graph(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, project):
    plt.figure()
    fig, ax = plt.subplots(figsize=[6.4, 4.8])

    ax.plot(x1, y1, label="A50")
    ax.plot(x2, y2, label="A100")
    ax.plot(x3, y3, label="A200")
    ax.plot(x4, y4, "--", label="U50")
    ax.plot(x5, y5, "--", label="U100")
    ax.plot(x6, y6, "--", label="U200")
    ax.set_xlim(-1000, 87000)
    ax.set_xticks([0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000])
    ax.set_ylim(-10, 1000)
    ax.set_yticks([0, 200, 400, 600, 800, 1000])
    ax.set_xlabel("Time(seconds)")
    ax.set_ylabel("Accumulated Program")
    ax.legend()

    axins = ax.inset_axes([0.4, 0.2, 0.5, 0.3])
    axins.plot(x1, y1, label="A50")
    axins.plot(x2, y2, label="A100")
    axins.plot(x3, y3, label="A200")
    axins.set_xlim(0, 20000)
    axins.set_xticks([0, 10000, 20000])
    axins.set_ylim(0, 10)
    axins.set_yticks([0, 5, 10])
    ax.indicate_inset_zoom(axins)

    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.08, top=0.95)
    plt.savefig("{output_path}/{project}.pdf".format(output_path=output_path, project=project), bbox_inches='tight')

def get_filename(option, project):
    target_path = pathlib.Path(target_path_template.format(option=option, project=project))
    filename = "{target_path}/summary-info.csv".format(target_path=str(target_path))
    return filename
    
def draw():
    project = "math85"

    df = pd.read_csv(get_filename("50-50-25", project), sep=',')
    x1 = df['Time'].to_list()
    y1 = df['Accumulated Acceptable'].to_list()
    x4 = df['Time'].to_list()
    y4 = df['Accumulated Unacceptable'].to_list()

    df = pd.read_csv(get_filename("100-100-50", project), sep=',')
    x2 = df['Time'].to_list()
    y2 = df['Accumulated Acceptable'].to_list()
    x5 = df['Time'].to_list()
    y5 = df['Accumulated Unacceptable'].to_list()
    
    df = pd.read_csv(get_filename("200-200-100", project), sep=',')
    x3 = df['Time'].to_list()
    y3 = df['Accumulated Acceptable'].to_list()
    x6 = df['Time'].to_list()
    y6 = df['Accumulated Unacceptable'].to_list()

    draw_graph(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, project)

if __name__ == "__main__":
    draw()
