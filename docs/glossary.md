# Glossary

| Term | Plain meaning | Where it appears |
|---|---|---|
| **Activation** | the numbers a model computes for one particular input ("today's dish") | Step 1 onward |
| **α (alpha)** | how hard we nudge the model along the direction | Step 6 |
| **AUC** | how often a randomly chosen comfort sentence scores higher than a randomly chosen pain sentence; 0.5 = coin flip, 1.0 = always | Step 3 |
| **Axis / dim** | one dimension of an array; `axis=0` (NumPy) and `dim=0` (PyTorch) mean the first | Step 0 |
| **Baseline** | a simple method to compare against, like the word-counter | Step 5 |
| **Batch** | several inputs processed together; even one sentence is wrapped as a batch of one | Step 1 |
| **Broadcasting** | NumPy/PyTorch automatically stretching a smaller array to match a larger one | Steps 0, 3 |
| **Build set** | the sentences the ruler is built from; called `train_df` / `y_train` in code ("train" means building the ruler: the model is never trained) | Step 2 |
| **Candidate direction** | a direction whose meaning we haven't established yet: it might track sensation, sentiment words, mood, or a mix | Step 3 |
| **Cherry-picking** | showing only the results that support your idea | Steps 6, 7 |
| **Confound** | a hidden second explanation for your result | Steps 5, 7 |
| **Context manager** | something used with `with`: sets up, runs your block, always cleans up | Step 6 |
| **Control** | a comparison that tests whether something other than your idea explains the result | Step 5 |
| **Cosine similarity** | how alike two directions are: 1 = same, 0 = unrelated, −1 = opposite | Steps 2, 4 |
| **Direction** | an arrow through the model's numbers; ours points from the average pain snapshot to the average comfort snapshot | Steps 0, 3 |
| **dtype** | the kind of number stored (e.g. float32, int64, bool) | Step 0 |
| **Embedding** | the numbers a token starts with, from a lookup table, before any layer | Step 1 |
| **Frozen** | fixed before the test: the direction, midpoint and chosen layer are not changed after seeing test results | Step 3 |
| **Greedy decoding** | always picking the single most likely next token | Step 6 |
| **Hook** | a function attached to a part of the model that runs whenever that part runs; can read (or replace) its output | Steps 2, 6 |
| **Layer** | one processing stage of the model; ours has 28 | Step 1 |
| **Logits** | the model's raw scores for every possible next token; not probabilities | Step 1 |
| **Mask** | an array of True/False used to pick items | Steps 0, 3 |
| **Midpoint** | halfway between the average pain and average comfort snapshots: the ruler's zero | Step 3 |
| **Null result** | a careful experiment that found no effect, which still counts as a finding | Step 7 |
| **PCA** | a way to draw high-dimensional data in 2-D by keeping the directions of greatest variation | Step 4 |
| **Pre-registration** | writing down your prediction before running the experiment | Step 7 |
| **Probe** | a simple measuring tool applied to a model's internal numbers (our "ruler") | Step 3 |
| **Residual stream** | the running representation that each layer adds to ("the shared note") | Step 1 |
| **Ruler** | the lab's nickname for its probe: the unit direction with zero at the midpoint, onto which each snapshot casts a "shadow" | Steps 0, 3 |
| **Score** | where a snapshot's shadow lands on the ruler: positive = comfort side, negative = pain side; not a probability or an intensity | Step 3 |
| **Shape** | the size of each dimension of an array, e.g. `(32, 28, 1536)` | Step 0 onward |
| **Snapshot** | the model's numbers for the last token of a sentence, at every layer: shape (layers, numbers) | Step 2 |
| **Softmax** | turns scores into probabilities that add up to 1 | Step 1 |
| **Sparse matrix** | a matrix that stores only its non-zero entries | Step 5 |
| **Stage** | one entry of `hidden_states`: stage 0 is the embedding, stage k is the output of layer k (counting from 1) | Step 1 |
| **Steering** | nudging a model's internal numbers to change what it writes | Step 6 |
| **Teacher forcing** | scoring a fixed ending one token at a time, instead of letting the model choose | Step 6 |
| **Tensor** | PyTorch's array; can live on a GPU | Step 0 onward |
| **Test leakage** | letting the final-exam sentences influence your choices | Steps 2–4 |
| **Token** | a chunk of text (word, part of a word, punctuation) with an ID number | Step 1 |
| **Unit vector** | an arrow rescaled to length 1 | Step 3 |
| **Validation set** | sentences used to make choices (like which layer), kept separate from the test set | Step 3 |
| **Weights** | the model's learned settings ("the recipe"); never changed in this lab | Step 1 |
| **XAI** | explainable AI: the field that studies how AI systems reach their outputs | research-ideas guide |
