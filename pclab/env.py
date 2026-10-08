"""Environment checks used by the first cell of every notebook."""

import random
import sys

import numpy as np


def in_colab():
    return 'google.colab' in sys.modules


def set_seed(seed=42):
    """Fix random choices so the same code gives the same result each run."""
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    return seed


def device_report():
    import torch
    import transformers
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('PyTorch', torch.__version__, '| Transformers', transformers.__version__)
    if device == 'cuda':
        print('GPU:', torch.cuda.get_device_name(0))
    else:
        print('No GPU found: the model will run, but slowly. In Colab choose Runtime → Change runtime type → T4 GPU.')
    return device


def enable_widgets():
    """Colab needs one extra switch for interactive widgets; plain Jupyter does not."""
    try:
        from google.colab import output
        output.enable_custom_widget_manager()
    except ImportError:
        pass
