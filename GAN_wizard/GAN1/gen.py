import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim, n_classes, code_dim, patch_len, num_channels):
        super(Generator, self).__init__()

        self.latent_dim = latent_dim
        self.n_classes = n_classes
        self.code_dim = code_dim
        self.num_channels = num_channels

        input_dim = latent_dim + n_classes + code_dim

        self.init_len = patch_len // 4
        self.l1 = nn.Sequential(nn.Linear(input_dim, 128 * self.init_len))


        self.conv_block = nn.Sequential(
            # nn.BatchNorm1d(128),

            nn.Upsample(scale_factor=2),
            nn.Conv1d(128, 128, 3, stride=1, padding=1),
            # nn.BatchNorm1d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Upsample(scale_factor=2),
            nn.Conv1d(128, 64, 3, stride=1, padding=1),
            # nn.BatchNorm1d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv1d(64, num_channels, 3, stride=1, padding=1),
        )


    def forward(self, noise, labels, code):
        gen_input = torch.cat((noise, labels, code), -1)
        out = self.l1(gen_input)
        out = out.view(out.shape[0], 128, self.init_len)

        out = self.conv_block(out)
        return out
