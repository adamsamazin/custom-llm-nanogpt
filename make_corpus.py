"""Generate the four teaching files for the corpus-extension experiment.

Writes corpus/opposites.txt, corpus/categories.txt, corpus/grammar.txt and
corpus/negation.txt from small controlled word lists and varied sentence frames,
the same way the notebook generates its classroom sentences. Seeded, so the files
are reproducible. Run check_corpus.py afterwards.

Rules followed here (see README "Keeping the exam out of the textbook"):
- No eval prompt appears contiguously in any file. Some prompts are only two words
  ("one bird", "the dogs", "yesterday she"), so those exact phrases never occur.
- The tested word pairs and facts are taught only through frames that differ from
  the test frame. The test frame itself ("the opposite of X is Y", "a X is a Y",
  "a X grows into a Y") is used only with pairs that are not in the tests.
- The notebook's loader splits text into separate passages at every ". " sentence
  boundary. The negation tests need a three-sentence context, so those stories are
  written with no space after the mid-story periods (". it" -> ".it"). The tokenizer
  still produces the same tokens as the eval prompts, and the leakage check still
  sees them, but the loader keeps each story together as one passage.
"""
import random
import sys
from pathlib import Path

rng = random.Random(7)
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "corpus")


def story(*sentences):
    """Join sentences into one passage the loader will not split (no space after '.')."""
    return " .".join(sentences) + " ."


# ---------------------------------------------------------------- opposites
# Pairs used inside the test frame "the opposite of X is Y" (never the tested pairs).
FRAME_PAIRS = [("big", "small"), ("tall", "short"), ("long", "short"), ("up", "down"), ("wet", "dry"),
               ("light", "dark"), ("day", "night"), ("fast", "slow"), ("heavy", "light"), ("early", "late"),
               ("loud", "soft"), ("hard", "soft"), ("open", "closed"), ("young", "old"), ("clean", "dirty"),
               ("round", "square"), ("warm", "cool"), ("high", "low"), ("thick", "thin"), ("wide", "narrow"),
               ("rich", "poor"), ("happy", "sad"), ("sweet", "sour"), ("strong", "weak"), ("near", "far"),
               ("top", "bottom"), ("left", "right"), ("push", "pull"), ("start", "stop"), ("wet", "dry")]
# The three tested pairs: taught only through the frames below, never "the opposite of".
TESTED_PAIRS = [("hot", "cold"), ("empty", "full"), ("noisy", "quiet")]
ALL_PAIRS = FRAME_PAIRS + TESTED_PAIRS

OPP_THINGS = {"hot": ["soup", "tea", "sand", "oven", "sun"], "cold": ["snow", "ice", "water", "wind", "river"],
              "empty": ["cup", "bag", "room", "bus", "jar"], "full": ["cup", "bag", "room", "bus", "jar"],
              "noisy": ["street", "market", "drum", "radio", "crowd"], "quiet": ["library", "garden", "night", "room", "lake"],
              "warm": ["blanket", "bath", "bread", "coat"], "cool": ["shade", "drink", "river", "wind"],
              "fast": ["car", "train", "horse", "river"], "slow": ["snail", "turtle", "bus", "walk"],
              "heavy": ["box", "stone", "truck", "bag"], "light": ["feather", "leaf", "paper", "kite"],
              "loud": ["drum", "bell", "horn", "crowd"], "soft": ["pillow", "wool", "voice", "blanket"],
              "early": ["bird", "train", "start", "morning"], "late": ["bus", "night", "dinner", "train"],
              "round": ["ball", "plate", "coin", "cup"], "square": ["box", "tile", "window", "table"],
              "big": ["house", "whale", "hill", "truck"], "small": ["mouse", "coin", "seed", "cup"],
              "wet": ["towel", "grass", "dog", "road"], "dry": ["desert", "towel", "sand", "leaf"],
              "clean": ["shirt", "plate", "floor", "window"], "dirty": ["shirt", "plate", "floor", "window"]}


