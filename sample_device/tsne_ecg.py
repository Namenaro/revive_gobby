import numpy as np
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import seaborn as sns

from np_datasets_wizard.utils import load_np_from_json

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
rc={"lines.linewidth": 2.5})
RS = 20150101

def scatter(x, colors):

    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40)
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')



    return f, ax, sc


def main():
    ecg_patches = load_np_from_json()
    ecg_patches = np.squeeze(ecg_patches, axis=1)

    y = np.full((len(ecg_patches), 1), 1)
    digits_proj = TSNE(random_state=RS).fit_transform(ecg_patches)
    scatter(digits_proj, y)
    plt.savefig('ecg-tsne.png', dpi=120)

main()