from GAN_wizard.save_restore_model import restore_model_from_file
from GAN_wizard.sample_input_for_gen import sample_input_for_generator
from np_datasets_wizard.show_np_dataset import show_np_dataset_1st_lead
from np_datasets_wizard.utils import np_to_json
from settings import PATH_TO_NUMPY_DATA_FOLDER


def show_and_save_output(batch_size, name, gen_model=None):
    if gen_model is None:
        gen_model = restore_model_from_file()
    z, label_input_one_hot, code_input, label_input_int\
        = sample_input_for_generator(gen_model, batch_size)
    gen_model.cuda()
    out = gen_model(z, label_input_one_hot, code_input)
    np_out = out.cpu().detach().numpy()
    show_np_dataset_1st_lead(np_out)
    #---------save it as dataset------
    file_path = PATH_TO_NUMPY_DATA_FOLDER + "\\" + name + ".json"
    np_to_json(np_out, file_path)
    print("np dataset saved to " + str(file_path))



if __name__ == "__main__":
    show_and_save_output(15, "noise256")