def opposites():
    lines = []
    for a, b in FRAME_PAIRS:
        for _ in range(4):
            lines.append(rng.choice([f"the opposite of {a} is {b} .", f"the opposite of {b} is {a} .",
                                     f"{a} is the opposite of {b} .", f"{b} is the opposite of {a} ."]))
    for a, b in ALL_PAIRS:
        for _ in range(6):
            lines.append(rng.choice([f"{a} and {b} are opposites .", f"{b} and {a} are opposites .",
                                     f"when it is not {a} it is {b} .", f"when it is not {b} it is {a} .",
                                     f"if something is not {a} then it is {b} .", f"{a} is not {b} .",
                                     f"is it {a} or {b} ?", f"one is {a} and the other is {b} .",
                                     f"{a} means not {b} .", f"{b} means not {a} ."]))
    for a, b in ALL_PAIRS:
        if a in OPP_THINGS and b in OPP_THINGS:
            for _ in range(40 if (a, b) in TESTED_PAIRS else 8):
                x, y = rng.choice(OPP_THINGS[a]), rng.choice(OPP_THINGS[b])
                lines.append(rng.choice([f"the {x} is {a} but the {y} is {b} .", f"the {x} was {a} and the {y} was {b} .",
                                         f"a {x} feels {a} and a {y} feels {b} .", story(f"this {x} is {a}", f"that {y} is {b}"),
                                         f"the {x} is very {a} .", f"the {y} is very {b} .",
                                         story(f"the {x} is not {b}", f"it is {a}"), story(f"the {y} is not {a}", f"it is {b}")]))
    return lines


# ---------------------------------------------------------------- categories
CATS = {"bird": ["sparrow", "eagle", "crow", "owl", "hawk", "swan"],
        "fish": ["trout", "shark", "tuna", "cod", "carp", "eel"],
        "animal": ["dog", "cat", "horse", "goat", "cow", "sheep", "pig", "bear", "duck"],
        "vegetable": ["onion", "potato", "bean", "pea", "cabbage", "lettuce"],
        "fruit": ["banana", "pear", "peach", "mango", "grape", "lemon"],
        "tree": ["oak", "pine", "maple", "birch", "elm", "willow"],
        "tool": ["hammer", "saw", "drill", "wrench", "shovel", "rake"],
        "fabric": ["cotton", "wool", "silk", "linen", "denim", "velvet"],
        "metal": ["iron", "copper", "gold", "silver", "tin", "steel"],
        "vehicle": ["car", "bus", "truck", "van", "jeep", "boat"]}
# Tested facts: robin/bird, salmon/fish, carrot/vegetable, apple/fruit. Taught only in other frames.
TESTED_FACTS = [("robin", "bird"), ("salmon", "fish"), ("carrot", "vegetable"), ("apple", "fruit")]
YOUNG = [("foal", "horse"), ("calf", "cow"), ("lamb", "sheep"), ("kid", "goat"), ("cub", "bear"),
         ("chick", "hen"), ("duckling", "duck"), ("piglet", "pig")]
# Tested: puppy/dog, kitten/cat. Taught only in other frames.
TESTED_YOUNG = [("puppy", "dog"), ("kitten", "cat")]
MASS = {"fabric", "metal"}


def art(word):
    return "an" if word[0] in "aeiou" else "a"


def isa(x, cat):
    return f"{x} is a {cat}" if x in sum([CATS[m] for m in MASS], []) else f"{art(x)} {x} is {art(cat)} {cat}"


