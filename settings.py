import json

#paths to initial datasets' jsons, without baseline wonder
PATH_TO_TRAIN_200_DELIN = "C:\\!mywork\\datasets\\BWR_ecg_200_delineation\\ecg_data_200.json"
PATH_TO_TEST_DATASETS_NO_DELIN = "C:\\!mywork\\datasets\\BWR_data_schiller\\"

LEADS = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
PATH_TO_METADATASETS_FOLDER = "C:\\mywork\\revive_gobby\\dataset_instanses"
PATH_TO_NUMPY_DATA_FOLDER = "C:\\mywork\\revive_gobby\\np_dataset_instanses"
PATH_TO_MODELS = "C:\\mywork\\revive_gobby\\models_instanses"
PATH_TO_SELECTORS = "C:\\mywork\\revive_gobby\\selectors_instances\\"
PATH_TO_SAMPLES_FROM_MODELS = "C:\\mywork\\revive_gobby\\model_samples_instances\\"

def load_json_dset_with_delin():
    """
    Load dataset with ECGS from json file, located at your computer.
    :return: dictionary, extracted from json file with ECGs.
    """
    path_to_json = PATH_TO_TRAIN_200_DELIN
    with open(path_to_json, 'r') as f:
        data = json.load(f)
        return data
    print("No delineation dataset was found at path: " + path_to_json)
    return NULL

def load_test_ECGs_no_delin(part_id=0):
    """
    :param part_id: vary btw 0 and 20
    :return: dictionary, extracted from json file with ECGs
    """
    part_path = PATH_TO_TEST_DATASETS_NO_DELIN + "data_part_" + str(part_id) + ".json"
    with open(part_path, 'r') as f:
        data = json.load(f)
        return data
    print("No test dataset was found at path: " + part_path)
    return NULL