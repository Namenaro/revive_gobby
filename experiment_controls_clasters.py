from sample_device.tsne_ecg import scatter
from np_datasets_wizard.json_to_np_randomly import get_numpy_from_json
from np_datasets_wizard.json_to_np_by_qrs import get_numpy_from_json as get_np_by_shift
from sample_device.utils import load_json
from settings import PATH_TO_METADATASETS_FOLDER
from np_datasets_wizard.downsamplle_np_datset import downsample_dataset
import os
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
RS = 20150101


def get_contrast(patch_len, amount_of_patches):
    file_path = os.path.join(PATH_TO_METADATASETS_FOLDER, "unnormal_axis30.json")
    json_data = load_json(file_path)
    leads_names = ['i']
    results, labels= get_numpy_from_json(json_data, patch_len, leads_names, amount_of_patches)
    ecg_patches = np.squeeze(results, axis=1)
    return ecg_patches, labels

def get_control_results(patch_len, control):
    file_path = os.path.join(PATH_TO_METADATASETS_FOLDER, "7_pacients_ideally_healthy_and_normal_axis.json" )
    json_data=load_json(file_path)
    results, labels= get_np_by_shift(json_data, patch_len, ['i'], "qrs", control)
    ecg_patches = np.squeeze(results, axis=1)
    return ecg_patches, labels

def make_experiment(controls_list, patch_len, name, maxpool):
    """
    Saves clasterisation picture for every control from list.
    :param controls_list: list of integers
    :param patch_len: a number >0
    :param name: Save them into folder with name.
    :return:
    """
    os.makedirs(name, exist_ok=True)
    amount_of_patches = 250
    ecg_contrast, patient_ids_contrast = get_contrast(patch_len, amount_of_patches)
    labels_contrast =[0] * len(ecg_contrast)

    for control in controls_list:
        pic = str(control)+"_len"+ str(patch_len)+".png"
        picname = os.path.join(name , pic)
        control_results, patients_ids = get_control_results(patch_len, control)
        labels_results =[1] * len(control_results)
        labels = np.concatenate((labels_results, labels_contrast), axis=0)
        ecg_patches = np.concatenate((control_results, ecg_contrast), axis=0)
        if maxpool <2:
            pass
        else:
            ecg_patches = downsample_dataset(ecg_patches, maxpool)
        print(ecg_patches.shape)
        digits_proj = TSNE(random_state=RS).fit_transform(ecg_patches)
        scatter(digits_proj, labels)
        plt.savefig(picname)

def make_seria_of_experiments(name, patch_lens,controls_list, maxpool):
    print ("start seria...")
    for patch_len in patch_lens:
        make_experiment(controls_list, patch_len, name, maxpool)


if __name__ == "__main__":
    controls_list = [ 0, 200]
    patch_lens = [64]
    name = "TEST"
    make_seria_of_experiments(name, patch_lens, controls_list, 16)
