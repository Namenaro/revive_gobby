import numpy as np
import json
import codecs


def np_to_json(np_arr, file_path):
    b = np_arr.tolist()
    json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'),
              separators=(',', ':'), sort_keys=True, indent=4)

def load_np_from_json(file_path):
    obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    a_new = np.array(b_new)
    return a_new
