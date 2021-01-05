import easygui

def select_and_load_np_data():
    file_path = easygui.fileopenbox("Select json with numpy data")
    with open(file_path, 'r') as f:
        return json.load(f)



def show_np_dataset():
