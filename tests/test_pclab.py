"""Fast checks of the helper library."""
import numpy as np
import pandas as pd
import pytest
import torch

import pclab


@pytest.fixture(scope='module')
def lab():
    tokenizer, model = pclab.load_model()
    return tokenizer, model


def test_data_is_balanced_and_paired():
    df = pclab.load_sentences()
    assert len(df) == 60 and df['text'].is_unique
    counts = df.groupby(['split', 'category']).size().unstack()
    assert (counts['Comfort'] == counts['Pain']).all()
    assert set(df['split']) == {'build', 'validation', 'test'}
    # Each pair: one comfort, one pain, same split
    for _, pair in df.groupby('pair_id'):
        assert sorted(pair['label']) == [0, 1] and pair['split'].nunique() == 1
    assert len(pclab.load_neutral()) == 6
    assert len(pclab.load_challenge()) == 8


def test_fit_directions_on_toy_data():
    acts = np.array([[[3.0, 2.5]], [[1.0, 1.0]], [[3.4, 2.8]], [[1.4, 1.2]]])  # (4 sentences, 1 layer, 2 numbers)
    labels = np.array([1, 0, 1, 0])
    raw, unit, mid, lengths = pclab.fit_directions(acts, labels)
    assert raw.shape == unit.shape == mid.shape == (1, 2)
    assert np.allclose(np.linalg.norm(unit, axis=-1), 1)
    scores = pclab.scores_at_all_layers(acts, unit, mid)
    assert scores.shape == (4, 1)
    assert (scores[labels == 1] > 0).all() and (scores[labels == 0] < 0).all()


def test_layer_choice_and_interval():
    table = pd.DataFrame({'layer': [1, 2, 3], 'accuracy': [0.5, 0.9, 0.9], 'auc': [0.5, 0.8, 0.95]})
    assert pclab.choose_layer(table) == 2  # 0-based index of layer 3
    lo, hi = pclab.wilson_interval(16, 16)
    assert 0.75 < lo < 1 and hi == pytest.approx(1.0)


def test_extract_shapes(lab):
    tokenizer, model = lab
    n_layers, hidden = len(pclab.get_layers(model)), model.config.hidden_size
    one = pclab.extract_one(model, tokenizer, 'The tea warmed her throat.')
    assert one.shape == (n_layers, hidden)
    mean = pclab.extract_one(model, tokenizer, 'The tea warmed her throat.', reduce='mean')
    assert mean.shape == (n_layers, hidden) and not np.allclose(one, mean)
    many = pclab.collect(model, tokenizer, ['a b', 'c d', 'e f'])
    assert many.shape == (3, n_layers, hidden)


def test_hooks_are_always_removed(lab):
    tokenizer, model = lab
    layer = pclab.get_layers(model)[0]
    before = len(layer._forward_hooks)
    pclab.extract_one(model, tokenizer, 'The tea warmed her throat.')
    vector = torch.ones(model.config.hidden_size)
    with pclab.steering(model, 0, 1.0, vector):
        assert len(layer._forward_hooks) == before + 1
    assert len(layer._forward_hooks) == before
    with pytest.raises(RuntimeError):
        with pclab.steering(model, 0, 1.0, vector):
            raise RuntimeError('boom')
    assert len(layer._forward_hooks) == before


def test_steering_changes_logits_and_zero_does_not(lab):
    tokenizer, model = lab
    enc = tokenizer('The warm bath felt', return_tensors='pt')
    vector = torch.randn(model.config.hidden_size)
    with torch.inference_mode():
        base = model(**enc, use_cache=False).logits[0, -1]
        with pclab.steering(model, 0, 0.0, vector):
            zero = model(**enc, use_cache=False).logits[0, -1]
        with pclab.steering(model, 0, 5.0, vector):
            pushed = model(**enc, use_cache=False).logits[0, -1]
    assert torch.equal(base, zero)
    assert not torch.allclose(base, pushed)


def test_generation_and_scoring_run(lab):
    tokenizer, model = lab
    text = pclab.generate_continuation(model, tokenizer, 'The warm bath felt', 0, max_new_tokens=3)
    assert isinstance(text, str)
    lp = pclab.candidate_mean_log_probability(model, tokenizer, 'The warm bath felt', ' comfortable.')
    assert np.isfinite(lp) and lp < 0


def test_look_handles_everything(capsys, lab):
    tokenizer, model = lab
    enc = tokenizer('hi', return_tensors='pt')
    for obj in [1, 2.5, None, 'text', [1, 'a'], (1, 2), {'a': 1}, np.zeros((2, 3)), torch.zeros(2),
                pd.DataFrame({'a': [1]}), pd.Series([1, 2]), enc, model, tokenizer, model(**enc, use_cache=False)]:
        pclab.look(obj, 'x')
    pclab.look(np.zeros((2, 3)), 'x', dims=('rows', 'cols'))
    assert '2 rows × 3 cols' in capsys.readouterr().out
