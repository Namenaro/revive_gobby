#ALL about constants: names, paths, etc...


LEADS = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
PATH_TO_METADATASETS_FOLDER = "C:\\mywork\\revive_gobby\\dataset_instanses"
PATH_TO_NUMPY_DATA_FOLDER = "C:\\mywork\\revive_gobby\\np_dataset_instanses"
PATH_TO_MODELS = "C:\\mywork\\revive_gobby\\models_instanses"

def load_initial_200_ECGs():
    """
    Load dataset with ECGS from json file, located at your computer.
    :return: dictionary, extracted from json file with ECGs.
    """
    import json
    path_to_whole_json_200_data = "C:\\!mywork\\datasets\\BWR_ecg_200_delineation\\ecg_data_200.json"
    with open(path_to_whole_json_200_data, 'r') as f:
        data = json.load(f)
        return data
    print("no dataset file was found")
    return NULL

