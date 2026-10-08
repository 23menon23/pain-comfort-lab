# Instructor guide

## Learning goals

By the end of the lab, students can:

1. **Read ML code without getting lost:** say the type and shape of each variable, name each dimension, and explain why a data structure or parameter was chosen.
2. **Explain** tokens, layers, activations, weights and directions in plain language.
3. **Run a fair representation experiment:** build/validation/test splits, a frozen choice, controls, and an honest report with uncertainty.
4. **Distinguish reading from intervening:** what a probe shows versus what steering shows.
5. **Reason about limits:** why "a model represents pain-related language" is not "a model feels pain".
6. **Design a small investigation** with a pre-registered prediction and a control.

## Prerequisites

Basic ML (classifier, train/test split, accuracy), some Python. No transformer, PyTorch or neuroscience background. Step 0 teaches the data-structure and shape fluency the rest of the lab relies on, so don't skip it with beginners.

## Session plans

| Format | Plan |
|---|---|
| **One 90-minute class** | Step 0 as pre-work (25 min at home). In class: Steps 1–3 (≈ 90 min). Steps 4–6 as homework or a second session. |
| **Two 90-minute classes** | Step 0 as pre-work. Class 1: Steps 1–3 (≈ 90 min). Class 2: Steps 4–6 (≈ 90 min). Step 7 as a project. |
| **Club series (30 min each)** | One step per meeting (8 meetings). Open each with the 🤔 Wonder question and ask for predictions before anyone runs code. |
| **Research onboarding** | Steps 0–6 self-paced, then a one-week Step 7 project presented at a group meeting. |

## Before class

- **Run every notebook once on a Colab GPU with the real model.** The automated tests only check that the code runs (on a tiny random model); they don't check scientific results.
- If you fork or move the repository, point the links at the new location with `python tools/set_repo_url.py <owner>/<repo>`; otherwise the Colab setup cell downloads the helpers from the original repository.
- Colab's free GPUs aren't guaranteed. Have a backup: pairs sharing one GPU session, or an instructor demo.
- The first model download takes a few minutes per session. Ask students to run the first two cells of a notebook as soon as they sit down.

## Facilitation: the inquiry cycle

Every step follows **🤔 Wonder → ✏️ Predict → Run → 📦 Look → 🧭 Explain → 🌱 Extend**.

- **Make predictions public.** Have students write a prediction on a sticky note or in the chat *before* running the cell. Surprises only teach if there was an expectation.
- **Read the shapes aloud.** When a `look()` printout appears, ask someone to say the shape in words: "32 sentences by 28 layers by 1,536 numbers." This one habit prevents most confusion later.
- **Use the 🛠️ Tinker cells for "what if" moments,** especially the deliberate errors. Ask: "Before you run it, what do you think the error will say?"
- **Hold the line on language.** Students (and the press) slide quickly from "represents" to "feels". Ask for the sentence without the words "feels" or "conscious".

## What to expect (and how to discuss it)

**The word-counter will probably be strong.** The build and test sentences contain clear sentiment words ("soothed", "burned", "sting"), so a TF–IDF classifier is expected to solve the test set. This is worth discussing, not hiding: a high ruler score alone can't show the model represents bodily sensation beyond word cues. The "no giveaway words" scaffold in Step 7 turns this into an investigation.

**Small numbers, wide intervals.** With 12 validation and 16 test sentences, one mistake moves accuracy by 6–8 points. Several layers may tie on validation; the tie-break rule picks one. Encourage students to describe ranges rather than single numbers.

**Snapshots are very similar to each other.** Step 2's cosine-similarity plot usually shows high similarity even between unrelated sentences, because the shared template dominates. This motivates subtracting averages in Step 3.

**The chosen layer may be early.** Validation uses only 12 sentences, and ties go to the earliest layer. With the real model, several layers may score perfectly, so the rule can pick an early one. That's fine for the probe, but Step 6 then steers at that early layer, where nudges may behave differently than at middle layers. It's a good discussion point (and the *read vs. steer* project in Step 7).

**Steering is variable.** The nudge is deliberately gentle: it's added to the newest position only, and because the cache is off, earlier positions are recomputed without it. It may shift the comfortable-vs-painful preference without changing greedy text, may only work at some strengths, or may produce nonsense. The random-arrow control is essential: if it moves the text as much as the real direction, the effect isn't specific. All of these are legitimate findings.

**Results differ slightly across machines.** Different GPUs and library versions can change small details. Each results ZIP includes a `settings.json` with versions, for comparison.

## Common problems

| Problem | What to do |
|---|---|
| The setup cell asked for a restart | **Runtime → Restart session**, then run the setup cell again and continue. |
| `NameError` (e.g. `train_act is not defined`) | A cell was skipped or the session restarted. Run from the top, in order. |
| The setup cell fails at `git clone` | The repository is private, or `REPO_URL` points to the wrong place (fix with `tools/set_repo_url.py`). |
| No GPU / very slow | **Runtime → Change runtime type → T4 GPU.** If none is available, try later or pair up. |
| "CUDA out of memory" | **Runtime → Restart session.** If it persists, set `MODEL_NAME = 'Qwen/Qwen2.5-0.5B'` and record it as a different experiment. |
| An error mentioning inf or NaN | Make sure the model loads in float32 (the default in `load_model`). |
| Widgets don't appear | Use the backup line at the bottom of each widget cell. |
| The model's text looks like fragments | It's an autocomplete model. Write unfinished descriptions, not questions. |

## Assessment

Use the [student worksheet](worksheet.md) and its 20-point rubric. Step-end 🧭 *Explain it* questions map onto worksheet sections A–E and work well as exit tickets.

## Studying the lab's impact (optional)

If you want to study whether the lab changes how students think about AI (for example, beliefs about AI sentience, or tendencies to anthropomorphise), use a pre/post survey. This is human-subjects research at most institutions: obtain IRB approval or an exemption *before* collecting data.

## Validation status

All notebooks are executed end to end by the automated tests (`tests/`) on a tiny, randomly initialised model with the same architecture as Qwen2.5, on CPU. That checks the mechanics (hooks attach and detach, shapes, plots, controls, generation, numerical scoring, export). It does **not** check scientific results with the real weights.
