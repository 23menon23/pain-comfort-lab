"""A tiny, randomly initialised model for automated tests (no download needed).

It has the same *shape of code* as the real model, so every cell runs,
but its numbers are random: never interpret results from it.
"""

import torch

_CACHE = {}


def _corpus():
    from .data import load_challenge, load_neutral, load_sentences
    texts = load_sentences()['text'].tolist() + load_neutral() + load_challenge()['text'].tolist()
    extra = ['Description: The bodily sensation is comfortable painful uncomfortable warm stove hot bath felt',
             'Jamie sat down and noticed the surface against their skin. Alex stepped into the water.',
             'Morgan rested a hand Taylor placed a foot Casey leaned Jordan held the cloth sensation']
    return texts + extra


def tiny_test_model(n_layers=6, hidden_size=64):
    if 'pair' in _CACHE:
        return _CACHE['pair']
    from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers
    from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM

    backend = Tokenizer(models.BPE())
    backend.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    backend.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=600, special_tokens=['<|endoftext|>'],
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    backend.train_from_iterator(_corpus(), trainer)
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, eos_token='<|endoftext|>',
                                        pad_token='<|endoftext|>')
    torch.manual_seed(0)
    config = Qwen2Config(vocab_size=len(tokenizer), hidden_size=hidden_size, intermediate_size=hidden_size * 2,
                         num_hidden_layers=n_layers, num_attention_heads=4, num_key_value_heads=2,
                         max_position_embeddings=512, eos_token_id=tokenizer.eos_token_id,
                         pad_token_id=tokenizer.eos_token_id, tie_word_embeddings=True)
    model = Qwen2ForCausalLM(config).eval()
    model.config._name_or_path = 'tiny-random-qwen2 (TEST ONLY)'
    _CACHE['pair'] = (tokenizer, model)
    return tokenizer, model
