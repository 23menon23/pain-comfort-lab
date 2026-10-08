"""Nudge the model along a direction while it runs, and measure what changes."""

from contextlib import contextmanager

import numpy as np
import torch

from .model import get_layers


@contextmanager
def steering(model, layer_index, strength=0.0, direction=None):
    """Inside a `with steering(...):` block, add strength × direction to the last token at one layer.

    The nudge is removed automatically when the block ends, even if an error happens.
    """
    if float(strength) == 0 or direction is None:
        yield  # No nudge: the model runs exactly as normal.
        return

    def hook(module, inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        changed = hidden.clone()  # Never edit the original in place; make a copy and edit that.
        changed[:, -1, :] += float(strength) * direction.to(hidden.device, hidden.dtype)
        if isinstance(output, tuple):
            return (changed,) + tuple(output[1:])
        return changed  # Returning a value from a forward hook REPLACES the layer's output.

    handle = get_layers(model)[layer_index].register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


@torch.inference_mode()
def generate_continuation(model, tokenizer, prompt, layer_index, strength=0.0, direction=None,
                          max_new_tokens=24):
    """Greedy continuation of `prompt`, optionally steered. Returns only the new text."""
    device = next(model.parameters()).device
    inputs = tokenizer(prompt, return_tensors='pt').to(device)
    prefix_length = inputs['input_ids'].shape[1]
    with steering(model, layer_index, strength, direction):
        generated = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_new_tokens=max_new_tokens,
            do_sample=False,          # greedy: always take the single most likely next token
            use_cache=False,          # re-run the whole text each step so the nudge is applied consistently
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(generated[0, prefix_length:], skip_special_tokens=True)


@torch.inference_mode()
def candidate_mean_log_probability(model, tokenizer, prompt, candidate, layer_index=0,
                                   strength=0.0, direction=None):
    """Average log-probability the model gives to `candidate` as the continuation of `prompt`."""
    device = next(model.parameters()).device
    prefix = tokenizer(prompt, return_tensors='pt')['input_ids'].to(device)
    candidate_ids = tokenizer.encode(candidate, add_special_tokens=False)
    assert candidate_ids, 'The candidate must contain at least one token.'
    log_probs = []
    with steering(model, layer_index, strength, direction):
        for token_id in candidate_ids:
            logits = model(input_ids=prefix, use_cache=False).logits[0, -1].float()
            log_probs.append(torch.log_softmax(logits, dim=-1)[token_id].item())
            next_id = torch.tensor([[token_id]], dtype=prefix.dtype, device=device)
            prefix = torch.cat([prefix, next_id], dim=1)
    return float(np.mean(log_probs))
