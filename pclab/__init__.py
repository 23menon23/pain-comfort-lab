"""pclab: small, readable helpers for the Pain–Comfort Lab.

Every function here is introduced and explained in a notebook first.
To read any of them, run:  show_source(function_name)
"""

from .catchup import rebuild_lab_state
from .data import load_challenge, load_neutral, load_sentences, split
from .directions import choose_layer, fit_directions, layer_table, scores_at_all_layers, wilson_interval
from .env import device_report, enable_widgets, in_colab, set_seed
from .inspect_tools import brief, look, show_source
from .plotting import COLORS, MARKERS, use_lab_style
from .model import DEFAULT_MODEL, get_backbone, get_layers, load_model, model_facts
from .results import save_results
from .snapshots import READOUT_SUFFIX, collect, extract_one, measurement_prompt
from .steering import candidate_mean_log_probability, generate_continuation, steering

__version__ = '1.0.0'
