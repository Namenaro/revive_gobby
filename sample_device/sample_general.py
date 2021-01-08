from GAN_wizard.save_restore_model import restore_model_from_file
from GAN_wizard.utils import  feed_np_batch_to_discriminator
from selector_wizard.utils import select_and_load_json, cut_from_signal
from np_datasets_wizard.utils import one_patient_to_np
from sample_device.utils import save_sample

import random
import numpy as np

def make_measurement(model, np_batch):
    validity, label, latent_code = feed_np_batch_to_discriminator(model, np_batch)
    # TODO may be concatenate them
    measurement = latent_code
    return validity, measurement


def get_patches_from_random_places_of_dataset(json_dataset, size_of_sample, patch_len, num_leads):
    patches_from_random_places = []
    ids = json_dataset.keys()
    half = int(patch_len / 2) + 1
    for _ in range(size_of_sample):
        random_id = random.choice(list(ids))
        json_node = json_dataset[random_id]
        np_signal = one_patient_to_np(num_leads, json_node)
        ecg_len = len(np_signal[0])
        random_center = random.randint(half, ecg_len - half)
        patch = cut_from_signal(np_signal, patch_len, random_center)
        patches_from_random_places.append(patch)
    return np.array(patches_from_random_places)


def make_random_sample_of_model_reactions(name, size_of_sample, model=None, json_dataset=None):
    if json_dataset is None:
        json_dataset, _ = select_and_load_json()

    if model is None:
        model = restore_model_from_file()

    num_leads = model.num_channels
    patch_len = model.patch_len

    np_patches_from_random_places = get_patches_from_random_places_of_dataset\
        (json_dataset, size_of_sample, patch_len, num_leads)
    validity, measurement = make_measurement(model, np_patches_from_random_places)
    save_sample(validity, measurement, name)
    return validity, measurement


if __name__ == "__main__":
    make_random_sample_of_model_reactions(name="test256", size_of_sample=20, model=None, json_dataset=None)
