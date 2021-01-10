
def create_dataset_for_device_A():
    from np_datasets_wizard.json_to_np_by_qrs import make_and_save_dataset
    make_and_save_dataset(256, "256_t_i_one_ideal", ["i"])




def create_device_A():
    from GAN_wizard.GAN1.gan import GAN
    from GAN_wizard.train import train_gan
    from GAN_wizard.save_restore_model import save_model_to_file
    from np_datasets_wizard.torch_dataset import UnsupervisedDataset

    n_epochs = 100
    gan = GAN(latent_dim=6,
              n_classes=2,
              patch_len=256,
              num_channels=1,
              code_dim=1)
    dataset_object = UnsupervisedDataset()
    train_gan(gan, n_epochs, dataset_object, contrast_object=None)
    save_model_to_file(gan.discriminator, "A_onT.discr")
    save_model_to_file(gan.generator, "A_onT.gen")

def visualise_device():
    from visualise_models.visualise_discr import make_visualisation
    make_visualisation()

def visualise_gen():
    from visualise_models.visualise_gen import show_and_save_output
    show_and_save_output(15, "qrs_generator_650_result")

def make_selector_on_deviceA():
    from selector_wizard.make_initial_selector import process_clear_json_dataset

    process_clear_json_dataset(name="jst_first_10_selector_A", threshold=0.9,
                               json_data=None, path_to_this_json=None, model=None)


def make_dataset_for_device_B_by_shift(): #.sig и .conext
    from selector_wizard.selector_to_np import selector_to_np_dataset
    selector_to_np_dataset(u=128, patch_len=256, name="u128_unnormal10_from_150ep", num_leads=1, selector=None)

def show_some_np_data():
    from np_datasets_wizard.show_np_dataset import show_np_dataset_1st_lead
    show_np_dataset_1st_lead()

def train_device_B():
    from GAN_wizard.GAN1.gan import GAN
    from GAN_wizard.train import train_gan
    from GAN_wizard.save_restore_model import save_model_to_file
    from np_datasets_wizard.torch_dataset import UnsupervisedDataset

    n_epochs = 10 # dataset in now larger!
    gan = GAN(latent_dim=6,
              n_classes=2,
              patch_len=256,
              num_channels=1,
              code_dim=1)
    dataset_object = UnsupervisedDataset()
    train_gan(gan, n_epochs, dataset_object, contrast_object=None)
    save_model_to_file(gan.discriminator, "devB_256_u128_healthy_1_ep10.discr")
    save_model_to_file(gan.generator, "devB_256_u128_healthy_1_ep10.gen")

def show_AB_interaction():
    import numpy as np
    from selector_wizard.show_interaction import show_interaction_selec_u_dev
    u_list = np.arange(20, 3000, 20).tolist()
    show_interaction_selec_u_dev(u_list=u_list, selector=None, model=None)

#create_dataset_for_device_A()
#create_device_A()
visualise_device()
#visualise_gen()
#make_selector_on_deviceA()
#make_dataset_for_device_B_by_shift()
#show_some_np_data()
#train_device_B()
#show_AB_interaction()