def categories():
    lines = []
    members = [(x, c) for c, xs in CATS.items() for x in xs]
    for x, c in members:
        lines.append(f"{isa(x, c)} .")
        lines.append(rng.choice([f"every {x} is {art(c)} {c} .", f"the {x} is {art(c)} {c} .",
                                 f"{x} belongs with the other {c} kind .", f"we call {art(x)} {x} {art(c)} {c} ."]))
    for _ in range(140):
        (x, c), (y, d) = rng.sample(members, 2)
        lines.append(story(isa(x, c), isa(y, d)))
    mods = ["small", "big", "young", "old", "little", "wild", "fat", "thin"]
    spots = ["garden", "river", "market", "kitchen", "field", "shop"]
    for x, c in TESTED_FACTS:
        lines += [f"every {x} is {art(c)} {c} .", f"{x}s are {c}s .", f"this {x} is a {c} too .",
                  f"we call the {x} {art(c)} {c} .", f"the {x} is one kind of {c} .", f"my {x} is {art(c)} {c} .",
                  f"that {x} is {art(c)} {c} .", f"the {x} is a kind of {c} .", f"all {x}s are {c}s ."]
        lines += [f"the {m} {x} is {art(c)} {c} ." for m in mods]
        lines += [f"the {m} {x} is a kind of {c} ." for m in mods]
        lines += [f"the {x} in the {sp} is {art(c)} {c} ." for sp in spots]
        lines += [f"the {x} at the {sp} is {art(c)} {c} ." for sp in spots]
    for y, a in YOUNG:
        for _ in range(4):
            lines.append(rng.choice([f"{art(y)} {y} grows into {art(a)} {a} .", f"the {y} grows into {art(a)} {a} .",
                                     f"{art(y)} {y} is a young {a} .", f"the {y} will become {art(a)} {a} ."]))
    for _ in range(60):
        (y, a), (z, b) = rng.sample(YOUNG, 2)
        lines.append(story(f"{art(y)} {y} grows into {art(a)} {a}", f"{art(z)} {z} grows into {art(b)} {b}"))
    for y, a in TESTED_YOUNG:
        lines += [f"{art(y)} {y} is a young {a} .", f"{art(y)} {y} is a baby {a} .", f"the {y} becomes {art(a)} {a} when it grows .",
                  f"a young {a} is called {art(y)} {y} .", f"a baby {a} is called {art(y)} {y} .", f"every {y} becomes {art(a)} {a} .",
                  f"the {y} will become {art(a)} {a} .", f"the {y} became {art(a)} {a} .", f"the {y} turned into {art(a)} {a} ."]
        lines += [f"the {m} {y} will become {art(a)} {a} ." for m in mods]
        lines += [f"the {m} {y} became {art(a)} {a} ." for m in mods]
        lines += [f"the {m} {y} is a young {a} ." for m in mods]
        lines += [f"the {y} in the {sp} is a young {a} ." for sp in spots]
    return lines


# ---------------------------------------------------------------- grammar
SING = ["one cat", "one dog", "one frog", "one cow", "one boy", "one girl", "a bird", "the bird", "the cat",
        "the dog", "the boy", "the girl", "my dog", "the cow", "the frog", "the child", "the man", "the woman"]
PLUR = ["two birds", "two dogs", "two cats", "the cats", "my dogs", "those dogs", "our dogs", "the birds",
        "the boys", "the girls", "the cows", "the frogs", "the children", "the men", "the women", "three cats"]
PRON_S = ["he", "she", "it"]
PRON_P = ["we", "they", "you"]
PLACES = ["park", "garden", "hill", "road", "field", "river", "house", "school", "market"]
VERBS = ["walk", "walk", "walk", "jump", "play", "talk", "wait", "cook"]  # walk is the tested verb
ADJ = ["happy", "tired", "hungry", "small", "quiet", "wet", "here", "ready", "busy", "late"]


