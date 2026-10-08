"""Build a comfort-minus-pain direction, score sentences with it, and pick a layer."""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score


def fit_directions(activations, labels):
    """One direction per layer from (n_sentences, n_layers, hidden) snapshots and 0/1 labels.

    Returns raw vectors, unit (length-1) vectors, midpoints, and vector lengths.
    """
    pos = activations[labels == 1].mean(axis=0)   # average comfort snapshot, (n_layers, hidden)
    neg = activations[labels == 0].mean(axis=0)   # average pain snapshot,    (n_layers, hidden)
    raw = pos - neg                                # the arrow from pain to comfort
    lengths = np.linalg.norm(raw, axis=-1)         # one length per layer, (n_layers,)
    unit = raw / np.maximum(lengths[:, None], 1e-8)
    midpoint = (pos + neg) / 2
    return raw, unit, midpoint, lengths


def scores_at_all_layers(activations, unit_vectors, midpoints):
    """(snapshot − midpoint) · unit direction, for every sentence and layer → (n_sentences, n_layers)."""
    return np.einsum('nld,ld->nl', activations - midpoints[None, :, :], unit_vectors)


def layer_table(scores, labels):
    """Accuracy and AUC at every layer (layers numbered from 1 for humans)."""
    n_layers = scores.shape[1]
    return pd.DataFrame({
        'layer': np.arange(1, n_layers + 1),
        'accuracy': [accuracy_score(labels, (scores[:, i] > 0).astype(int)) for i in range(n_layers)],
        'auc': [roc_auc_score(labels, scores[:, i]) for i in range(n_layers)],
    })


def choose_layer(table):
    """Highest accuracy, then highest AUC, then earliest layer. Returns a 0-based Python index."""
    ranked = table.sort_values(['accuracy', 'auc', 'layer'], ascending=[False, False, True])
    return int(ranked.iloc[0]['layer']) - 1


def wilson_interval(correct, total, z=1.96):
    """A rough 95% range for an accuracy measured on a small number of sentences."""
    p = correct / total
    denom = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denom
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return center - half, center + half
