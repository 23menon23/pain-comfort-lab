# Student investigation worksheet

**Complete this in your own words.** Clear explanations and honest limitations matter more than a high score. A result that "didn't work" can still earn full credit if you explain it well. You can fill this in a Markdown cell at the end of a notebook, or in a short document, as your instructor directs.

Name(s): ________________________  Date: ____________  Model used: ____________________

## A. Explain the experiment *(Steps 0–2)*

1. Explain the difference between a **weight** and an **activation** using an analogy of your own.
2. Explain a **token**, a **layer** and a **direction** in one sentence each.
3. Describe the shape of `train_act` in words. What would change if you added two sentences? If you used a model with 24 layers?
4. State the lab's main question as a testable prediction (a hypothesis), and describe one result that would count *against* it.

## B. Report the frozen-ruler results *(Steps 3–5)*

| Item | Your result |
|---|---|
| Selected layer (1–28) | |
| Why this layer was selected | |
| Final test: correct / total, and accuracy | |
| Plausible range for accuracy | |
| Final test AUC | |
| Word-counter accuracy | |
| Share of shuffled-label rulers matching or beating ours | |
| Share of random-direction rulers matching or beating ours | |

- Why didn't we use the test set to choose the layer?
- What does the word-counter's result tell you, and what does it **not** tell you?

## C. Inspect three challenge or mystery sentences *(Step 4)*

Include at least one metaphor or negation and one mixed sensation. Fill in your prediction **before** measuring. Not every sentence has a single right label.

| Sentence | Your interpretation before running | Observed ruler score | What might explain the result? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

For one surprising result, give **two different possible explanations** (for example: word clues, mixed sensations, general mood, the template ending, the small number of build sentences).

## D. Compare nudging conditions *(Step 6)*

Use the **same prompt** for every row. Copy the model's actual output; don't invent examples.

Prompt: ______________________________________________

| Condition | α | Actual continuation | Sensation described | Coherence (1–5) |
|---|---:|---|---|---:|
| Pain direction | −1 | | | |
| No nudge | 0 | | | |
| Comfort direction | +1 | | | |
| Random arrow | +1 | | | |

Did the numerical preference (Part 5 of Step 6) change **consistently** across all four prompts? Did the random arrow do the same? Remember that numbers can change even when the generated text looks the same.

## E. Conclusion (150–250 words)

Answer these in connected prose:

- What could our ruler read from the model's numbers, on these sentences?
- Did nudging add evidence? Which result supports your answer?
- What did the fake rulers, the word-counter and the tricky sentences reveal?
- What are two limitations, and what would you test next?
- Why does the experiment **not** establish that the model experiences pain or pleasure?

You may begin: *"Our results provide evidence that … under the tested conditions. They do not establish … . A follow-up test would … ."*

## What to submit

- Your saved notebooks **with outputs** (File → Download → .ipynb, or File → Save a copy in Drive).
- The results ZIP files exported at the end of Steps 4–7.
- This completed worksheet.

## Rubric (20 points)

| Criterion | Points |
|---|---:|
| Clear explanation of model, activation, shape and direction concepts | 4 |
| Correct use of build, validation and test sets; accurate reporting | 4 |
| Interpretation of challenge examples and controls | 4 |
| Fair comparison of nudging conditions, including coherence | 4 |
| Evidence-based conclusion, limitations and proposed follow-up | 4 |
