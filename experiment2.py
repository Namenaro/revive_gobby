
def make_selector_on_deviceA():
    from selector_wizard.make_initial_selector import process_clear_json_dataset
    process_clear_json_dataset(name="jst_first_10_selector_A", threshold=0.9,
                               json_data=None, path_to_this_json=None, model=None)


def make_dataset_for_device_B_by_shift(): #.sig и .conext
    from selector_wizard.selector_to_np import selector_to_np_dataset
    selector_to_np_dataset(u=128, patch_len=256, name="u128A_256_healthy7", num_leads=1, selector=None)

def show_some_np_data():
    from np_datasets_wizard.show_np_dataset import show_np_dataset_1st_lead
    show_np_dataset_1st_lead()


def tsne_cutted_patches():
    from sample_device.tsne_ecg import visualise
    visualise()

#make_selector_on_deviceA()
#make_dataset_for_device_B_by_shift()
#show_some_np_data()
tsne_cutted_patches()

