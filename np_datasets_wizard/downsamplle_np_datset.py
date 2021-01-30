from np_datasets_wizard.utils import load_np_from_json
from settings import PATH_TO_NUMPY_DATA_FOLDER
from np_datasets_wizard.utils import np_to_json


import torch
import torch.nn as nn
import easygui
import numpy as np
from torch.autograd import Variable

class Net(nn.Module):
    def __init__(self, maxpool):
        super(Net, self).__init__()
        self.down = nn.MaxPool1d(maxpool, stride=maxpool)

    def forward(self, x):
        x = self.down(x)
        return x

def select_and_load_np_data():
    file_path = easygui.fileopenbox("Select json with numpy data")
    return load_np_from_json(file_path)

def downsample_dataset(np_arr, maxpool):
    initaial_shape = len(np_arr.shape)
    if initaial_shape ==2:
        np_arr=np.expand_dims(np_arr, axis=1)
    with torch.no_grad():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = Net(maxpool).to(device)
        model.eval()

        FloatTensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
        data = (FloatTensor(np_arr)).to(device)
        output = model(data).cpu().detach().numpy()
        if initaial_shape == 2:
            output = np.squeeze(output, 1)
        return output
    return None

def downsample_and_save_np_dataset(name, np_arr=None):
    if np_arr is None:
        np_arr = select_and_load_np_data()

    downsampled_np = downsample_dataset(np_arr)
    path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".np"
    np_to_json(downsampled_np, path)

    print("np dataset saved to " + str(path))
    print("shape: " + str(downsampled_np.shape))

if __name__ == "__main__":
    name = "downsampled2"
    downsample_and_save_np_dataset(name)
