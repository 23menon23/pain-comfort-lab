"""Rebuild, in one call, what notebooks 02–03 built step by step.

Each notebook runs in a fresh session, so later notebooks use this to get back
to the same starting point: the same sentences, the same snapshots, the same
directions and the same validation-chosen layer.
"""

from .data import load_sentences, split
from .directions import choose_layer, fit_directions, layer_table, scores_at_all_layers
from .snapshots import collect


def rebuild_lab_state(model, tokenizer):
    """Returns a dictionary of named results. Use state.keys() to see what is inside."""
    sentences = load_sentences()
    build_df, val_df, test_df = split(sentences, 'build'), split(sentences, 'validation'), split(sentences, 'test')
    train_act = collect(model, tokenizer, build_df['text'], 'Build snapshots')
    val_act = collect(model, tokenizer, val_df['text'], 'Validation snapshots')
    y_train, y_val = build_df['label'].to_numpy(), val_df['label'].to_numpy()
    raw_vectors, unit_vectors, midpoints, vector_lengths = fit_directions(train_act, y_train)
    validation_results = layer_table(scores_at_all_layers(val_act, unit_vectors, midpoints), y_val)
    best_layer = choose_layer(validation_results)
    print(f'Catch-up complete. Validation chose layer {best_layer + 1} (Python index {best_layer}).')
    return {
        'build_df': build_df, 'val_df': val_df, 'test_df': test_df,
        'train_act': train_act, 'val_act': val_act, 'y_train': y_train, 'y_val': y_val,
        'raw_vectors': raw_vectors, 'unit_vectors': unit_vectors,
        'midpoints': midpoints, 'vector_lengths': vector_lengths,
        'validation_results': validation_results, 'best_layer': best_layer,
    }
