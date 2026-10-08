# Research ideas from the Pain–Comfort Lab

*Adapted from "Research Ideas from the Pain–Comfort AI Lab" by Pratibha Menon (October 2026).*

## Start here

The lab answered one question, but the same tools can answer dozens more, and many of them nobody has tested yet. This guide shows where to look and how to turn curiosity into a real experiment. Research doesn't mean discovering something no one has ever imagined. A good project asks a clear question, tests it fairly, and reports honestly, even when the answer is "it didn't work".

**How to use this guide**

1. Skim the map of research areas below and pick one that makes you curious.
2. Read that area's section: the big question, what's already known, and questions you could test.
3. Use the research recipe (in [Step 7](../notebooks/07_your_investigation.ipynb)) to turn your question into an experiment.
4. Pick a starter project at your level, or invent your own.

Talk to your advisor before you start. A ten-minute conversation can save you a week of work.

## The six research areas at a glance

In all six, professional researchers are still working out the answers, so a careful student project can add something real.

| Area | The big question | Where you met it in the lab |
|---|---|---|
| 1. Probing | What information is hidden in the model's numbers? | Steps 2–4 |
| 2. Concepts and confounds | Is the model tracking physical sensation, mood, or just words? | Steps 4 and 5 |
| 3. Steering | Can nudging a model's numbers change what it writes, in a controlled way? | Step 6 |
| 4. Trustworthy explanations | How do we know an explanation of AI is true, not just convincing? | Step 5 |
| 5. How models differ | Do other models, sizes or languages show the same patterns? | Step 3 |
| 6. Big questions | What can experiments like this tell us about AI, experience and fairness? | Throughout |

Areas 1–5 involve running experiments in the notebooks. Area 6 includes projects that need no code at all.

## Area 1 · Probing: what's hidden in the numbers?

**The big question:** what does a model represent at each layer, and how is it organised?

**What's known:** a probe is a simple measuring tool, like our pain–comfort ruler, applied to a model's internal numbers. Researchers have used probes to find information about grammar, word meaning, sentiment, and even whether the model treats a statement as true or false. Probing is one of the most widely used tools for looking inside AI models.

**The catch:** a probe shows that information can be *read out* of the numbers. It doesn't show the model *uses* that information. A thermometer can read the temperature of a room without heating it.

**Questions you could test**

- **The template:** our snapshot uses the ending "The bodily sensation is". Does the best layer change with "It felt", or no ending at all? *(Step 7, Recipe 1)*
- **Where to look:** we read the last token only. Does averaging over every token work better or worse? *(`reduce='mean'`)*
- **How much data:** we built the ruler from 16 pairs. Try 2, 4, 8 and 16. How few do you need before it stops working? *(Step 3, optional cell)*
- **More than two categories:** can a probe tell *burning* pain from *sharp* pain, or warmth from softness?
- **Related concepts:** build a hot–cold direction and a rough–smooth direction. Do they point the same way as pain–comfort? (Compare directions with *cosine similarity*: 1 means the same direction, 0 means unrelated.)

## Area 2 · Concepts and confounds: what is the direction really tracking?

**The big question:** when our ruler separates pain from comfort, is it tracking physical sensation, general mood, or just certain words?

**What's known:** a *confound* is a hidden second explanation for your result. Our sentences mix three things at once: physical sensation, positive or negative words ("soothed", "burned"), and mood. In fact, the simple word-counter in Step 5 is expected to solve the lab's test set, so word clues alone can do the lab's task. That isn't a failure. It's an open puzzle, and solving it is a real research contribution.

**Questions you could test**

- **No giveaway words:** write sentences where pain or comfort is implied by the situation, not stated ("She stepped barefoot onto the asphalt at noon in July"). Does the ruler still work? Does the word-counter? *(Step 7, Scaffold A)*
- **Mood vs. sensation:** build a second direction from happy vs. sad sentences that mention no physical sensation. Is it the same arrow as pain–comfort, or a different one? *(Step 7, Recipe 4)*
- **Negation:** "The shot didn't hurt at all." Does the model handle *not*, or does it react to "hurt"?
- **Metaphor:** "a burning desire", "a painful meeting", "a soft voice". Where do these land on the ruler?
- **Emotional pain:** does heartbreak or grief land on the same side as a burned hand?

This area connects naturally to psychology and linguistics. If you're studying either, you have a head start.

## Area 3 · Steering: can we change what a model writes?

**The big question:** if we nudge a model's internal numbers, does its behaviour change in a predictable, controlled way?

**What's known:** researchers have used this kind of nudging, often called *activation steering*, to shift a model's tone, topic and style without retraining it. Steering is exciting because it tests cause and effect, not just correlation. It's also tricky: text can turn into nonsense, a random arrow can change the output too, and it's easy to show only the examples that worked.

