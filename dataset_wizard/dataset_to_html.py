import matplotlib.pyplot as plt
import base64
from io import BytesIO
import torch
import numpy as np
import os

from settings import LEADS
"""
This code is intended for visualisation of the dataset:
it can draw selected json with ECGs to a html page with pictures and text.
You can select which leads and which patients to draw.
"""

def get_lead_signal(ecg, lead_name):
    return ecg['Leads'][lead_name]['Signal']


def get_ecg_description(ecg):
    return ecg["TextDiagnosisDoc"]


def plot_one_ecg_to_fig(ecg_json_node, leads_names):
    numleads = len(leads_names)
    fig, axs = plt.subplots(numleads, 1, figsize=(8, 2 * numleads), sharex=True, sharey=True)
    axs = axs.ravel()

    for i in range(numleads):
        name = leads_names[i]
        signal = get_lead_signal(ecg_json_node, name)
        axs[i].plot(signal)
        axs[i].set_title(name)
    return fig


def draw_ecgs_from_json_to_html_by_ids(json_data,
                                       ecgs_ids,
                                       name_html,
                                       folder,
                                       message="",
                                       leads_to_draw=LEADS[:2]):
    html = "<!DOCTYPE HTML><html>" + str(leads_to_draw) + "<head></head><body>"
    html += message + "<br>" \
            + "Selected ECGs are: " + str(ecgs_ids)

    os.makedirs(folder, exist_ok=True)
    for ecg_id in ecgs_ids:
        html += "<hr>"
        ecg = json_data[ecg_id]
        ECG_title = "<p>" + str(ecg_id) + "// " + get_ecg_description(ecg) + "</p>"
        html += ECG_title
        fig = plot_one_ecg_to_fig(ecg, leads_names=leads_to_draw)
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html += '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'descrition.. <br>'
        plt.close(fig)

    # Save html
    html += "</body></html>"
    filename = folder + "/" + name_html
    with open(filename, 'w') as f:
        f.write(html)


def draw_all_dataset_to_html(json_data,
                             name_html,
                             folder,
                             message="",
                             leads_to_draw=LEADS[:3]):
    ecgs_ids = json_data.keys()
    draw_ecgs_from_json_to_html_by_ids(json_data,
                                       ecgs_ids,
                                       name_html,
                                       folder,
                                       message,
                                       leads_to_draw)
if __name__ == "__main__":
    pass

