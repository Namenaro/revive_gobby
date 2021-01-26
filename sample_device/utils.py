from settings import PATH_TO_SAMPLES_FROM_MODELS
from np_datasets_wizard.utils import np_to_json
import easygui
import json

def save_sample(np_validities, np_measuremens, name):
    path = PATH_TO_SAMPLES_FROM_MODELS + name
    val_name = path + ".valid"
    meas_name = path + ".measur"
    np_to_json(np_validities, val_name)
    np_to_json(np_measuremens, meas_name)
    print('Saved: ' + val_name + ", of shape "+ str(np_validities.shape))
    print('Saved: ' + meas_name + ", of shape "+ str(np_validities.shape))

def load_json(file_path=None):
    text = "select json"
    if file_path is None:
        file_path = easygui.fileopenbox(text)
        if file_path is None:
            return None
    with open(file_path, 'r') as f:
        return json.load(f)

