import numpy as np
import torch
from torch.autograd import Variable

def to_categorical(y, num_columns):
    """Returns one-hot encoded Variable"""
    y_cat = np.zeros((y.shape[0], num_columns))
    y_cat[range(y.shape[0]), y] = 1.0
    return y_cat

def feed_np_batch_to_discriminator(model, numpy_batch):
    cuda = True if torch.cuda.is_available() else False
    if cuda:
        model.cuda()
    Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
    ecg_batch = Variable(Tensor(numpy_batch))
    validity, label, latent_code = model(ecg_batch)
    return validity.detach().numpy(), label.detach().numpy(), latent_code.detach().numpy()
