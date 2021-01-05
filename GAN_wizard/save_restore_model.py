from settings import PATH_TO_MODELS

#from GAN_wizard.GAN1.gen import Generator

import os

def save_model(mymodel, filename):
    from importlib import import_module
    os.makedirs(PATH_TO_MODELS, exist_ok=True)
    path_file = PATH_TO_MODELS + "\\" + filename + ".pth"
    module_path = str(mymodel.__class__.__module__)
    class_name=str(mymodel.__class__.__name__)

    cls = getattr(import_module(module_path), class_name)
    inst = cls(latent_dim=6,
              n_classes=2,
              patch_len=256,
              num_channels=1,
              code_dim=1)
    print(inst.latent_dim)



if __name__ == "__main__":
    from GAN_wizard.GAN1.gan import GAN
    from np_datasets_wizard.torch_dataset import UnsupervisedDataset
    from GAN_wizard.train import train_gan

    n_epochs = 1
    gan = GAN(latent_dim=6,
              n_classes=2,
              patch_len=256,
              num_channels=1,
              code_dim=1)
    dataset_object = UnsupervisedDataset()
    train_gan(gan, n_epochs, dataset_object, contrast_object=None)
    save_model(gan.generator, "te")


