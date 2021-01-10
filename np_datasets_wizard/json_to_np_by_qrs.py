from settings import PATH_TO_NUMPY_DATA_FOLDER
from np_datasets_wizard.utils import np_to_json
import easygui
import json
import numpy as np


def get_lead_signal(ecg, lead_name):
    return ecg['Leads'][lead_name]['Signal']


def get_triplets_qrs(ecg, lead_name='i'):
    return ecg['Leads'][lead_name]['DelineationDoc']['qrs']


def get_triplets_t(ecg, lead_name='i'):
    return ecg['Leads'][lead_name]['DelineationDoc']['t']


def get_triplets_p(ecg, lead_name='i'):
    return ecg['Leads'][lead_name]['DelineationDoc']['p']


def cut_from_signal(ecg, center_point, leads_names, patch_len):
    result = []
    for lead_name in leads_names:
        lead_signal = get_lead_signal(ecg, lead_name)
        start_point = center_point - int(patch_len / 2)
        end_point = start_point + patch_len
        if start_point < 0 or end_point > len(lead_signal):
            return None
        result.append(lead_signal[start_point:end_point])
    return result


def get_numpy_from_json(json_data, patch_len, leads_names):
    result = []
    for patient_id in json_data.keys():
        patient = json_data[patient_id]
        triplets = get_triplets_t(patient)
        for triplet in triplets:
            center_point = triplet[1]
            cutted = cut_from_signal(patient, center_point, leads_names, patch_len)
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
    make_and_save_dataset(256, "256_qrs_i", ["i"])
