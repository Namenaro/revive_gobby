

def get_ecgs_by_query(json_data, query):
    ecgs_ids = []
    for case_id in json_data.keys():
        print(case_id)
        if query.is_query_ok(json_data[case_id]):
            ecgs_ids.append(case_id)
    return ecgs_ids

def save_new_dataset_by_ids(old_json, ecg_ids_to_save, name_new_dataset):
    """
    Saves json only with selected (by id) patients.
    :param old_json: initail dataset dict
    :param ecg_ids_to_save: which patient we want to keep for new dataset
    :param name_new_dataset: name of file, string, ends with .json
    :return:
    """
    import json
    from settings import PATH_TO_DATASETS_FOLDER
    new_json_data = {}
    for ecg_id in old_json.keys():
        if ecg_id in ecg_ids_to_save:
            new_json_data[ecg_id]= old_json[ecg_id]
    result_file_path = PATH_TO_DATASETS_FOLDER + "\\" + name_new_dataset
    with open(result_file_path, 'w') as outfile:
        json.dump(new_json_data, outfile)




