import argparse
import os
import numpy as np
import math
import itertools
from typing import NamedTuple

import torchvision.transforms as transforms
from torchvision.utils import save_image

from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

import torch.nn as nn
import torch.nn.functional as F
import torch


def train_gan(gan, n_epochs, dataset_object, contrast_object=None):
    cuda = True if torch.cuda.is_available() else False

    FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
    LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor

    # Optimizers
    lr = 0.0002
    b1 = 0.5
    b2 = 0.999
    optimizer_G = torch.optim.Adam(gan.generator.parameters(), lr=lr, betas=(b1, b2))
    optimizer_D = torch.optim.Adam(gan.discriminator.parameters(), lr=lr, betas=(b1, b2))
    optimizer_info = torch.optim.Adam(
        itertools.chain(gan.generator.parameters(), gan.discriminator.parameters()), lr=lr, betas=(b1, b2)
    )

    # dataloaders
    contrastloader = None
    dataloader = torch.utils.data.DataLoader(dataset_object,
                                             batch_size=10,
                                             shuffle=True
                                             )
    if contrast_object is not None:
        contrastloader = torch.utils.data.DataLoader(contrast_object,
                                                     batch_size=10,
                                                     shuffle=True
                                                     )

    ############################################################
    for epoch in range(n_epochs):
        for i, ecgs in enumerate(dataloader):
            batch_size = ecgs.shape[0]

            valid = Variable(FloatTensor(batch_size, 1).fill_(1.0), requires_grad=False)
            fake = Variable(FloatTensor(batch_size, 1).fill_(0.0), requires_grad=False)
            real_ecgs = Variable(ecgs.type(FloatTensor))

            # -----------------Train Generator-----------------
            z, label_input_one_hot, code_input, label_input_int = gan.sample_input_for_generator(batch_size)
            gen_ecgs = gan.generator(z, label_input_one_hot, code_input)
            validity, _, _ = gan.discriminator(gen_ecgs)
            g_loss = gan.adversarial_loss(validity, valid)
            g_loss.backward()
            optimizer_G.step()

            # ---------------------Train Discriminator---------------------
            optimizer_D.zero_grad()
            real_pred, _, _ = gan.discriminator(real_ecgs)
            d_real_loss = gan.adversarial_loss(real_pred, valid)

            fake_pred, _, _ = gan.discriminator(gen_ecgs.detach())
            d_fake_loss = gan.adversarial_loss(fake_pred, fake)

            #TODO here add contrast!
            d_loss = (d_real_loss + d_fake_loss) / 2
            d_loss.backward()
            optimizer_D.step()

            # ------------------Information Loss------------------
            optimizer_info.zero_grad()
            gen_ecgs = gan.generator(z, label_input_one_hot, code_input)
            _, pred_label, pred_code = gan.discriminator(gen_ecgs)
            info_loss = gan.categorical_loss(pred_label, label_input_int) + 0.1 * gan.continuous_loss(
                pred_code, code_input
            )
            info_loss.backward()
            optimizer_info.step()

            #--------------------Logs-----------------------------
            print(
                "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f] [info loss: %f]"
                % (epoch, n_epochs, i, len(dataloader), d_loss.item(), g_loss.item(), info_loss.item())
            )