def grammar():
    lines = []
    for _ in range(90):
        s, p, place, adj = rng.choice(SING), rng.choice(PLUR), rng.choice(PLACES), rng.choice(ADJ)
        lines.append(rng.choice([f"{s} is in the {place} .", f"{s} is {adj} .", f"{s} was in the {place} yesterday .",
                                 f"{s} was {adj} yesterday .", f"{s} is at the {place} now .", f"{s} is {adj} today ."]))
        lines.append(rng.choice([f"{p} are in the {place} .", f"{p} are {adj} .", f"{p} were in the {place} yesterday .",
                                 f"{p} were {adj} yesterday .", f"{p} are at the {place} now .", f"{p} are {adj} today ."]))
    for _ in range(40):
        place, adj = rng.choice(PLACES), rng.choice(ADJ)
        pr, pp = rng.choice(PRON_S), rng.choice(PRON_P)
        lines.append(rng.choice([f"{pr} is at the {place} .", f"{pr} is {adj} .", f"{pr} was at the {place} yesterday .",
                                 f"{pp} are at the {place} .", f"{pp} are {adj} .", f"{pp} were at the {place} yesterday .",
                                 f"i am at the {place} .", f"i am {adj} .", f"i was at the {place} yesterday .",
                                 f"i am {adj} today .", f"you are {adj} ."]))
    for _ in range(500):
        v, place = rng.choice(VERBS), rng.choice(PLACES)
        s, p, pr, pp = rng.choice(SING), rng.choice(PLUR), rng.choice(PRON_S), rng.choice(PRON_P)
        subj_s = rng.choice([s, pr, "he", "she", "the girl", "the boy"])
        subj_p = rng.choice([p, pp])
        # "yesterday she" is a test prompt: she never directly follows yesterday here.
        lines.append(rng.choice([
            f"yesterday {subj_s if subj_s != 'she' else 'the girl'} {v}ed at the {place} .",
            f"{subj_s} {v}ed at the {place} yesterday .",
            f"last night {subj_s} {v}ed near the {place} .",
            f"yesterday {subj_p} {v}ed at the {place} .",
            f"{subj_p} {v}ed at the {place} yesterday .",
            f"today {subj_s} {v}s at the {place} .",
            f"{subj_s} {v}s at the {place} every day .",
            f"today {subj_p} {v} at the {place} .",
            f"{subj_p} {v} at the {place} every day .",
            f"{subj_s} is {v}ing at the {place} now .",
            f"{subj_p} are {v}ing at the {place} now .",
            f"i {v}ed at the {place} yesterday .",
            f"i {v} at the {place} every day .",
            f"i am {v}ing at the {place} now .",
            f"tomorrow {subj_s} will {v} at the {place} .",
            f"tomorrow {subj_p} will {v} at the {place} .",
        ]))
    return [l for l in lines if l]


# ---------------------------------------------------------------- negation
NAMES = {"ava": "she", "ben": "he", "cara": "she", "dan": "he", "eli": "he", "fay": "she", "gus": "he",
         "ivy": "she", "jon": "he", "kim": "she", "max": "he", "mia": "she", "tom": "he", "zoe": "she"}
OBJECTS = ["cup", "hat", "car", "ball", "bag", "shirt", "coat", "pen", "sock", "kite"]
COLOURS = ["red", "blue", "green", "yellow", "black", "white", "brown", "pink", "grey", "orange"]
FOODS = ["tea", "milk", "rice", "bread", "soup", "cake", "jam", "eggs", "water", "juice", "coffee", "corn"]
VERBS_N = [("buy", "bought"), ("eat", "ate"), ("drink", "drank"), ("want", "wanted"), ("take", "took"),
           ("pick", "picked"), ("cook", "cooked"), ("choose", "chose"), ("order", "ordered")]
STATE_OBJ = ["gate", "window", "shop", "jar", "bottle", "lid", "road", "cage"]
STATES = [("open", "locked"), ("locked", "open"), ("open", "broken"), ("closed", "open"), ("empty", "full"),
          ("full", "empty"), ("hot", "cold"), ("cold", "warm"), ("clean", "dirty"), ("dry", "wet"),
          ("wide", "narrow"), ("broken", "fixed"), ("missing", "here"), ("closed", "locked")]
# Tested triples never generated: (box, red->blue), (ava, buy tea->milk), (door, open->closed).
BANNED_PAIRS = {("red", "blue"), ("tea", "milk"), ("open", "closed")}


