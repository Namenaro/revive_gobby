from settings import PATH_TO_NUMPY_DATA_FOLDER

import easygui
import json

def get_numpy_from_json(json_data, patch_len):
    pass

def select_and_load_json():
    file_path = easygui.fileopenbox("Select json with data")
    with open(file_path, 'r') as f:
        return json.load(f)

def make_and_save_dataset(patch_len):
    json_data = select_and_load_json()
    numpy_data = get_numpy_from_json(json_data, patch_len)


if __name__ == "__main__":
    make_and_save_dataset(256)
