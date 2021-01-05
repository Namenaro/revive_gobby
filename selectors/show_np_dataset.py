from selectors.utils import load_np_from_json

import easygui
import matplotlib.pyplot as plt

"""
Use:
1) select in dialogue file with numpy dataset of interest (shape NxMxY)
2) see a picture with first several examples of the the first lead
"""

def select_and_load_np_data():
    file_path = easygui.fileopenbox("Select json with numpy data")
    return load_np_from_json(file_path)

def np_arr_1d_to_pic(np_arr_1d):
    fig, big_axes = plt.subplots(figsize=(14.0, 14.0), nrows=3, ncols=1, sharey=True)

    for row, big_ax in enumerate(big_axes, start=1):
        big_ax.tick_params(labelcolor=(1., 1., 1., 0.0), top='off', bottom='off', left='off', right='off')
        big_ax._frameon = False

    for i in range(1, 10):
        ax = fig.add_subplot(3, 3, i)
        if i <len(np_arr_1d):
            ax.plot(np_arr_1d[i])

    fig.set_facecolor('w')
    plt.tight_layout()
    plt.show()

def show_np_dataset_1st_lead():
    np_arr = select_and_load_np_data()
    to_show = []
    for i in range(len(np_arr)):
        to_show.append(np_arr[i][0])
    np_arr_1d_to_pic(to_show)

if __name__ == "__main__":
    show_np_dataset_1st_lead()