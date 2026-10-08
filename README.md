# The Pain–Comfort Lab: Looking Inside a Language Model

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23228533.svg)](https://doi.org/10.5281/zenodo.23228533)
[![Tests](https://github.com/23menon23/pain-comfort-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/23menon23/pain-comfort-lab/actions/workflows/tests.yml)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)

**A curiosity-driven, inquiry-based lab for beginners.** When a language model reads *"The tea **burned** her throat"* and *"The tea **warmed** her throat pleasantly"*, its internal numbers differ. Is there a consistent pattern in that difference? And if we push the model's numbers along that pattern, does it start writing differently?

Students find out for themselves, using a free, openly licensed model (Qwen2.5-1.5B) in Google Colab. They take snapshots of the model's internal activations, find a "pain → comfort" direction, test it honestly against controls, nudge the model along it, and then design an investigation of their own.

> **What this lab can and can't show.** It *can* show whether a model's internal numbers contain a pattern linked to pain-versus-comfort *language*, and whether nudging that pattern changes what the model writes. It *cannot* show that the model feels anything. A spell-checker can recognize that "ouch" is a pain word without feeling pain.

## Who it's for

- **Students with some basic machine-learning knowledge** (you know what a classifier, a training/test split and accuracy are) **who haven't worked with transformers.**
- Some Python helps; you don't need PyTorch or deep-learning experience.
- No neuroscience or psychology background needed.

## Built so you don't get lost in the code

Most beginners don't get lost because any single line is hard. They get lost because, three cells later, they no longer know **what kind of thing** a variable is or **what shape** it has. Every notebook in this lab is built around one habit: **Run → Look → Explain.**

| Signpost | What it does |
|---|---|
| 📦 **What came back?** | After every important line, we stop and inspect the result with `look()`, which prints its type, its shape *with each dimension named* (`(32, 28, 1536) → 32 sentences × 28 layers × 1536 numbers`), and a peek at the values. |
| 🔍 **Code walk-through** | A line-by-line table: what each piece does and *why it's written that way*. |
| 🎛️ **Why this setting?** | The reasoning behind parameters like `return_tensors='pt'`, `dtype=float32`, `do_sample=False`, `use_cache=False`. |
| 🧱 **Why this data structure?** | Why a list, a NumPy array, a tensor, a DataFrame, a dictionary or a sparse matrix was chosen. |
| 🛠️ **Tinker** | Change one thing on purpose and predict what happens, including deliberate errors to learn from. |
| ✏️ **Predict first** | Write a guess before running. Surprises are where learning happens. |
| 🌱 **Curiosity branch** | An open question that can become a student project. |

There are no black boxes: each helper function is first written out and explained in a notebook, then reused from the small `pclab` library. Anyone can read any helper with `show_source(...)`. New to all of this? Start with **Step 0**, which teaches the habit on tiny made-up data. See also the [code-reading guide](docs/code-reading-guide.md).

## The learning path

Each step is one notebook with its own inquiry question. Click a badge to open it in Google Colab (choose **Runtime → Change runtime type → T4 GPU** for Steps 1–7).

| Step | Notebook | Inquiry question | Code ideas you'll learn to read | Time |
|---|---|---|---|---:|
| 0 | [How to read code without getting lost](notebooks/00_how_to_read_code.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/00_how_to_read_code.ipynb) | When a line runs, what exactly did it hand back? | lists, dicts, arrays, tensors, DataFrames; shapes and axes; masks; broadcasting; reading errors | 25 min |
| 1 | [Meet the model](notebooks/01_meet_the_model.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/01_meet_the_model.ipynb) | What does a model expect after *"The hot stove felt"*, and what does that look like inside? | tokenizers, `BatchEncoding`, model outputs, logits, softmax, `topk`, hidden states | 30 min |
| 2 | [Taking snapshots](notebooks/02_taking_snapshots.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/02_taking_snapshots.ipynb) | Are the model's numbers different, consistently, for pain and comfort sentences? | forward hooks, `try/finally`, `.detach().cpu().numpy()`, `np.stack`, 3-D arrays | 30 min |
| 3 | [Finding a direction](notebooks/03_finding_a_direction.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/03_finding_a_direction.ipynb) | Is there one arrow from "pain" to "comfort", and at which layer is it clearest? | mean differences, unit vectors, dot products, `einsum` (vs. a loop), accuracy vs. AUC, validation | 30 min |
| 4 | [The final exam and tricky sentences](notebooks/04_final_exam_and_tricky_sentences.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/04_final_exam_and_tricky_sentences.ipynb) | Does it work on unseen sentences? What about *"a burning desire"*? | sealed test sets, confidence intervals, confusion matrices, PCA fit/transform | 30 min |
| 5 | [Fair comparisons](notebooks/05_fair_comparisons.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/05_fair_comparisons.ipynb) | Could luck, or a simple word-counter, do as well? | permutation-style controls, matrix shapes, TF–IDF pipelines, sparse matrices | 25 min |
| 6 | [From watching to nudging](notebooks/06_steering.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/06_steering.ipynb) | If we push the model's numbers along the arrow, does its writing change? | hooks that modify outputs, context managers, `generate` settings, teacher forcing, log-probabilities | 35 min |
| 7 | [Your own investigation](notebooks/07_your_investigation.ipynb) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/23menon23/pain-comfort-lab/blob/main/notebooks/07_your_investigation.ipynb) | What do *you* want to know? | pre-registration, scaffolds for a "no giveaway words" test and a name-swap fairness check | open |

**Ways to run it:** Steps 1–6 take about three hours in total. Run them as two 90-minute classes (Steps 1–3, then 4–6, with Step 0 as pre-work), or as a series of 30-minute club meetings, one step each. The [instructor guide](docs/instructor-guide.md) has session plans.

Each inquiry step follows the same cycle: **🤔 Wonder → ✏️ Predict → Run → 📦 Look → 🧭 Explain → 🌱 Extend.**

## What's in the repository

```
pain-comfort-lab/
├── notebooks/            the eight steps (00–07), with no pre-filled outputs
├── pclab/                small, readable helper library used by the notebooks
├── data/                 the sentence sets as CSV files, plus a datasheet
│   ├── sentences.csv     30 comfort/pain pairs: 16 build, 6 validation, 8 test
│   ├── challenge.csv     8 mixed, metaphorical and negated sentences
│   ├── neutral.csv       6 sentences with no pain or comfort content
│   └── DATASHEET.md
├── docs/
│   ├── code-reading-guide.md   the Run → Look → Explain method, with a data-structure cheat sheet
│   ├── research-ideas.md       six research areas and starter projects for students
│   ├── worksheet.md            the student investigation worksheet
│   ├── instructor-guide.md     session plans, expected results, facilitation notes, rubric
│   └── glossary.md
├── tests/                automated checks: every notebook runs end to end on a tiny test model
├── CITATION.cff          how to cite this lab (GitHub shows a "Cite this repository" button)
└── .zenodo.json          metadata for the DOI on Zenodo
```

## Running it

**In Google Colab (recommended):** click a badge above. The first code cell downloads this repository's helper code and data; the next downloads the model (about 3 GB, once per session). Use a GPU runtime for Steps 1–7. Step 0 runs anywhere.

**On your own computer:**

```bash
git clone https://github.com/23menon23/pain-comfort-lab.git
cd pain-comfort-lab
pip install -r requirements.txt
jupyter lab notebooks/
```

The 1.5B model needs about 6 GB of memory in 32-bit precision. A CPU works but is slow; a GPU is much better. For a lighter run, change `MODEL_NAME` to `'Qwen/Qwen2.5-0.5B'` (results will differ, so record it as a different experiment).

## For students: turning curiosity into research

The lab answers one question, but the same tools can answer dozens more, and many have never been tested. [`docs/research-ideas.md`](docs/research-ideas.md) maps six research areas (probing, concepts and confounds, steering, trustworthy explanations, how models differ, and big questions about AI and experience), with starter projects at three levels. Step 7 gives ready-to-run scaffolds.

## Citing this lab

If you use or adapt this lab, please cite it. GitHub's **"Cite this repository"** button (from [`CITATION.cff`](CITATION.cff)) gives APA and BibTeX. Once released on Zenodo, cite the DOI above. The concept DOI always resolves to the latest version; each release also gets its own version DOI.

Please also cite the model ([Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115)) and the methods the lab builds on (see [Further reading](#further-reading)).

## Further reading

The lab's methods come from published research. These are background sources, not claims that this small classroom experiment will succeed.

- Alain & Bengio (2016), [Understanding intermediate layers using linear classifier probes](https://arxiv.org/abs/1610.01644): the idea behind our "ruler".
- Kim et al. (2018), [Testing with Concept Activation Vectors (TCAV)](https://arxiv.org/abs/1711.11279): directions for human concepts.
- Adebayo et al. (2018), [Sanity Checks for Saliency Maps](https://arxiv.org/abs/1810.03292): when convincing explanations fail.
- Hewitt & Liang (2019), [Designing and Interpreting Probes with Control Tasks](https://arxiv.org/abs/1909.03368): why probes need controls.
- Turner et al. (2023), [Steering Language Models With Activation Engineering](https://arxiv.org/abs/2308.10248): nudging models by adding directions.
- Zou et al. (2023), [Representation Engineering](https://arxiv.org/abs/2310.01405): reading and steering concepts inside models.
- Panickssery et al. (2023), [Steering Llama 2 via Contrastive Activation Addition](https://arxiv.org/abs/2312.06681): the closest method to our nudge.
- Qwen Team (2024), [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115): the model used in the lab.

## Licence

- **Text, notebooks' explanatory content and data:** [Creative Commons Attribution 4.0](LICENSE-CONTENT.md) (CC BY 4.0). Reuse and adapt freely, with credit.
- **Code** (the `pclab` library, code cells and tests): [MIT](LICENSE).
- **The model** (Qwen2.5-1.5B) is not included. It's downloaded from Hugging Face under its own [Apache 2.0 licence](https://huggingface.co/Qwen/Qwen2.5-1.5B).

## How this lab was made

Designed by Pratibha Menon (Pennsylvania Western University). The original single notebook, research question and refrences, learning goals, experimental design (paired sentences, a sealed test set, controls) and decisions about what to include are the author's.

Generative AI tools were used during development: **Claude (Anthropic)** helped draft code, revise the explanations for beginners, restructure the original single notebook into the eight-step version with code walk-throughs, review the code for errors and write automated tests. The author reviewed and edited all AI-assisted content and is responsible for its accuracy. AI tools are not authors of this lab.

**How it was checked:** every notebook is executed end to end by the automated tests on a tiny, randomly initialised model of the same architecture. This verifies the code runs (hooks, plots, controls, generation, scoring, widgets, hook clean-up, export). The author verified the scientific results with the real model; instructors should run the notebooks on a Colab GPU before class.

**For students:** you're welcome to use AI tools in your own work with this lab, following your instructor's policy. If you do, follow the same practice: **use it, disclose it, verify it, own it.**
