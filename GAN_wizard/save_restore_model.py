from settings import PATH_TO_MODELS
import easygui

import os
from importlib import import_module
import torch


def save_model_to_file(mymodel, filename):
    """
    Save model to file: it's params, classname, weights
    :param mymodel: model to save, with predefined dict of params (latent_dim, ...)
    :param filename: short string, for exampe "mymodel.gen"
    :return:
    """
    os.makedirs(PATH_TO_MODELS, exist_ok=True)
    path_file = PATH_TO_MODELS + "\\" + filename

    module_path = str(mymodel.__class__.__module__)
    class_name = str(mymodel.__class__.__name__)

    torch.save({
        'model_state_dict': mymodel.state_dict(),

        'module_path': module_path,
        'class_name': class_name,

        # -- hyperparams---
        'latent_dim': mymodel.latent_dim,
        'n_classes': mymodel.n_classes,
        'patch_len': mymodel.patch_len,
        'num_channels': mymodel.num_channels,
        'code_dim': mymodel.code_dim
    }, path_file)


def restore_model_from_file(filename=None):
    if filename is None:
        filename = easygui.fileopenbox("Select file with saved model")
    checkpoint = torch.load(filename)

    module_path = checkpoint['module_path']
    class_name = checkpoint['class_name']
    myclass = getattr(import_module(module_path), class_name)

    model = myclass(latent_dim=checkpoint['latent_dim'],
                    n_classes=checkpoint['n_classes'],
                    patch_len=checkpoint['patch_len'],
                    num_channels=checkpoint['num_channels'],
                    code_dim=checkpoint['code_dim'])

    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model

if __name__ == "__main__":
    """ Example of use"""
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
    save_model_to_file(gan.generator, "256_one_epoch.gen")
    model = restore_model_from_file()
    print(model.latent_dim)
