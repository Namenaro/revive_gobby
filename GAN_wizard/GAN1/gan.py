from GAN_wizard.GAN1.discr import Discriminator
from GAN_wizard.GAN1.gen import Generator
from GAN_wizard.utils import to_categorical


import torch
import numpy as np
from torch.autograd import Variable

class GAN:
    def __init__(self, latent_dim,
                 n_classes,
                 patch_len,
                 num_channels,
                 code_dim
                 ):
        self.latent_dim = latent_dim
        self.n_classes = n_classes
        self.patch_len = patch_len
        self.num_channels = num_channels
        self.code_dim = code_dim

        self.adversarial_loss = torch.nn.MSELoss()
        self.categorical_loss = torch.nn.CrossEntropyLoss()
        self.continuous_loss = torch.nn.MSELoss()

        self.generator = Generator(latent_dim=self.latent_dim,
                                   n_classes=self.n_classes,
                                   code_dim=self.code_dim,
                                   patch_len=self.patch_len,
                                   num_channels=self.num_channels)
        self.discriminator = Discriminator(n_classes=self.n_classes,
                                           code_dim=self.code_dim,
                                           patch_len=self.patch_len,
                                           num_channels=self.num_channels)

        def weights_init_normal(m):
            classname = m.__class__.__name__
            if classname.find("Conv") != -1:
                torch.nn.init.normal_(m.weight.data, 0.0, 0.02)
            elif classname.find("BatchNorm") != -1:
                torch.nn.init.normal_(m.weight.data, 1.0, 0.02)
                torch.nn.init.constant_(m.bias.data, 0.0)

        cuda = True if torch.cuda.is_available() else False
        if cuda:
            self.generator.cuda()
            self.discriminator.cuda()
            self.adversarial_loss.cuda()
            self.categorical_loss.cuda()
            self.continuous_loss.cuda()

        # Initialize weights
        self.generator.apply(weights_init_normal)
        self.discriminator.apply(weights_init_normal)

    def sample_input_for_generator(self, batch_size):
        cuda = True if torch.cuda.is_available() else False
        FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
        LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor

        z = np.random.normal(0, 1, (batch_size, self.latent_dim))

        label_input_int = np.random.randint(0, self.n_classes, batch_size)
        label_input_one_hot = to_categorical(label_input_int, num_columns=self.n_classes)

        code_input = np.random.uniform(-1, 1, (batch_size, self.code_dim))

        label_input_one_hot = Variable(FloatTensor(label_input_one_hot))
        code_input = Variable(FloatTensor(code_input))
        z = Variable(FloatTensor(z))
        label_input_int = Variable(LongTensor(label_input_int), requires_grad=False)
        return z, label_input_one_hot, code_input, label_input_int

