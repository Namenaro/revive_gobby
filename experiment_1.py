
def create_dataset_for_device_A():
    from np_datasets_wizard.json_to_np_by_qrs import make_and_save_dataset
    make_and_save_dataset(256, "256_qrs_i_one_ideal", ["i"])

def create_device_A():
    from GAN_wizard.GAN1.gan import GAN
    from GAN_wizard.train import train_gan
    from GAN_wizard.save_restore_model import save_model_to_file
    from np_datasets_wizard.torch_dataset import UnsupervisedDataset

    n_epochs = 650
    gan = GAN(latent_dim=6,
              n_classes=2,
              patch_len=256,
              num_channels=1,
              code_dim=1)
    dataset_object = UnsupervisedDataset()
    train_gan(gan, n_epochs, dataset_object, contrast_object=None)
    save_model_to_file(gan.discriminator, "sig265_650_epoch_1d_2cl.discr")
    save_model_to_file(gan.generator, "sig265_650_epoch_1d_2cl.gen")

def visualise_device():
    from visualise_models.visualise_discr import make_visualisation
    make_visualisation()

def visualise_gen():
    from visualise_models.visualise_gen import show_and_save_output
    show_and_save_output(15, "qrs_generator_650_result")

def make_dataset_for_device_B():
    pass

#create_dataset_for_device_A()
#create_device_A()
#visualise_device()
#visualise_gen()