def negation():
    lines = []
    for _ in range(150):
        o = rng.choice(OBJECTS)
        a, b = rng.sample(COLOURS, 2)
        while (a, b) in BANNED_PAIRS:
            a, b = rng.sample(COLOURS, 2)
        n = rng.choice(list(NAMES))
        lines.append(rng.choice([
            story(f"the {o} is not {a}", f"it is {b}", f"the {o} is {b}"),
            story(f"the {o} is not {a}", f"it is {b}", f"so the {o} is {b}"),
            story(f"{n} has a {o}", f"it is not {a}", f"it is {b}", f"the {o} is {b}"),
            story(f"the {o} was not {a}", f"it was {b}", f"the {o} was {b}"),
            story(f"my {o} is not {a}", f"my {o} is {b}", f"the {o} is {b}"),
        ]))
    for _ in range(150):
        n = rng.choice(list(NAMES))
        pr = NAMES[n]
        v, vp = rng.choice(VERBS_N)
        if n == "ava" and v == "buy":
            v, vp = ("want", "wanted")
        a, b = rng.sample(FOODS, 2)
        while (a, b) in BANNED_PAIRS or (v == "buy" and a == "tea"):   # never "did not buy tea"
            a, b = rng.sample(FOODS, 2)
        lines.append(rng.choice([
            story(f"{n} did not {v} {a}", f"{pr} {vp} {b}", f"{n} {vp} {b}"),
            story(f"{n} did not {v} {a}", f"{pr} {vp} {b} instead", f"{n} {vp} {b}"),
            story(f"{n} did not {v} the {a}", f"{pr} {vp} the {b}", f"so {n} {vp} the {b}"),
            story(f"{pr} did not {v} {a}", f"{n} {vp} {b}", f"{n} {vp} {b} today"),
        ]))
    for _ in range(120):
        o = rng.choice(STATE_OBJ)
        a, b = rng.choice(STATES)
        if (a, b) in BANNED_PAIRS:
            a, b = ("closed", "locked")
        lines.append(rng.choice([
            story(f"the {o} is not {a}", f"it is {b}", f"the {o} is {b}"),
            story(f"the {o} is not {a}", f"it is {b}", f"so the {o} is {b}"),
            story(f"the {o} was not {a}", f"it was {b}", f"the {o} was {b}"),
            story(f"the {o} is not {a} now", f"it is {b}", f"the {o} is {b}"),
        ]))
    # Vocabulary support for tested objects and distractor words, outside the tested frames.
    support = ["the box was heavy .", "ben put the hat in the box .", "the box has a lid .", "a cup is in the box .",
               "the big box was full .", "kim opened the box .", "there is a pen in the box .", "the box was empty .",
               "the door was locked last night .", "the old door was heavy .", "a door has a key .", "tom painted the door .",
               "the door of the shop was open .", "gus fixed the door .", "the door was wide .", "mia opened the door .",
               "the road is wide .", "a wide road has room for a bus .", "the river is wide here .",
               "my sock is missing .", "the key is missing .", "one pen is missing from the bag .",
               "the gate is wide open .", "the shop is closed at night .", "the window is closed .",
               "ava is in the garden .", "ava was at the market .", "ava has a red kite .", "ava is happy today .",
               "the rice is hot .", "the bread is soft .", "the milk is cold .", "the tea is warm ."]
    lines += support
    adjs = ["heavy", "empty", "full", "big", "small", "old", "new", "clean"]
    lines += [f"{n} put the {o} in the box ." for n in NAMES for o in OBJECTS[:5]]
    lines += [f"the box was {a} ." for a in adjs] + [f"the box is {a} ." for a in adjs if a not in ("red", "blue")]
    lines += [f"{n} opened the door ." for n in NAMES] + [f"{n} painted the door {c} ." for n in list(NAMES)[:6] for c in COLOURS[:4]]
    lines += [f"the door was {a} ." for a in adjs] + [f"{n} knocked on the door ." for n in NAMES]
    lines += [f"the {w} is wide ." for w in ["road", "river", "gate", "field", "street", "window"]]
    lines += [f"my {o} is missing ." for o in OBJECTS] + [f"{n} said the {o} is missing ." for n in list(NAMES)[:5] for o in OBJECTS[:4]]
    return lines


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in [("opposites", opposites), ("categories", categories), ("grammar", grammar), ("negation", negation)]:
        lines = fn()
        (OUT / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}.txt: {len(lines)} lines, {len(set(lines))} unique")
