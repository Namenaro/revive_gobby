from np_datasets_wizard.utils import one_patient_to_np
from selector_wizard.utils import cut_from_signal, get_dataset_for_selector, save_np_u_selectors, restore_selector_from_file

import easygui

def selector_to_np_dataset(u, patch_len, name, num_leads, selector=None):
    if selector is None:
        selector = restore_selector_from_file()
    json_dataset = get_dataset_for_selector(selector)

    cutted_signals_batch = []
    contexts_batch = []

    for patient_id in selector:
        if patient_id == "dataset":
            continue
        json_node = json_dataset[patient_id]
        np_signal = one_patient_to_np(num_leads, json_node)
        points = selector[patient_id]
        for coord in points.keys():
            center_point_to_cut = int(coord) + u
            patch_of_signal = cut_from_signal(np_signal, patch_len, center_point_to_cut)
            if patch_of_signal is not None:
                cutted_signals_batch.append(patch_of_signal)
                old_measurement = points[coord]
                contexts_batch.append(old_measurement)

    if len(cutted_signals_batch) > 0:
        save_np_u_selectors(cutted_signals_batch, contexts_batch, name)
    else:
        print("With that u and patch_len selector results with empty numpy array, saving aborted.")


if __name__ == "__main__":
    selector_to_np_dataset(u=50, patch_len=256, name="some_test_u50", num_leads=1, selector=None)
