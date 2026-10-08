"""Load a language model and find its layers."""

import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_MODEL = 'Qwen/Qwen2.5-1.5B'


def load_model(model_name=DEFAULT_MODEL, revision='main', dtype=torch.float32, device=None):
    """Download (first time only) and load a tokenizer and a model.

    Returns a pair: (tokenizer, model).
    """
    if os.environ.get('PCLAB_TEST_MODEL'):  # Automated tests only: a tiny random model, no download.
        from .testing import tiny_test_model
        return tiny_test_model()
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)
    model = AutoModelForCausalLM.from_pretrained(model_name, revision=revision, dtype=dtype)
    model = model.to(device)
    model.eval()  # "Use" mode: switches off training-only behaviour. Nothing is trained in this lab.
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer, model


def get_layers(model):
    """Return the list of transformer layers (blocks), whatever the model family calls them."""
    for path in ('model.layers', 'transformer.h', 'gpt_neox.layers', 'model.decoder.layers'):
        obj = model
        try:
            for attribute in path.split('.'):
                obj = getattr(obj, attribute)
            return obj
        except AttributeError:
            continue
    raise AttributeError('Could not find the layers. Run print(model) and look for a list of repeated blocks.')


def get_backbone(model):
    """The part of the model that produces hidden states (everything except the final word-scoring layer)."""
    return model.base_model


def resolved_revision(model, model_name=None, revision='main'):
    """The exact commit (version) of the model files, so others can repeat your work."""
    commit = getattr(model.config, '_commit_hash', None)  # set by older versions of Transformers
    if commit or os.environ.get('PCLAB_TEST_MODEL'):
        return commit
    try:  # newer versions: ask the Hugging Face Hub which commit 'main' currently points to
        from huggingface_hub import model_info
        return model_info(model_name or model.config._name_or_path, revision=revision).sha
    except Exception:
        return None


def model_facts(model, model_name=None, revision='main'):
    """A small dictionary of facts worth recording with any result."""
    return {
        'model': model_name or getattr(model.config, '_name_or_path', 'unknown'),
        'requested_revision': revision,
        'resolved_revision': resolved_revision(model, model_name, revision),
        'n_layers': len(get_layers(model)),
        'hidden_size': model.config.hidden_size,
        'vocab_size': model.config.vocab_size,
        'n_parameters': sum(p.numel() for p in model.parameters()),
        'dtype': str(next(model.parameters()).dtype),
        'device': str(next(model.parameters()).device),
    }
