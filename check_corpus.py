"""Pre-training checks for the teaching corpus. Reads the eval suite for the leakage
check only; never trains, never builds the real vocabulary, and is not a training input.

Usage:  python check_corpus.py [--folder corpus] [--cases lang_25,lang_26,...]

1. Leakage: reports any corpus file containing an eval prompt (the same normalized
   contiguous match that the notebook uses to reject files).
2. Vocabulary simulation: rebuilds the notebook's pipeline (classroom sentences +
   folder files -> reserve eval prefixes -> dedupe -> seeded 90/10 split -> count
   training tokens -> keep the 509 most frequent) and reports, for each eval case,
   whether every prompt and choice word would be in vocabulary, with counts.
3. Spirit check: flags passages that contain an answer-bearing phrase for a target
   case (e.g. "salmon is a fish") so near-copies of the answer key can be reviewed.
"""
import argparse
import random
import re
from collections import Counter
from pathlib import Path

from run_evals import load_suite, matching_cases, normalized, reserve_classroom_passages

SEED, BLOCK_SIZE, KEEP = 42, 48, 509


def word_tokens(text):
    return re.findall(r"\w+(?:[']\w+)*|[^\w\s]", text.lower(), flags=re.UNICODE)


def chunk_text(text, max_tokens=47):
    chunks = []
    for unit in re.split(r"(?<=[.!?])\s+|\n+", text):
        tokens = word_tokens(unit)
        chunks.extend(" ".join(tokens[i:i + max_tokens]) for i in range(0, len(tokens), max_tokens))
    return chunks


def classroom_corpus():
    """Verbatim copy of the notebook's generator (section 3)."""
    domains = [
        ("customer client buyer shopper consumer subscriber", "service purchase support order", "store"),
        ("product item package brand merchandise offering", "price quality delivery design", "market"),
        ("loan credit mortgage investment bond deposit", "interest risk payment return", "bank"),
        ("apple banana orange pear peach mango", "fruit taste juice harvest", "kitchen"),
        ("car bus train truck taxi bicycle", "travel route traffic journey", "station"),
        ("software application program platform website system", "code data security update", "office"),
        ("doctor nurse physician surgeon therapist dentist", "patient health care treatment", "hospital"),
        ("teacher tutor instructor professor educator lecturer", "student lesson course learning", "school"),
    ]
    sentences = []
    for nouns, contexts, place in domains:
        for noun in nouns.split():
            for context in contexts.split():
                for adjective in ["new", "local", "important", "different"]:
                    for frame in [
                        "the team discussed the {noun} and the {context} at the {place} .",
                        "we learned about the {adjective} {noun} during a discussion of {context} .",
                        "the report about the {noun} explains the {context} in detail .",
                        "our {place} has a question about the {adjective} {noun} and {context} .",
                        "they compared the {adjective} {noun} with another {noun} at the {place} .",
                        "a review of {context} helped us understand the {adjective} {noun} .",
                        "today the {place} focused on {context} and the {adjective} {noun} .",
                        "the {adjective} {noun} was mentioned in the {context} report yesterday .",
                    ]:
                        sentences.append(frame.format(noun=noun, context=context, place=place, adjective=adjective))
    for noun in "customer client buyer shopper consumer subscriber".split():
        for product in "product item package brand merchandise offering".split():
            for verb in "ordered reviewed compared returned recommended selected".split():
                sentences.append(f"the {noun} {verb} the {product} after checking the price .")
    return "\n".join(sentences)


