
def get_num_ecgs_with_feature(json_data, binary_feature_name):
    """Смотрим, у скольки пациентов датасета в разделе
    докторсокого стуктурированного диагноза (т.е. в "StructuredDiagnosisDoc")
    находится True """
    counter = 0
    for case_id in json_data.keys():
        if(json_data[case_id]["StructuredDiagnosisDoc"][binary_feature_name] is True):
            counter += 1
    return counter

def print_diagnosis_distribution(json_data):
    ecgs_ids = json_data.keys()
    first_ecg_id = next(iter(ecgs_ids ))
    binary_features_list = list(json_data[first_ecg_id]["StructuredDiagnosisDoc"].keys())
    feature_num_trues = dict()
    for binary_feature_name in binary_features_list:
        num_trues = get_num_ecgs_with_feature(json_data, binary_feature_name)
        feature_num_trues[binary_feature_name] = num_trues

    for w in sorted(feature_num_trues, key=feature_num_trues.get, reverse=True):
        print(w, feature_num_trues[w])

if __name__ == "__main__":
    from settings import load_initial_200_ECGs
    data = load_initial_200_ECGs()
    print_diagnosis_distribution(data)