**Questions you could test**

- **Dose and response:** try α from −2 to +2 in small steps. Plot how the comfortable-vs-painful preference changes. At what strength does the text stop making sense? *(Step 6, optional cell)*
- **Best layer for reading vs. steering:** the layer that probes best isn't always the one that steers best. Steer at every layer and compare.
- **Where to nudge:** we nudge only the last token. What happens if you nudge every token?
- **New prompt styles:** does steering still work in a short story, a dialogue or a product review?
- **Blind ratings:** have classmates rate generated text for sensation and sense-making *without knowing which condition produced it*. Blind rating is a standard technique for avoiding bias.

**Something to discuss:** steering could make AI safer, for example by reducing harmful outputs. It could also be misused. Who should be allowed to steer a model, and should users be told?

## Area 4 · Trustworthy explanations: is it true, or just convincing?

**The big question:** how can we tell whether an explanation of an AI system is *faithful* to what the model really does, rather than just *plausible*?

**What's known:** this lab is part of a field called *explainable AI* (XAI). One lesson from XAI research is that explanations can look convincing and still be wrong. Some popular explanation methods have failed simple "sanity checks", producing nearly the same explanation even for a model with scrambled weights. That's why the lab includes fake rulers and a word-counter: they check whether our explanation beats the obvious alternatives.

**Questions you could test**

- **More fake rulers:** run 1,000 random directions instead of 200. How often does a random one match or beat the real ruler?
- **Stability:** reshuffle which sentence pairs go into the build, validation and test sets, five different ways. Does the chosen layer stay the same?
- **What the word-counter relies on:** Step 5 lists its strongest words. Remove those words from your sentences and retest both methods. (Explanation tools such as SHAP or LIME can go further.)
- **Pre-registration:** before running a new experiment, write down your prediction and what result would prove you wrong. Afterwards, compare. How often were you right?

This matters beyond the lab. Laws and company policies increasingly ask whether AI decisions can be explained, so knowing how to test an explanation is a valuable skill.

## Area 5 · How models differ: is the pattern universal?

**The big question:** is the pain–comfort direction a quirk of one model, or do many models organise this concept in similar ways?

**What's known:** researchers often find that different models learn surprisingly similar internal patterns, but not always, and often not at the same layer. Comparing models is a good way to learn which findings are general and which are accidents.

**Questions you could test**

- **Model size:** switch to the smaller Qwen2.5-0.5B (one line in the load cell). Does the best layer sit at a similar *relative* depth, say 60% of the way through?
- **Base vs. chat model:** try Qwen2.5-1.5B-Instruct, the chatbot version of the same model. Does chat training change the direction, or how well steering works?
- **Other languages:** Qwen models handle many languages. Translate the sentences into Spanish, Chinese or another language you know. Does a ruler built from English sentences still work?
- **Other model families:** try a model from a different developer. `pclab.get_layers` already looks for layers under several common names, but some models need small code changes, so this is a good Researcher-level project.

**A practical note:** free Colab can handle models up to a few billion parameters. Very large models won't fit, so pick comparisons that stay small.

## Area 6 · Big questions: AI, experience and fairness

**The big question:** what can experiments like this tell us about AI and society, and where do they reach their limits?

The lab can't show that a model feels anything. But it raises real questions in philosophy, ethics and media studies, and some of them make excellent projects. Several need no code at all.

**Questions you could explore**

- **Evidence for experience:** what *would* count as evidence that an AI system has experiences? Why isn't "it represents pain-related language" enough? A classic philosophy-of-mind question with a new twist.
- **How we talk about AI (no code):** collect news headlines and company announcements that describe AI as "thinking", "feeling" or "knowing". How common is this language, and how might it shape public trust?
- **Moral status debates:** some philosophers and AI companies have started asking whether future AI systems could deserve moral consideration, while others think the question is premature. Map the main arguments on each side.
- **Fairness check:** take one pain sentence and swap in different names. Does the score change when only the name changes? Doctors are known to sometimes underestimate pain in certain groups of patients, so finding out whether AI models pick up similar patterns matters, especially as AI is used in healthcare. *(Step 7, Scaffold B)*
- **Rules for steering:** if companies can change a model's behaviour by nudging its internal numbers, what should they be required to disclose to users?

## From question to experiment: a research recipe

