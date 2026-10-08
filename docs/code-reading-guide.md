# Code-reading guide: how not to get lost

Machine-learning code is rarely hard one line at a time. People get lost because they lose track of **what kind of thing** each variable is and **what shape** it has. This guide collects the habits the lab teaches, so you can use them on any notebook, not just this one.

## The habit: Run → Look → Explain

1. **Run** one line or one small cell.
2. **Look** at what came back. In this lab, `look(x, 'name', dims=(...))` prints the type, the shape with each dimension named, the number type, and a peek. Outside the lab, `type(x)`, `x.shape`, `x.dtype`, `len(x)` and `x[:5]` do the same job.
3. **Explain** it in one sentence before moving on: *"`val_scores` is a NumPy array: 12 sentences × 28 layers of scores."* If you can't say the sentence, stop and look again.

## Five questions for any code cell

| # | Question | Where to find the answer |
|---|---|---|
| 1 | What goes in? | the arguments in the brackets; the variables used |
| 2 | What comes out, and what type is it? | `look(result)` or `type(result)` |
| 3 | What shape, and what does each dimension mean? | `result.shape`; name each number out loud |
| 4 | Why this data structure? | the 🧱 notes in the notebooks; the cheat sheet below |
| 5 | Which settings were chosen, and what would change if one changed? | parameters with `=`; the 🎛️ notes; then try it (🛠️) |

## Data-structure cheat sheet

| Structure | Looks like | Good at | In this lab | Get a part of it |
|---|---|---|---|---|
| `list` | `[a, b, c]` | holding anything in order; growing one item at a time | sentences; results collected in a loop | `x[0]`, `x[-1]`, `x[:3]` |
| `tuple` | `(a, b)` | a fixed group that shouldn't change | `hidden_states`; functions returning two things (`tokenizer, model = ...`) | `x[0]`; unpack with `a, b = x` |
| `dict` | `{'key': value}` | looking things up by name | settings; `state` bundles of results | `x['key']`, `x.keys()` |
| NumPy `ndarray` | `array([[...]])` | fast maths on a grid of same-type numbers | snapshots `(sentences, layers, numbers)`; scores | `x[0]`, `x[:, 9, :]`, `x[mask]` |
| PyTorch `Tensor` | `tensor([...])` | the same, but can live on a GPU; the model's own format | token IDs, logits, hidden states, the nudge vector | same as NumPy; `.item()` for a single number |
| pandas `DataFrame` | a table | named columns that humans read | sentences + labels; results tables | `df['col']`, `df.head()`, `df[df['split'] == 'test']` |
| pandas `Series` | one column | a column with an index | counts from `groupby(...).size()` | `s['label']`, `s.unstack()` |
| `BatchEncoding` | dict of tensors | the tokenizer's output | `input_ids`, `attention_mask` | `enc['input_ids']`; pass to the model with `**enc` |
| model output | dict-like object | the model's output bundle | `.logits`, `.hidden_states` | `out.logits` |
| sparse matrix | mostly zeros | storing only non-zero entries | the word-counter's word counts | `.shape`, `.nnz`, `.toarray()` (small ones only) |

**Rule of thumb:** text lives in lists and DataFrames; numbers *the model* makes are tensors; numbers *we* analyse are NumPy arrays. The bridge from tensor to array is `t.detach().float().cpu().numpy()`, and from array to tensor is `torch.tensor(a, device=DEVICE)`.

## The shapes you'll meet in this lab

For the default model (28 layers, 1,536 numbers per token, a vocabulary of 151,936):

| Variable | Shape | In words |
|---|---|---|
| `enc['input_ids']` | `(1, T)` | 1 text × T tokens |
| `outputs.logits` | `(1, T, 151936)` | 1 text × T positions × one score per vocabulary entry |
| `outputs.hidden_states` | tuple of 29 × `(1, T, 1536)` | embedding + 28 layers, each: text × position × numbers |
| one snapshot (`extract_one`) | `(28, 1536)` | layers × numbers, for the last token |
| `train_act` | `(32, 28, 1536)` | sentences × layers × numbers |
| `raw_vectors`, `unit_vectors`, `midpoints` | `(28, 1536)` | one per layer |
| `vector_lengths` | `(28,)` | one length per layer |
| `scores_at_all_layers(...)` | `(n, 28)` | sentences × layers |
| `test_scores` | `(16,)` | one score per test sentence at the frozen layer |
| random control scores | `(16, 200)` | test sentences × fake rulers |

## Shape rules worth memorising

- **A single number in an index removes that dimension:** `x[0]` on `(32, 28, 1536)` gives `(28, 1536)`.
- **A colon keeps it:** `x[:, 9, :]` gives `(32, 1536)`.
- **`-1` means "the last one":** `hidden[0, -1, :]` is the last token.
- **`.mean(axis=k)` (NumPy) or `dim=k` (PyTorch) squashes dimension `k`.** `axis=-1` is the last dimension.
- **A True/False mask picks rows:** `x[labels == 1]`.
- **`None` adds a dimension of size 1:** `lengths[:, None]` turns `(28,)` into `(28, 1)`; `snapshot[None]` turns one item into a batch of one.
- **Broadcasting lines shapes up from the right.** Sizes must be equal, or one of them must be 1. `(28, 1536) / (28, 1)` works; `(28, 1536) / (28,)` doesn't.
- **Matrix multiplication `@` needs the inner sizes to match:** `(16, 1536) @ (1536, 200)` → `(16, 200)`.

## Reading a function you didn't write

1. Read the `def` line. What are the parameters? Which have **default values**? Defaults are choices someone made, and overriding them is how you experiment.
2. Read the docstring (the text in triple quotes). What does it promise to return?
3. Find every `return`. What type and shape does each one hand back?
4. Call the function on one small input and `look()` at the result.
5. In this lab, `show_source(fn)` prints any helper with line numbers.

## PyTorch and NumPy idioms decoded

| Code | Meaning |
|---|---|
| `with torch.inference_mode():` / `@torch.inference_mode()` | we're only using the model, not training it: skip training bookkeeping |
| `model.eval()` | "use" mode: switches off training-only behaviour |
| `.to(DEVICE)` | move to the GPU (or CPU); the model and its inputs must be on the same device |
| `.detach()` | stop tracking for training |
| `.cpu()` | move to main memory, so NumPy can read it |
| `.numpy()` | tensor → NumPy array |
| `.item()` | one-number tensor → plain Python number |
| `.tolist()` | tensor or array → Python list |
| `.clone()` / `.copy()` | an independent copy, safe to edit |
| `**enc` | unpack a dictionary into named arguments |
| `a, b = f()` | unpack two returned values |
| `[f(x) for x in items]` | list comprehension: a compact loop that builds a list |
| `try: ... finally: ...` | the `finally` part always runs, even after an error; used to remove hooks |
| `with something():` | a context manager: set up, run your block, then always clean up |

## When you hit an error

1. Read the **last line** first. That's the actual message.
2. Find the line in your code that the message points to (look for the arrow `---->`).
3. Run `look()` on every variable in that line.
4. For shape errors, write the shapes side by side and ask which dimensions should match.
5. `NameError: ... is not defined` almost always means a cell was skipped or the session restarted. Run the notebook from the top, in order.
