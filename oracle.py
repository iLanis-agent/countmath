#!/usr/bin/env python3
# Count Math oracle - mirrors engine.js using math.perm / math.comb / math.factorial and itertools for small words.
import json, math, re
from collections import Counter
from itertools import permutations

def _int(text, label, lo, hi):
    t = text.strip() if isinstance(text, str) else ""
    err = f"{label} must be a whole number from {lo} to {hi}"
    if not re.fullmatch(r"[0-9]{1,8}", t):
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def num(x):
    s = str(x)
    if len(s) <= 15:
        return f"{x:,}"
    r = (int(s[:4]) + 5) // 10
    ex = len(s) - 1
    if r == 1000:
        r, ex = 100, ex + 1
    return f"about {r // 100}.{r % 100:02d} x 10^{ex}"

def ways(x):
    return num(x) + (" way" if x == 1 else " ways")

def order_truth(n, k):
    nn = _int(n, "things", 1, 100); kk = _int(k, "picks", 0, 100)
    if kk > nn:
        raise ValueError("picks cannot be more than things")
    prod = " (" + " x ".join(str(nn - j) for j in range(kk)) + ")" if 2 <= kk <= 6 else ""
    return (f"Picking {kk} of {nn} {'thing' if nn == 1 else 'things'}: {ways(math.perm(nn, kk))} when order matters{prod}, "
            f"{ways(math.comb(nn, kk))} when order does not matter.")

def pair_truth(n):
    nn = _int(n, "people", 2, 1000000)
    pairs = math.comb(nn, 2)
    return (f"{nn} people each shaking hands once with every other person make {num(pairs)} {'handshake' if pairs == 1 else 'handshakes'} "
            f"({nn} x {nn - 1} / 2, not {nn} x {nn - 1} = {num(nn * (nn - 1))}).")

def word_truth(word):
    w = word.strip().upper() if isinstance(word, str) else ""
    if not re.fullmatch(r"[A-Z]{2,20}", w):
        raise ValueError("enter 2 to 20 letters, A to Z only")
    c = Counter(w)
    if len(w) <= 8:
        orders = len(set(permutations(w)))  # brute force
    else:
        orders = math.factorial(len(w))
        for v in c.values():
            orders //= math.factorial(v)
    total = math.factorial(len(w))
    reps = [f"{ch} appears {c[ch]} times" for ch in sorted(c) if c[ch] > 1]
    if not reps:
        why = "because no letter repeats"
    elif len(reps) == 1:
        why = f"instead of {num(total)}, because {reps[0]}"
    else:
        why = f"instead of {num(total)}, because {', '.join(reps[:-1])} and {reps[-1]}"
    return f"The letters of {w} ({len(w)} letters) can be arranged in {num(orders)} different {'order' if orders == 1 else 'orders'}, {why}."

FNS = {"orderTruth": order_truth, "pairTruth": pair_truth, "wordTruth": word_truth}
CASES = [
    ("orderTruth", ["10", "3"]), ("orderTruth", ["52", "5"]), ("orderTruth", ["5", "5"]), ("orderTruth", ["1", "1"]),
    ("orderTruth", ["10", "0"]), ("orderTruth", ["10", "1"]), ("orderTruth", ["10", "2"]), ("orderTruth", ["49", "6"]),
    ("orderTruth", ["100", "50"]), ("orderTruth", ["100", "100"]), ("orderTruth", ["100", "7"]), ("orderTruth", ["20", "6"]),
    ("orderTruth", ["2", "1"]), ("orderTruth", ["26", "4"]), ("orderTruth", [" 8 ", " 3 "]), ("orderTruth", ["3", "4"]),
    ("orderTruth", ["0", "0"]), ("orderTruth", ["101", "1"]), ("orderTruth", ["10", "-1"]), ("orderTruth", ["abc", "1"]),
    ("orderTruth", ["10", "1.5"]), ("orderTruth", ["", "1"]),
    ("pairTruth", ["10"]), ("pairTruth", ["2"]), ("pairTruth", ["3"]), ("pairTruth", ["23"]), ("pairTruth", ["1000"]),
    ("pairTruth", ["1000000"]), ("pairTruth", ["1"]), ("pairTruth", ["1000001"]), ("pairTruth", ["abc"]), ("pairTruth", ["0"]),
    ("wordTruth", ["BANANA"]), ("wordTruth", ["CAT"]), ("wordTruth", ["AA"]), ("wordTruth", ["AB"]), ("wordTruth", ["mississippi"]),
    ("wordTruth", ["abcdefghijklmnopqrst"]), ("wordTruth", ["aaaaaaaaaaaaaaaaaaaa"]), ("wordTruth", ["LETTER"]), ("wordTruth", [" level "]),
    ("wordTruth", ["BOOKKEEPER"]), ("wordTruth", ["A"]), ("wordTruth", ["abcdefghijklmnopqrstu"]), ("wordTruth", ["two words"]),
    ("wordTruth", ["abc1"]), ("wordTruth", [""]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
