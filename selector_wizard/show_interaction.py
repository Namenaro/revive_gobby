from selector_wizard.utils import cut_from_signal, get_dataset_for_selector, restore_selector_from_file
from GAN_wizard.save_restore_model import restore_model_from_file
from GAN_wizard.utils import feed_np_batch_to_discriminator
from np_datasets_wizard.utils import one_patient_to_np

import numpy as np

def get_all_signal_patches_for_every_u(u_list, model, selector, json_data):
    num_leads = model.num_leads
    patch_len = model.patch_len

    signals_indexed_by_u = []
    for _ in u_list:
        signals_indexed_by_u.append([])

    for id in selector.keys():
        if id == "dataset": continue
        json_node = json_data[id]
        np_signal = one_patient_to_np(num_leads, json_node)

        for coord in selector[id].keys():
            for i in range(len(u_list)):  # i is common index for u_list and signals_indexed_by_u
                center_point = coord + u_list[i]
                cutted_patch = cut_from_signal(np_signal, patch_len, center_point)
                if cutted_patch is None:
                    pass
                else:
                    signals_indexed_by_u[i].append(cutted_patch)
    return signals_indexed_by_u

def print_summary(signals_indexed_by_u, u_list):
    print ("Shifts and sizes of sample (for the shift):")
    for i in range(len(signals_indexed_by_u)):
        print(str(u_list[i]) + " -> " + str(len(signals_indexed_by_u[i])))

def show_sample_by_u(u_list, validity_indexed_by_u):
    """ On X-axis are values from u_list """



def get_model_reaction_for_every_u(signals_indexed_by_u, model):
    num_of_shifts = len(signals_indexed_by_u)

    validity_indexed_by_u = []
    for _ in range(num_of_shifts):
        validity_indexed_by_u.append([])

    for u_index in range(num_of_shifts):
        numpy_batch_for_shift = np.array(signals_indexed_by_u[u_index])
        if len(numpy_batch_for_shift) < 1:
            continue
        else:
            # TODO may be to threshold validity
            validity, _, _= feed_np_batch_to_discriminator(model, numpy_batch_for_shift)
            validity_indexed_by_u[u_index] = validity
    return validity_indexed_by_u[u_index]


def show_interaction_selec_u_dev(u_list, selector=None, model=None):
    if selector is None:
        selector = restore_selector_from_file()
    json_data = get_dataset_for_selector(selector)
    if model is None:
        model = restore_model_from_file()
    signals_indexed_by_u = get_all_signal_patches_for_every_u(u_list, model, selector, json_data)
    print_summary(signals_indexed_by_u, u_list)
    validity_indexed_by_u = get_model_reaction_for_every_u(signals_indexed_by_u, model)
    show_sample_by_u(u_list, validity_indexed_by_u)

