from settings import LEADS

import numpy as np
import json
import codecs
import easygui

def get_lead_signal(ecg, lead_name):
    return ecg['Leads'][lead_name]['Signal']

def np_to_json(np_arr, file_path):
    b = np_arr.tolist()
    json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'),
              separators=(',', ':'), sort_keys=True, indent=4)

def load_np_from_json(file_path=None):
    if file_path is None:
        file_path = easygui.fileopenbox("select file with numpy dataset")
    obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    a_new = np.array(b_new)
    return a_new

def one_patient_to_np(num_leads, patient_json_node):
    leads_names = LEADS[: num_leads]
    res = []
    for lead_name in leads_names:
        lead_signal = get_lead_signal(patient_json_node, lead_name)
        res.append(lead_signal)
    return np.arrray(res)

