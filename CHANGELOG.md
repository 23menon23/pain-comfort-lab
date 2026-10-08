# Changelog

Changes to `data/` are listed explicitly because they change results.

## 1.0.0 (unreleased)

First public release.

- Restructured the single-notebook lab (CMIS 4250 Pain–Pleasure XAI Lab, v2.0) into eight inquiry-based steps (`notebooks/00`–`07`).
- New Step 0 on reading ML code: data structures, shapes and axes, masks, broadcasting, reading errors.
- Every step now includes 📦 *What came back?* inspection cells, 🔍 line-by-line code walk-throughs, 🎛️ parameter explanations, 🧱 data-structure explanations and 🛠️ tinker prompts.
- New explorations: first-token vs. last-token snapshots, hook vs. `hidden_states` comparison, snapshot similarity by layer, loop vs. `einsum` scoring, sample-size curve, direction vs. PCA alignment, word-counter feature weights, next-token probabilities under steering, dose–response curve.
- New Step 7 with pre-registration, a "no giveaway words" scaffold and a name-swap fairness scaffold.
- Helper code moved to the small `pclab` package; sentences moved to `data/*.csv` with a datasheet. Sentence content is unchanged from v2.0.
- The exact model version is now recorded on all Transformers versions (asked of the Hugging Face Hub when the library no longer stores it).
- Hook clean-up checks now compare hook counts before and after (recent Transformers versions attach their own hooks).
- Added automated tests that execute every notebook on a tiny random model.
