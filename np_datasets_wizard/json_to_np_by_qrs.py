from settings import PATH_TO_NUMPY_DATA_FOLDER
from np_datasets_wizard.utils import np_to_json
import easygui
import json
import numpy as np

SHIFT_DISPERSIA = 0.0

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

def get_shift(mode=None):
    if mode is None:
        return 0
    if mode == "normal":
        return np.random.normal(0.0, SHIFT_DISPERSIA)

def get_numpy_from_json(json_data, patch_len, leads_names):
    result = []
    labels = []
    for patient_id in json_data.keys():
        patient = json_data[patient_id]
        triplets = get_triplets_t(patient)
        for triplet in triplets:
            shift = int(get_shift("normal"))
            center_point = triplet[1] + shift
            cutted = cut_from_signal(patient, center_point, leads_names, patch_len)
            if cutted is not None:
                result.append(cutted)
                labels.append(shift)
    return np.array(result), np.array(labels)


def select_and_load_json(file_path=None):
    if file_path is None:
        file_path = easygui.fileopenbox("Select json dataset")
    with open(file_path, 'r') as f:
        return json.load(f)


def make_and_save_dataset(patch_len, name, leads_names):
    json_data = select_and_load_json()
    numpy_data, labels = get_numpy_from_json(json_data, patch_len, leads_names)
    numpy_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".np"
    label_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".labels"
    np_to_json(numpy_data, numpy_path)
    np_to_json(labels, label_path)
    print("np dataset saved to " + str(numpy_path))
    print("shape: " + str(numpy_data.shape))


def make_and_save_from2jsons(patch_len, name, leads_names):
    json_data1 = select_and_load_json()
    numpy_data1, labels1 = get_numpy_from_json(json_data1, patch_len, leads_names)
    meta_label1 = np.full(labels1.shape, 0)

    json_data2 = select_and_load_json()
    numpy_data2, labels2 = get_numpy_from_json(json_data2, patch_len, leads_names)
    meta_label2 = np.full(labels2.shape, 1)

    numpy_data = np.concatenate((numpy_data1, numpy_data2))
    shift_labels = np.concatenate((labels1, labels2))
    meta_labels = np.concatenate((meta_label1, meta_label2))

    numpy_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".np"
    label_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".labels_shifts"
    meta_labels_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".labels_meta"

    np_to_json(numpy_data, numpy_path)
    np_to_json(shift_labels, label_path)
    np_to_json(meta_labels ,meta_labels_path )
    print("np dataset saved to " + str(numpy_path))
    print("shape: " + str(numpy_data.shape))

def experiment(patch_len, dispersion):
    leads_names = ['i']
    from settings import PATH_TO_METADATASETS_FOLDER
    name = str(patch_len) + "_t_i_normal_cs_stdepr" + str(int(dispersion))

    path1 = PATH_TO_METADATASETS_FOLDER +"\\7_pacients_ideally_healthy_and_normal_axis.json"
    json_data1 = select_and_load_json(path1)
    numpy_data1, labels1 = get_numpy_from_json(json_data1, patch_len, leads_names)
    meta_label1 = np.full(labels1.shape, 0)

    path2 = PATH_TO_METADATASETS_FOLDER + "\\st_depression6.json"
    json_data2 = select_and_load_json(path2)
    numpy_data2, labels2 = get_numpy_from_json(json_data2, patch_len, leads_names)
    meta_label2 = np.full(labels2.shape, 1)

    numpy_data = np.concatenate((numpy_data1, numpy_data2))
    shift_labels = np.concatenate((labels1, labels2))
    meta_labels = np.concatenate((meta_label1, meta_label2))

    numpy_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".np"
    label_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".labels_shifts"
    meta_labels_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".labels_meta"

    np_to_json(numpy_data, numpy_path)
    np_to_json(shift_labels, label_path)
    np_to_json(meta_labels, meta_labels_path)
    print("np dataset saved to " + str(numpy_path))
    print("shape: " + str(numpy_data.shape))

if __name__ == "__main__":
    experiment(100, 0.0)
