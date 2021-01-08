from settings import PATH_TO_SELECTORS
from np_datasets_wizard.utils import np_to_json
import easygui
import json
import numpy as np


def select_and_load_json():
    file_path = easygui.fileopenbox("Select json with data")
    with open(file_path, 'r') as f:
        return json.load(f), file_path


def save_selector_to_file(selector, filename):
    path = PATH_TO_SELECTORS + filename + ".json"
    print("Saving selector to " + path + "...")
    # nupmy arrays are not json serializanle, so make them lists:
    if len(selector.keys()) < 2:
        print("Selector is empty, abort saving.")
        return
    for patient_id in selector.keys():
        if patient_id == "dataset":
            continue
        for point in selector[patient_id].keys():
            measurement_at_point = selector[patient_id][point]
            selector[patient_id][point] = measurement_at_point.tolist()
    with open(path, 'w') as f:
        json.dump(selector, f)



def restore_selector_from_file(filename=None):
    if filename is None:
        filename = easygui.fileopenbox("Select file with saved SELECTOR")
    with open(filename, 'r') as f:
        selector = json.load(f)
        for patient_id in selector.keys():
            if patient_id == "dataset":
                continue
            for point in selector[patient_id].keys():
                measurement_at_point = selector[patient_id][point]
                selector[patient_id][point] = np.array(measurement_at_point)
        return selector
    return None


def cut_from_signal(np_signal, patch_len, center_point):
    half = int(patch_len / 2)
    start = center_point - half
    end = start + patch_len
    if end >= len(np_signal[0]) or start < 0:
        return None
    return np_signal[:, start:end]


def get_dataset_for_selector(selector):
    path_to_json_dataset = selector["dataset"]
    with open(path_to_json_dataset, 'r') as f:
        return json.load(f)
    return None


def save_np_u_selectors(cutted_signals_batch, contexts_batch, name):
    signal_patches_filename = PATH_TO_SELECTORS + name + ".sig"
    measurs_filename = PATH_TO_SELECTORS + name + ".conext"
    np_to_json(np.array(cutted_signals_batch), signal_patches_filename)
    np_to_json(np.array(contexts_batch), measurs_filename)
    print ("Saved signal: " + signal_patches_filename)
    print("Saved context: " + measurs_filename)

