from torch.utils.data import Dataset, DataLoader
from np_datasets_wizard.utils import load_np_from_json

import easygui


class UnsupervisedDataset(Dataset):
    """ECG patches dataset."""

    def __init__(self, np_data=None):
        if np_data is None:
            file_path = easygui.fileopenbox("Select json with numpy data")
            self.data = load_np_from_json(file_path)
        else:
            self.data = np_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]



