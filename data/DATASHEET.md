# Datasheet: Pain–Comfort Lab sentence sets

Following the structure of *Datasheets for Datasets* (Gebru et al., 2021).

## Motivation

**Why was the dataset created?** To give beginners a small, transparent set of sentences for probing whether a language model's internal activations separate descriptions of **physical pain** from descriptions of **physical comfort**, and for testing that separation against controls.

**Who created it?** The lab author (see `CITATION.cff`).

## Composition

| File | Rows | Columns | Contents |
|---|---:|---|---|
| `sentences.csv` | 60 | `split`, `pair_id`, `label`, `category`, `text` | 30 minimal pairs (one comfort, one pain sentence about the same situation) |
| `challenge.csv` | 8 | `challenge_id`, `text`, `type`, `what_makes_it_tricky` | mixed, literal, metaphorical, negated, and mood-vs-sensation sentences, **unlabeled** by design |
| `neutral.csv` | 6 | `text` | sentences with no pain or comfort content |

- `label`: **1 = Comfort, 0 = Pain**. `category` repeats this in words.
- `split`: `build` (16 pairs), `validation` (6 pairs), `test` (8 pairs). Both sentences of a pair are always in the same split, and different splits use different situations, so no situation leaks between splits.
- `pair_id`: links the two sentences of a pair, e.g. `build-03`.
- All sentences are short, invented, third-person English descriptions. No sentence describes a real person.

## Collection process

Sentences were written for this lab. Pairs were designed to keep the object, body part and sentence structure as similar as possible while changing whether the sensation is painful or comfortable.

## Known limitations

- **Giveaway words.** Most sentences contain explicit valence words ("soothed", "burned", "sting"). A bag-of-words classifier is expected to solve the test set, so high probe accuracy on these sentences can't distinguish bodily-sensation representations from word-level sentiment. Step 5 demonstrates this; Step 7 helps students build harder sets.
- **Small size.** 16 test sentences give wide confidence intervals (one error ≈ 6 percentage points).
- **Narrow coverage.** Everyday, mild, mostly skin- and touch-related sensations; one language (English); simple syntax.
- **Labels are the author's judgement.** No inter-rater agreement study has been done. Some comfort sentences describe *relief from* discomfort (e.g. "eased the ache"), which itself mentions pain words.
- **Pronouns.** Both sentences in a pair use the same pronoun, and "her"/"his" each appear in exactly 15 comfort and 15 pain sentences, so pronouns can't explain the comfort/pain split. Only two genders are represented.

## Intended uses

Teaching and small exploratory experiments on open language models. **Not** intended for clinical, diagnostic or pain-assessment use, or for claims about any model's subjective experience.

## Distribution and maintenance

Distributed with the lab repository under CC BY 4.0. Corrections and new sentence sets are welcome by pull request (see `CONTRIBUTING.md`). Changes to existing rows are recorded in `CHANGELOG.md`, because they change results.
