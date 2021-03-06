from GAN_wizard.save_restore_model import restore_model_from_file
from GAN_wizard.utils import feed_np_batch_to_discriminator
from np_datasets_wizard.show_np_dataset import select_and_load_np_data

import numpy as np
import matplotlib.pyplot as plt

def make_cuttings_one_signal(patch_len, np_signal):
    half_patch_len = int(patch_len/2)
    padding = half_patch_len + 2
    start_point = padding
    signal_len = np_signal.shape[1]
    end_point = signal_len - padding

    coords_iterator = range(start_point, end_point)
    all_patches = []
    for patch_center in coords_iterator:
        patch_start = patch_center - half_patch_len
        patch_end = patch_start + patch_len
        one_patch = np_signal[:, patch_start:patch_end]
        all_patches.append(one_patch)

    return np.array(all_patches), start_point, end_point


def draw(validity, label, latent_code, ecg_signal):
    plt.subplot(3, 1, 1)
    plt.plot(validity, '-', lw=2)
    plt.title("Validity")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(ecg_signal[0,:], '-', lw=2)
    plt.title('ECG')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    print ("label_shape:" + str(label.shape))
    plt.plot(label[:, 0], '-', lw=2)
    plt.title('babel_code_0')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def make_visualisation(discr_model=None):
    if discr_model is None:
        discr_model = restore_model_from_file()
    patch_len = discr_model.patch_len
    np_data = select_and_load_np_data()
    for np_signal in np_data:
        print("one signal shape = "+ str(np_signal.shape))
        numpy_batch, start_point, end_point = make_cuttings_one_signal(patch_len, np_signal)
        print(numpy_batch.shape)
        validity, label, latent_code = feed_np_batch_to_discriminator(discr_model, numpy_batch)
        draw(validity, label, latent_code, np_signal[:, start_point:end_point])


if __name__ == "__main__":
    make_visualisation()
