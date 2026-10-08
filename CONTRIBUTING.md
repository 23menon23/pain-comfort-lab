# Contributing

Thank you for helping improve the lab. Contributions from instructors and students are welcome: new sentence sets, clearer explanations, bug fixes, translations and new Step 7 scaffolds.

## Ground rules for notebooks

The lab's main design goal is that **beginners never get lost in the code**. When you add or change a code cell:

- After any line that returns something new, add a 📦 *What came back?* `look(...)` with named dimensions.
- For any non-obvious line, add a row to a 🔍 walk-through table: *what it does* and *why it's written this way*.
- Explain any parameter value a student might wonder about (🎛️), and any choice of data structure (🧱).
- Ask for a ✏️ prediction before results a student could reason about.
- Avoid claims that the model feels, wants or understands anything.
- **Commit notebooks without outputs** (in Jupyter: *Edit → Clear Outputs of All Cells*). Pre-filled outputs spoil predictions.

## Changing the data

Changes to existing rows in `data/` change everyone's results. Prefer adding a **new** file (e.g. `data/no_giveaway_pairs.csv`) with a short section in `data/DATASHEET.md`. Record any change in `CHANGELOG.md`.

## Running the tests

```bash
pip install -r requirements.txt pytest nbclient ipykernel
pytest -q
```

The tests run every notebook end to end on a tiny random model (no download, CPU only). They check that the code runs, not that the science is right, so please also run changed notebooks on a Colab GPU with the real model.
