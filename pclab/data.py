"""Load the lab's sentence sets from the CSV files in the data/ folder.

Why CSV files? Keeping the sentences outside the code means you can read,
edit, cite and reuse them without touching any Python.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def load_sentences(path=None):
    """All labeled sentences: one row per sentence.

    Columns: split (build / validation / test), pair_id, label (1 = Comfort,
    0 = Pain), category, text.
    """
    df = pd.read_csv(path or DATA_DIR / 'sentences.csv')
    assert df['text'].is_unique, 'Duplicate sentences found: inspect the dataset.'
    return df


def split(df, name):
    """Rows for one split ('build', 'validation' or 'test'), renumbered from 0."""
    return df[df['split'] == name].reset_index(drop=True)


def load_neutral(path=None):
    """Sentences with no pain or comfort content."""
    return pd.read_csv(path or DATA_DIR / 'neutral.csv')['text'].tolist()


def load_challenge(path=None):
    """Mixed, metaphorical and negated sentences, with notes on what makes each tricky."""
    return pd.read_csv(path or DATA_DIR / 'challenge.csv')
