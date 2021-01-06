from GAN_wizard.utils import to_categorical


import torch
import numpy as np
from torch.autograd import Variable

def sample_input_for_generator(generator, batch_size):
    cuda = True if torch.cuda.is_available() else False
    FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
    LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor

    z = np.random.normal(0, 1, (batch_size, generator.latent_dim))

    label_input_int = np.random.randint(0, generator.n_classes, batch_size)
    label_input_one_hot = to_categorical(label_input_int, num_columns=generator.n_classes)

    code_input = np.random.uniform(-1, 1, (batch_size, generator.code_dim))

    label_input_one_hot = Variable(FloatTensor(label_input_one_hot))
    code_input = Variable(FloatTensor(code_input))
    z = Variable(FloatTensor(z))
    label_input_int = Variable(LongTensor(label_input_int), requires_grad=False)
    return z, label_input_one_hot, code_input, label_input_int