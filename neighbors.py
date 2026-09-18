"""Nearest neighbours of chosen words in the saved embedding tables (cosine, all 64 dims).

Reads a run's checkpoint.json (initial and final token embeddings, as the embedding
viewer does) and prints the top-5 neighbours before and after training. Inference-only.

Usage: python neighbors.py results/expanded/checkpoint.json customer cold kitten
"""
import json
import sys

import torch


def neighbours(table, vocabulary, word, k=5):
    index = vocabulary.index(word)
    vectors = torch.nn.functional.normalize(torch.tensor(table), dim=1)
    scores = vectors @ vectors[index]
    scores[index] = -2  # exclude the word itself
    top = torch.topk(scores, k)
    return [(vocabulary[i], round(v.item(), 3)) for v, i in zip(top.values, top.indices)]


def main():
    path, words = sys.argv[1], sys.argv[2:]
    ck = json.loads(open(path, encoding="utf-8").read())
    vocab = ck["vocabulary"]
    out = {}
    for word in words:
        if word not in vocab:
            print(f"{word}: not in vocabulary")
            continue
        before = neighbours(ck["initial_embeddings"], vocab, word)
        after = neighbours(ck["weights"]["wte"], vocab, word)
        out[word] = {"id": vocab.index(word), "before": before, "after": after}
        print(f"{word} (id {vocab.index(word)})")
        print("  before:", ", ".join(f"{w} {s}" for w, s in before))
        print("  after: ", ", ".join(f"{w} {s}" for w, s in after))
    if out:
        target = path.replace("checkpoint.json", "neighbors.json")
        open(target, "w", encoding="utf-8").write(json.dumps(out, indent=2))
        print("saved", target)


if __name__ == "__main__":
    main()
