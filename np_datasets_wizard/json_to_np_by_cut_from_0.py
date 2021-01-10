from settings import PATH_TO_NUMPY_DATA_FOLDER
from np_datasets_wizard.utils import np_to_json
import easygui
import json
import numpy as np


def get_lead_signal(ecg, lead_name):
    return ecg['Leads'][lead_name]['Signal']


def cut_from_signal(ecg, start_point, leads_names, patch_len):
    result = []
    for lead_name in leads_names:
        lead_signal = get_lead_signal(ecg, lead_name)
        end_point = start_point + patch_len
        if start_point < 0 or end_point > len(lead_signal):
            return None
        result.append(lead_signal[start_point:end_point])
    return result


def get_numpy_from_json(json_data, patch_len, leads_names):
    start_point = 0
    result = []
    for patient_id in json_data.keys():
        patient = json_data[patient_id]
        cutted = cut_from_signal(patient, start_point, leads_names, patch_len)
        if cutted is not None:
            result.append(cutted)
    return np.array(result)


def select_and_load_json():
    file_path = easygui.fileopenbox("Select json with data")
    with open(file_path, 'r') as f:
        return json.load(f)


def make_and_save_dataset(patch_len, name, leads_names):
    json_data = select_and_load_json()
    numpy_data = get_numpy_from_json(json_data, patch_len, leads_names)
    file_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".json"
    np_to_json(numpy_data, file_path)
    print("np dataset saved to " + str(file_path))
    print("shape: " + str(numpy_data.shape))


if __name__ == "__main__":
    make_and_save_dataset(4998, "t_without_qrs_visualis", ["i"])
