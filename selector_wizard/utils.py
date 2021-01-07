from settings import PATH_TO_SELECTORS

import easygui
import json

def select_and_load_json():
    file_path = easygui.fileopenbox("Select json with data")
    with open(file_path, 'r') as f:
        return json.load(f)

def save_selector_to_file(selector, filename):
    path = PATH_TO_SELECTORS + "\\" + filename + ".json"
    with open(path, 'w') as f:
        json.dump(selector, f)