"""Take snapshots of a model's internal numbers (activations)."""

import numpy as np
import torch
from tqdm.auto import tqdm

from .model import get_backbone, get_layers

READOUT_PREFIX = 'Description: '
READOUT_SUFFIX = '\nThe bodily sensation is'


def measurement_prompt(text, prefix=READOUT_PREFIX, suffix=READOUT_SUFFIX):
    """Wrap a sentence in the fixed template we measure at."""
    return prefix + text.strip() + suffix


@torch.inference_mode()
def extract_one(model, tokenizer, text, prompt_fn=measurement_prompt, reduce='last'):
    """Snapshot one sentence at every layer.

    Returns a NumPy array of shape (n_layers, hidden_size).
    reduce='last' keeps the final token (what the lab uses);
    reduce='mean' averages over all tokens (an option for your own investigations).
    """
    layers = get_layers(model)
    collected = [None] * len(layers)
    handles = []

    def observer(index):
        def hook(module, inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output  # shape (batch, tokens, hidden)
            if reduce == 'last':
                vector = hidden[0, -1, :]
            elif reduce == 'mean':
                vector = hidden[0].mean(dim=0)
            else:
                raise ValueError("reduce must be 'last' or 'mean'")
            collected[index] = vector.detach().float().cpu().numpy().copy()
        return hook

    try:
        for index, block in enumerate(layers):
            handles.append(block.register_forward_hook(observer(index)))
        device = next(model.parameters()).device
        inputs = tokenizer(prompt_fn(text), return_tensors='pt').to(device)
        get_backbone(model)(**inputs, use_cache=False)
    finally:
        for handle in handles:
            handle.remove()

    result = np.stack(collected)
    assert np.isfinite(result).all(), 'Snapshot contains inf/NaN values. Check the model precision (dtype).'
    return result


def collect(model, tokenizer, texts, description='Snapshots', **kwargs):
    """Snapshot many sentences. Returns shape (n_sentences, n_layers, hidden_size)."""
    return np.stack([extract_one(model, tokenizer, text, **kwargs) for text in tqdm(list(texts), desc=description)])
