from settings import PATH_TO_NUMPY_DATA_FOLDER
from np_datasets_wizard.utils import np_to_json
import easygui
import json
import numpy as np
import random

def get_lead_signal(ecg, lead_name):
    return ecg['Leads'][lead_name]['Signal']


def one_patient_to_np(leads_names, patient_json_node):
    result = []
    for lead_name in leads_names:
        lead_signal = get_lead_signal(patient_json_node, lead_name)
        result.append(lead_signal)
    return np.array(result)

def cut_from_signal_at_random_point(np_patinet, patch_len):
    len_of_signal = len(np_patinet[0])
    random_start = random.randint(0, len_of_signal- patch_len -1)
    return np_patinet[:, random_start:random_start+patch_len]

def get_numpy_from_json(json_data, patch_len, leads_names, amount_of_patches):
    result = []
    labels = []
    counter = 0
    len_keys = len(json_data.keys())
    keys = list(json_data.keys())
    while counter < amount_of_patches:
        for i in range(len_keys):
            patient_id = keys[i]
            patient_json_node = json_data[patient_id]
            np_patinet = one_patient_to_np(leads_names, patient_json_node)
            cutted = cut_from_signal_at_random_point(np_patinet, patch_len)
            if cutted is not None:
                result.append(cutted)
                labels.append(i)
                counter += 1
                if counter == amount_of_patches:
                    break
    return np.array(result), np.array(labels)


def select_and_load_json():
    file_path = easygui.fileopenbox("Select json medical dataset")
    with open(file_path, 'r') as f:
        return json.load(f)


def make_and_save_random_dataset(patch_len, name, leads_names, amount_of_patches):
    json_data = select_and_load_json()
    numpy_data, numpy_labels = get_numpy_from_json(json_data, patch_len, leads_names, amount_of_patches)
    signal_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".np"
    np_to_json(numpy_data, signal_path)
    label_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".sig"
    np_to_json(numpy_labels, label_path)
    print("np dataset saved to " + str(signal_path))
    print("shape: " + str(numpy_data.shape))


if __name__ == "__main__":
    patch_len = 8
    amount_of_patches = 600
    name = "ALL_random_patchlen"+ str(patch_len) + "_size" + str(amount_of_patches)
    make_and_save_random_dataset(patch_len, name, ["i"], amount_of_patches)
