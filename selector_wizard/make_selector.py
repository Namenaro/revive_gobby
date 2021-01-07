from GAN_wizard.utils import feed_np_batch_to_discriminator
from GAN_wizard.save_restore_model import restore_model_from_file
from selector_wizard.utils import select_and_load_json, save_selector_to_file
from visualise_models.visualise_discr import make_cuttings_one_signal
from np_datasets_wizard.utils import one_patient_to_np, np_to_json
from settings import PATH_TO_SELECTORS

import numpy as np


def make_measurement(model, np_batch):
    validity, label, latent_code = feed_np_batch_to_discriminator(model, np_batch)
    # TODO may be concatenate them
    measurement = latent_code
    return validity, measurement


def process_one_json_node(threshold, json_node, model):
    patch_len = model.patch_len
    num_leads = model.num_channels

    points_measurements = {}
    np_signal = one_patient_to_np(num_leads, json_node)
    np_batch_cuttings, start_point, end_point = make_cuttings_one_signal(patch_len, np_signal)
    validity, measurements = make_measurement(model, np_batch_cuttings)

    super_threshold_indices = validity > threshold
    for index in super_threshold_indices:
        point_in_ecg = start_point + index
        measurement_at_point = measurements[index]
        points_measurements[point_in_ecg] = measurement_at_point
    return points_measurements


def process_clear_json_dataset(name, threshold, json_data=None, model=None):
    selector = {}
    if json_data is None:
        json_data = select_and_load_json()
    if model is None:
        model = restore_model_from_file()

    for patient_id in json_data.keys():
        points_dict = process_one_json_node(threshold, json_data[patient_id], model)
        selector[patient_id] = points_dict
    save_selector_to_file(selector, name)
    return selector

def cut_from_signal(np_signal, patch_len, center_point):
    half = int(patch_len/2)
    start= center_point - half
    end = start + patch_len
    if end >= len(np_signal[0]) or start < 0:
        return None
    return np_signal[:, start:end]

def selector_to_np_dataset(u, selector, json_dataset, patch_len, name, num_leads):
    signal_patches_filename = PATH_TO_SELECTORS + name + ".sig"
    measurs_filename = PATH_TO_SELECTORS + name + ".conext"

    cutted_signals_batch = []
    contexts_batch = []

    for patient_id in selector:
        json_node =json_dataset[patient_id]
        np_signal = one_patient_to_np(num_leads, json_node)
        points = selector[patient_id]
        for coord in points.keys():
            center_point_to_cut = coord + u
            patch_of_signal = cut_from_signal(np_signal, patch_len, center_point_to_cut)
            if patch_of_signal is not None:
                cutted_signals_batch.append(patch_of_signal)
                old_measurement = points[coord]
                contexts_batch.append(old_measurement)
    np_to_json(np.array(cutted_signals_batch), signal_patches_filename)
    np_to_json(np.array(contexts_batch), measurs_filename)

