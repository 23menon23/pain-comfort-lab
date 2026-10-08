"""Save your results so someone else (or future you) can check them."""

import json
import platform
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


def _jsonable(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def save_results(name, tables, settings=None, arrays=None, folder='results'):
    """Write tables (CSV), settings (JSON) and arrays (NPZ) to a folder, zip it, and offer a download.

    tables   : dict of {file_stem: DataFrame}
    settings : dict of things needed to repeat the experiment
    arrays   : dict of {name: NumPy array}
    """
    import sklearn
    import torch
    import transformers

    out = Path(folder) / name
    out.mkdir(parents=True, exist_ok=True)
    for stem, table in tables.items():
        pd.DataFrame(table).to_csv(out / f'{stem}.csv', index=False)
    settings = dict(settings or {})
    settings['versions'] = {
        'python': platform.python_version(), 'torch': torch.__version__,
        'transformers': transformers.__version__, 'numpy': np.__version__,
        'pandas': pd.__version__, 'sklearn': sklearn.__version__,
    }
    (out / 'settings.json').write_text(json.dumps({k: _jsonable(v) for k, v in settings.items()}, indent=2))
    if arrays:
        np.savez_compressed(out / 'arrays.npz', **arrays)
    (out / 'READ_ME.txt').write_text(
        'Pain–Comfort Lab results. Scores describe a candidate language representation.\n'
        'They are not probabilities, pain intensities, or evidence of experience.\n'
        'Python layer indices start at 0; human-readable layer numbers start at 1.\n')
    archive = Path(folder) / f'{name}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(out.iterdir()):
            z.write(path, arcname=f'{name}/{path.name}')
    print('Saved:', archive.resolve())
    try:
        from google.colab import files  # Only exists inside Google Colab.
        files.download(str(archive))
    except ImportError:
        pass