1. **Ask a question you can test.** "Does AI understand pain?" is too big. "Does our pain–comfort direction also separate emotional pain from emotional comfort?" can be tested in a week.
2. **Write down your prediction**, and what result would prove it wrong, *before* you run anything.
3. **Change one thing at a time.** If you change the model *and* the sentences, you won't know which change caused your result.
4. **Plan your data.** Write at least 10 pairs of new sentences, more if you can. Keep a test set sealed until the end, just like the lab does.
5. **Choose your comparison.** Random directions, the word-counter, and the original lab setup are all good choices.
6. **Run and record everything.** Save the exported ZIP files and a copy of your notebook. Keep notes on everything you tried, including what failed.
7. **Analyse honestly.** Did your result beat the controls? Is it bigger than noise? With 16 test sentences, a single mistake changes accuracy by about 6 points.
8. **Explain it.** Give at least two possible explanations, name the limitations, suggest a next experiment.
9. **Share it.** See below.

**Fill in this sentence before you start:**

> We will test whether \_\_\_\_\_\_ by changing \_\_\_\_\_\_ while keeping \_\_\_\_\_\_ the same. We predict \_\_\_\_\_\_. If \_\_\_\_\_\_ happens instead, our prediction is wrong.

## Starter projects by level

**Explorer** projects only change sentences or settings; **Investigator** projects need small code edits; **Researcher** projects need new code.

| Project | Level | The question | Area |
|---|---|---|---|
| Metaphor hunt | Explorer | Where do 20 metaphorical pain and comfort phrases land on the ruler? | 2 |
| Name-swap fairness check | Explorer | Does a pain sentence's score change when only the person's name changes? | 6 |
| Template test | Explorer | Does changing the ending "The bodily sensation is" change the best layer? | 1 |
| How media describes AI | Explorer (no code) | How often do headlines describe AI as feeling or thinking? | 6 |
| No-giveaway-words test | Investigator | Does the ruler still work when pain is implied, not stated? | 2 |
| Steering strength curve | Investigator | How does the effect grow with α, and when does text break? | 3 |
| Small vs. large model | Investigator | Does the best layer sit at the same relative depth in a smaller model? | 5 |
| Mood vs. sensation | Investigator | Is a happy–sad direction the same arrow as pain–comfort? | 2 |
| Cross-language transfer | Researcher | Does a ruler built from English sentences work in another language? | 5 |
| Best layer to read vs. steer | Researcher | Is the layer that probes best also the one that steers best? | 3 |
| Beating the word-counter | Researcher | Can you design a test the word-counter fails but the ruler passes? | 4 |
| Base vs. chat model | Researcher | Does chat training change the pain–comfort direction? | 5 |

## Sharing your work, and doing it right

**Where to share:** a club presentation, a poster at your campus research day, a write-up on GitHub or a blog, and later, national venues such as the National Conference on Undergraduate Research (NCUR), ACM student research competitions, and undergraduate research journals. Your advisor can help you choose.

**How to structure a write-up:** your question, what you did, what you found, how it compared with the controls, the limitations, and what you'd test next. Keep it short and include your charts.

**Research etiquette**

- **Cite your tools and sources:** this lab (see [`CITATION.cff`](../CITATION.cff)), the Qwen2.5 model, and the research papers behind the methods.
- **Say what's yours:** state clearly what you added: new sentences, a new comparison, a new analysis.
- **AI use:** you may use AI tools if your advisor's policy allows. If you do, follow four rules: **use it, disclose it, verify it, own it.**
- **Don't overclaim:** write "the model's internal numbers separate pain and comfort descriptions", not "the model feels pain".
- **Report what didn't work:** a carefully tested null result is a real finding. Hiding failed attempts, or showing only the best examples, is *cherry-picking*.
- **Keep it safe:** use made-up sentences, never personal or sensitive information.

## Reading list

These are research papers, so they get technical. Read the abstract and introduction first, and ask your advisor for help with the rest.

- Alain and Bengio (2016), [Understanding intermediate layers using linear classifier probes](https://arxiv.org/abs/1610.01644): the idea behind our ruler.
- Kim et al. (2018), [Testing with Concept Activation Vectors (TCAV)](https://arxiv.org/abs/1711.11279): building directions for human concepts.
- Adebayo et al. (2018), [Sanity Checks for Saliency Maps](https://arxiv.org/abs/1810.03292): when convincing explanations fail.
- Hewitt and Liang (2019), [Designing and Interpreting Probes with Control Tasks](https://arxiv.org/abs/1909.03368): why probes need controls.
- Turner et al. (2023), [Steering Language Models With Activation Engineering](https://arxiv.org/abs/2308.10248): nudging models by adding directions.
- Zou et al. (2023), [Representation Engineering](https://arxiv.org/abs/2310.01405): reading and steering concepts inside models.
- Panickssery et al. (2023), [Steering Llama 2 via Contrastive Activation Addition](https://arxiv.org/abs/2312.06681): the closest method to our lab's nudge.
- Qwen Team (2024), [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115): the model used in the lab.
