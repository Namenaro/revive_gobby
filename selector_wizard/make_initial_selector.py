from GAN_wizard.utils import feed_np_batch_to_discriminator
from GAN_wizard.save_restore_model import restore_model_from_file
from selector_wizard.utils import select_and_load_json, save_selector_to_file
from visualise_models.visualise_discr import make_cuttings_one_signal
from np_datasets_wizard.utils import one_patient_to_np
from settings import PATH_TO_SELECTORS

import numpy as np
import json



def process_one_json_node(threshold, json_node, model):
    patch_len = model.patch_len
    num_leads = model.num_channels

    points_measurements = {}
    np_signal = one_patient_to_np(num_leads, json_node)
    np_batch_cuttings, start_point, end_point = make_cuttings_one_signal(patch_len, np_signal)
    validities, measurements = make_measurement(model, np_batch_cuttings)

    for index in range(len(validities)):
        validity = validities[index]
        if validity >= threshold:
            point_in_ecg = start_point + index
            measurement_at_point = measurements[index]
            points_measurements[point_in_ecg] = measurement_at_point
    return points_measurements


def process_clear_json_dataset(name, threshold, json_data=None, path_to_this_json=None, model=None):
    selector = {}
    if json_data is None:
        json_data, path_to_this_json = select_and_load_json()
    selector["dataset"] = path_to_this_json
    if model is None:
        model = restore_model_from_file()

    for patient_id in json_data.keys():
        print ("Process patient " + str(patient_id) + "...")
        points_measures_dict = process_one_json_node(threshold, json_data[patient_id], model)
        selector[patient_id] = points_measures_dict
    save_selector_to_file(selector, name)
    return selector

if __name__ == "__main__":
    process_clear_json_dataset(name="healthy", threshold=0.5, json_data=None, path_to_this_json=None, model=None)

