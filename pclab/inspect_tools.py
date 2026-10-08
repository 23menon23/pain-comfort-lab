"""Tools for answering "what did that line of code just give me?"

Two helpers live here:

* ``look(obj)`` prints a plain-language description of any object: what kind
  of thing it is, its shape, its number type, and a small peek at its values.
* ``show_source(fn)`` prints the code of any helper function, with line
  numbers, so nothing in this lab is a black box.
"""

import inspect
from collections.abc import Mapping

import numpy as np

try:  # torch and pandas are always present in the lab, but keep this file importable without them
    import torch
except ImportError:  # pragma: no cover
    torch = None
try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None


# One-sentence descriptions of the data structures you will meet in this lab.
TYPE_NOTES = {
    'list': 'a Python list: an ordered collection that can hold anything and can grow',
    'tuple': 'a Python tuple: an ordered collection that cannot be changed after it is made',
    'dict': 'a Python dictionary: values looked up by name (key)',
    'str': 'a piece of text',
    'int': 'a whole number',
    'float': 'a decimal number',
    'bool': 'True or False',
    'NoneType': 'None: "nothing here"',
    'numpy.ndarray': 'a NumPy array: a grid of numbers, all of the same type, built for fast math',
    'torch.Tensor': "a PyTorch tensor: like a NumPy array, but it can live on a GPU and is what the model computes with",
    'pandas.DataFrame': 'a pandas DataFrame: a table with named columns, like a spreadsheet',
    'pandas.Series': 'a pandas Series: one column of a table, with an index',
    'transformers.BatchEncoding': "the tokenizer's output: a dictionary of tensors (token IDs plus an attention mask)",
}


def _type_name(obj):
    """A short, readable name such as 'torch.Tensor' or 'list'."""
    cls = type(obj)
    module = cls.__module__.split('.')[0]
    if module == 'builtins':
        return cls.__name__
    if torch is not None and isinstance(obj, torch.Tensor):
        return 'torch.Tensor'
    if isinstance(obj, np.ndarray):
        return 'numpy.ndarray'
    if pd is not None and isinstance(obj, pd.DataFrame):
        return 'pandas.DataFrame'
    if pd is not None and isinstance(obj, pd.Series):
        return 'pandas.Series'
    return f'{module}.{cls.__name__}'


def _note_for(obj):
    name = _type_name(obj)
    if name in TYPE_NOTES:
        return TYPE_NOTES[name]
    if name.startswith('transformers.') and isinstance(obj, Mapping):
        if name.endswith('BatchEncoding'):
            return TYPE_NOTES['transformers.BatchEncoding']
        return 'a model output object: a dictionary-like container; reach its parts by name (e.g. .logits)'
    if hasattr(obj, 'convert_ids_to_tokens'):
        return 'a tokenizer: turns text into token IDs and back'
    if name.startswith('transformers.') or name.startswith('torch.'):
        return 'a model object or model part (PyTorch module)'
    return ''


def _is_array_like(obj):
    return isinstance(obj, np.ndarray) or (torch is not None and isinstance(obj, torch.Tensor))


def _shape_story(shape, dims):
    """Turn (32, 28, 1536) + ('sentence', 'layer', 'number') into words."""
    shape = tuple(int(s) for s in shape)
    if dims is None:
        return str(shape)
    if len(dims) != len(shape):
        return f'{shape}   (note: you named {len(dims)} dimensions but there are {len(shape)})'
    parts = [f'{size} {name}' for size, name in zip(shape, dims)]
    return f'{shape}  →  ' + ' × '.join(parts)


def brief(obj):
    """A one-line summary, used when describing the items inside containers."""
    if _is_array_like(obj):
        extra = f', on {obj.device}' if torch is not None and isinstance(obj, torch.Tensor) else ''
        return f'{_type_name(obj)}  shape {tuple(obj.shape)}  dtype {obj.dtype}{extra}'
    if pd is not None and isinstance(obj, pd.DataFrame):
        return f'DataFrame with {obj.shape[0]} rows × {obj.shape[1]} columns'
    if isinstance(obj, (list, tuple)):
        return f'{_type_name(obj)} of {len(obj)} items'
    if isinstance(obj, Mapping):
        return f'{_type_name(obj)} with {len(obj)} keys'
    if isinstance(obj, str):
        text = obj if len(obj) <= 60 else obj[:57] + '...'
        return f'str {text!r}'
    if isinstance(obj, (int, float, bool)) or obj is None:
        return f'{_type_name(obj)} {obj!r}'
    return _type_name(obj)


