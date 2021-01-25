import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

from np_datasets_wizard.utils import load_np_from_json

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
rc={"lines.linewidth": 2.5})
RS = 20150101


def scatter(x, colors):
    cm = plt.cm.get_cmap('RdYlBu')
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    if colors is None:
        sc = ax.scatter(x[:, 0], x[:, 1], lw=0, s=40)
    else:
        sc = ax.scatter(x[:, 0], x[:, 1], lw=0, s=40, c=colors, cmap=cm)
        plt.colorbar(sc)
    ax.axis('off')
    ax.axis('tight')
    return f, ax, sc


def visualise():
    ecg_patches = load_np_from_json(text="select np signal data")
    ecg_patches = np.squeeze(ecg_patches, axis=1)

    labels = load_np_from_json(text="select np labels")

    digits_proj = TSNE(random_state=RS).fit_transform(ecg_patches)
    scatter(digits_proj, labels)
    plt.show()

if __name__ == "__main__":
    visualise()