# Answer-bearing phrases for the twelve target cases (spirit check; the notebook does not use these).
ANSWER_PHRASES = {
    "lang_25": ["one bird is"], "lang_26": ["the dogs are"], "lang_27": ["yesterday she walked"],
    "lang_28": ["opposite of hot is cold"], "lang_29": ["opposite of empty is full"],
    "lang_30": ["opposite of noisy is quiet"],
    "lang_31": ["the box is blue", "not red . it is blue"], "lang_32": ["ava bought milk", "not buy tea"],
    "lang_33": ["the door is closed", "not open . it is closed"],
    "lang_46": ["a salmon is a fish"], "lang_47": ["kitten grows into a cat"], "lang_48": ["an apple is a fruit"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", default="corpus")
    parser.add_argument("--cases", default="lang_25,lang_26,lang_27,lang_28,lang_29,lang_30,"
                                            "lang_31,lang_32,lang_33,lang_46,lang_47,lang_48")
    args = parser.parse_args()
    suite = load_suite("evals/language_evals.json")
    cases = {c["id"]: c for c in suite["cases"]}
    targets = args.cases.split(",")

    root = Path(args.folder)
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md"}
                   and p.name != "README.md" and not any(part.startswith(".") for part in p.relative_to(root).parts))
    extra = []
    print("== 1. Leakage check (exact normalized prompt match) ==")
    leaks = False
    for path in files:
        text = path.read_text(encoding="utf-8-sig")
        hits = matching_cases(text, suite)
        chunks = chunk_text(text, BLOCK_SIZE - 1)
        types = len(set(t for c in chunks for t in c.split()))
        extra.extend(chunks)
        print(f"  {path.name}: {len(chunks)} passages, {len(set(chunks))} unique, {types} word types"
              + (f"  LEAK -> {hits}" if hits else "  ok"))
        leaks |= bool(hits)
    if not files:
        print("  (no corpus files found)")

    base, sep = reserve_classroom_passages(chunk_text(classroom_corpus(), BLOCK_SIZE - 1), suite)
    docs = sorted(set(base + extra))
    random.Random(SEED).shuffle(docs)
    train = docs[:int(.9 * len(docs))]
    counts = Counter(t for d in train for t in word_tokens(d))
    retained = sorted((t for t in counts if len(t) <= 128), key=lambda t: (-counts[t], t))[:KEEP]
    vocab = set(retained)
    threshold = counts[retained[-1]] if len(counts) > KEEP else 0
    print(f"\n== 2. Vocabulary simulation ==")
    print(f"  reserved classroom passages: {sep['excluded_passages']} | unique passages: {len(docs):,}"
          f" (classroom {len(set(base)):,} + new {len(set(extra) - set(base)):,}) | train {len(train):,}")
    print(f"  training word types: {len(counts)} | retained: {len(retained)} (cap {KEEP})"
          f" | omitted: {len(counts) - len(retained)} | count needed to stay in vocabulary: {threshold}")
    scorable = 0
    for cid, case in cases.items():
        words = word_tokens(case["prompt"]) + [word_tokens(c)[0] for c in case["choices"]]
        missing = sorted({w for w in words if w not in vocab})
        ok = not missing and len(word_tokens(case["prompt"])) + 1 <= BLOCK_SIZE
        scorable += ok
        if cid in targets or (missing and case["group"] != "extend_corpus"):
            detail = ", ".join(f"{w}={counts.get(w, 0)}" for w in dict.fromkeys(words))
            state = "SCORABLE" if ok else "unscorable: missing " + str(missing)
            print(f"  {cid} [{case['category']}] {state}\n      {detail}")
    print(f"  => {scorable}/48 cases would be scorable")

    print("\n== 3. Spirit check (answer-bearing phrases in any passage) ==")
    flagged = 0
    for cid in targets:
        for phrase in ANSWER_PHRASES.get(cid, []):
            hits = [d for d in set(extra) if normalized(phrase) in normalized(d)]
            if hits:
                flagged += len(hits)
                print(f"  {cid}: '{phrase}' appears in {len(hits)} passage(s), e.g. '{hits[0]}'")
    print("  none" if not flagged else f"  {flagged} passage(s) flagged for review")
    if leaks:
        raise SystemExit("\nFAIL: exact eval prompt found in corpus. The notebook would reject this folder.")


if __name__ == "__main__":
    main()
