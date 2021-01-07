from GAN_wizard.utils import feed_np_batch_to_discriminator
from GAN_wizard.save_restore_model import restore_model_from_file
from selector_wizard.utils import select_and_load_json, save_selector_to_file
from visualise_models.visualise_discr import make_cuttings_one_signal
from np_datasets_wizard.utils import one_patient_to_np
import easygui

def make_measurement(model, np_batch):
    validity, label, latent_code = feed_np_batch_to_discriminator(model, np_batch)
    #TODO may be concatenate them
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

