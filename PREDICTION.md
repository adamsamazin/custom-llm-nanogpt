### My prediction

**My three choices**

- **Corpus:** Experiment 1 uses the supplied classroom sentences only, with `corpus/` empty. Experiment 2 keeps the classroom sentences and adds four teaching files I wrote for the extension skills *opposites*, *categories and analogies*, *grammar*, and *negation*. I chose the first three because each is a short, local pattern (a frame plus a word pair) that a 2-block, 64-number model can plausibly memorize from varied examples. I added negation as a deliberate stretch: it requires copying the corrected word from an earlier sentence, which I expect this model to fail at, and I want one category where I can separate "the words are now in the vocabulary" from "the model learned the pattern".
- **Training steps: 3,000** for both experiments. The 10-step setup check confirmed the pipeline runs. Holding the budget fixed keeps the corpus as the only difference between the two required runs.
- **Learning rate: 0.001** for both, with the notebook's warmup and cosine decay. This is the default; the model has only ~112k parameters and a 136-word vocabulary, so I would rather keep the well-tested value than tune it and confound the comparison. A much larger rate risks the loss diverging; a much smaller one would leave the model closer to its random start after 3,000 steps.

**What I expect to see**

- **Validation loss.** The untrained model scores 4.93, which is ln(136): it is guessing uniformly over the vocabulary. The classroom corpus is eight fixed sentence frames, so most words in a sentence are predictable once the frame is identified; the real uncertainty is in the noun, context and adjective slots. I predict validation loss falls to roughly 1.0–1.4 by step 3,000, with training and validation loss nearly equal because the held-out sentences share the same templates.
- **Generated text.** Untrained samples are word salad. I expect grammatical template sentences by the halfway point (step 1,500) and mostly domain-consistent sentences (fruit words with the kitchen, medical words with the hospital) by the end, with occasional cross-domain mixes.
- **Neighbours of `customer`.** Right now its nearest neighbours are random. After training I expect them to be the other nouns that share its slot and contexts: client, buyer, shopper, consumer, subscriber.
- **First parameter update.** Tiny. At step 0 the warmup learning rate is 0.001 / 100 = 0.00001, and AdamW's first step moves each weight by roughly that amount.
- **Language evals, experiment 1.** starter_patterns close to 16/16; starter_transfer around 4/8 because the model depends on templates; extend_corpus 0/24 because those words are not in the vocabulary (24 unscorable cases).
- **Language evals, experiment 2.** Coverage rises from 24 to about 36 scorable cases. Opposites, categories and grammar: at least 6 of 9 correct. Negation: scorable but at or near chance (0–1 of 3). Starter scores should hold, though the new words may slightly dilute the starter patterns.