def look(obj, name=None, dims=None, peek=5):
    """Describe any object in plain language.

    Parameters
    ----------
    obj : anything
        The thing you want to understand.
    name : str, optional
        A label to print (usually the variable name).
    dims : tuple of str, optional
        Names for each dimension of an array, for example
        ('sentence', 'layer', 'number'). Printing the shape with names is the
        single best habit for not getting lost.
    peek : int
        How many values or items to show.
    """
    label = name or 'this value'
    tname = _type_name(obj)
    note = _note_for(obj)
    print(f'📦 {label}')
    print(f'   type  : {tname}' + (f'   ({note})' if note else ''))

    if _is_array_like(obj):
        print(f'   shape : {_shape_story(obj.shape, dims)}')
        print(f'   dtype : {obj.dtype}   (the kind of number stored)')
        if torch is not None and isinstance(obj, torch.Tensor):
            print(f'   device: {obj.device}   (cpu = main memory, cuda = GPU)')
            values = obj.detach().float().cpu().numpy() if obj.is_floating_point() else obj.detach().cpu().numpy()
        else:
            values = obj
        flat = np.asarray(values).ravel()
        if flat.size:
            shown = ', '.join(f'{v:.4g}' if isinstance(v, (float, np.floating)) else str(v) for v in flat[:peek])
            more = ', ...' if flat.size > peek else ''
            print(f'   peek  : [{shown}{more}]   (first {min(peek, flat.size)} of {flat.size} values, read row by row)')
            if np.issubdtype(np.asarray(flat).dtype, np.number):
                print(f'   range : min {flat.min():.4g}, max {flat.max():.4g}')
        return

    if pd is not None and isinstance(obj, pd.DataFrame):
        print(f'   shape : {obj.shape[0]} rows × {obj.shape[1]} columns')
        print(f'   columns: ' + ', '.join(f'{c} ({obj[c].dtype})' for c in obj.columns))
        print(f'   first {min(peek, len(obj))} rows:')
        with pd.option_context('display.max_colwidth', 70, 'display.width', 140):
            print('   ' + obj.head(peek).to_string().replace('\n', '\n   '))
        return

    if pd is not None and isinstance(obj, pd.Series):
        print(f'   length: {len(obj)}   dtype: {obj.dtype}')
        print('   first values: ' + ', '.join(repr(v) for v in obj.head(peek).tolist()))
        return

    if isinstance(obj, Mapping):
        keys = list(obj.keys())
        print(f'   keys  : {len(keys)} → {keys[:12]}' + (' ...' if len(keys) > 12 else ''))
        for key in keys[:12]:
            print(f'     [{key!r}] → {brief(obj[key])}')
        return

    if isinstance(obj, (list, tuple)):
        print(f'   length: {len(obj)}')
        kinds = sorted({_type_name(item) for item in obj})
        if kinds:
            print(f'   holds : {", ".join(kinds)}')
        for i, item in enumerate(obj[:peek]):
            print(f'     [{i}] → {brief(item)}')
        if len(obj) > peek:
            print(f'     ... and {len(obj) - peek} more')
        return

    if isinstance(obj, str):
        print(f'   length: {len(obj)} characters')
        print(f'   value : {obj!r}')
        return

    if isinstance(obj, (int, float, bool, np.integer, np.floating)) or obj is None:
        print(f'   value : {obj!r}')
        return

    if hasattr(obj, 'convert_ids_to_tokens') and hasattr(obj, '__len__'):
        print(f'   vocabulary: {len(obj):,} tokens')
        print(f'   end-of-text token: {getattr(obj, "eos_token", None)!r}')
        return

    if torch is not None and isinstance(obj, torch.nn.Module):
        n_params = sum(p.numel() for p in obj.parameters())
        print(f'   parameters (weights): {n_params:,}')
        children = list(obj.named_children())
        if children:
            print('   parts : ' + ', '.join(name for name, _ in children[:8]) + (' ...' if len(children) > 8 else ''))
        return

    text = repr(obj)
    print(f'   value : {text[:300]}' + (' ...' if len(text) > 300 else ''))


def show_source(fn):
    """Print the code of a function with line numbers, so you can read it."""
    lines, start = inspect.getsourcelines(fn)
    print(f'# Source of {fn.__module__}.{fn.__qualname__}\n')
    for number, line in enumerate(lines, start=1):
        print(f'{number:>3} │ {line}', end='')
